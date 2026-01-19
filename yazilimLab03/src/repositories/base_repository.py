"""
Temel repository sınıfı - CRUD operasyonları

Transaction yönetimi ve eager loading desteği içerir.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any, Callable
from contextlib import contextmanager
import logging

from src.config.database import get_connection, release_connection

T = TypeVar('T')
logger = logging.getLogger(__name__)


class TransactionContext:
    """Transaction yönetimi için context manager."""
    
    def __init__(self, connection):
        self.connection = connection
        self.committed = False
    
    def commit(self):
        """Transaction'ı commit et."""
        if not self.committed:
            self.connection.commit()
            self.committed = True
            logger.debug("Transaction committed")
    
    def rollback(self):
        """Transaction'ı geri al."""
        if not self.committed:
            self.connection.rollback()
            logger.debug("Transaction rolled back")


class BaseRepository(ABC, Generic[T]):
    
    def __init__(self):
        self.table_name: str = ""
        self._current_transaction: Optional[TransactionContext] = None
    
    @abstractmethod
    def _row_to_entity(self, row: tuple, columns: List[str]) -> T:
        pass
    
    @abstractmethod
    def _entity_to_values(self, entity: T) -> tuple:
        pass
    
    @contextmanager
    def transaction(self):
        """
        Transaction context manager.
        
        Kullanım:
            with repository.transaction() as tx:
                repository.create(entity1)
                repository.create(entity2)
                tx.commit()
        """
        conn = None
        try:
            conn = get_connection()
            tx = TransactionContext(conn)
            self._current_transaction = tx
            logger.debug(f"Transaction started for {self.table_name}")
            yield tx
            
            # Auto-commit if not manually committed
            if not tx.committed:
                tx.commit()
                
        except Exception as e:
            logger.error(f"Transaction error in {self.table_name}: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            self._current_transaction = None
            if conn:
                release_connection(conn)
    
    def execute_in_transaction(self, operations: List[Callable]) -> bool:
        """
        Birden fazla operasyonu tek transaction içinde çalıştırır.
        
        Args:
            operations: Çalıştırılacak operasyonlar (callable list)
            
        Returns:
            bool: Tüm operasyonlar başarılı mı
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            for operation in operations:
                operation(cursor)
            
            conn.commit()
            logger.info(f"{len(operations)} operasyon transaction içinde başarıyla tamamlandı")
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Transaction operasyonlarında hata: {e}")
            return False
        finally:
            if conn:
                release_connection(conn)
    
    def _execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            cursor.close()
            logger.debug(f"Query executed: {query[:50]}... returned {len(rows)} rows")
            return rows, columns
        except Exception as e:
            logger.error(f"Query error: {e}")
            raise
        finally:
            if conn:
                release_connection(conn)
    
    def _execute_non_query(self, query: str, params: tuple = None, return_id: bool = False) -> Optional[int]:
        """INSERT, UPDATE, DELETE sorgusu çalıştırır"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            result = None
            if return_id:
                cursor.execute("SELECT LASTVAL()")
                result = cursor.fetchone()[0]
            
            conn.commit()
            cursor.close()
            logger.debug(f"Non-query executed: {query[:50]}...")
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Non-query error: {e}")
            raise
        finally:
            if conn:
                release_connection(conn)
    
    def _execute_batch(self, query: str, params_list: List[tuple]) -> int:
        """
        Batch operasyon çalıştırır (N+1 sorgu problemini çözer).
        
        Args:
            query: SQL query template
            params_list: Parametre listesi
            
        Returns:
            int: Etkilenen satır sayısı
        """
        if not params_list:
            return 0
        
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Batch execute
            from psycopg2.extras import execute_batch
            execute_batch(cursor, query, params_list, page_size=100)
            
            affected = cursor.rowcount
            conn.commit()
            cursor.close()
            
            logger.info(f"Batch query executed: {len(params_list)} items, {affected} affected")
            return affected
            
        except ImportError:
            # execute_batch yoksa tek tek çalıştır
            logger.warning("execute_batch not available, falling back to individual queries")
            count = 0
            for params in params_list:
                self._execute_non_query(query, params)
                count += 1
            return count
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Batch query error: {e}")
            raise
        finally:
            if conn:
                release_connection(conn)
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """
        Tüm kayıtları getirir.
        
        Args:
            limit: Maksimum kayıt sayısı (sayfalama için)
            offset: Başlangıç offset (sayfalama için)
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []
        
        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params = [limit, offset]
        
        rows, columns = self._execute_query(query, tuple(params) if params else None)
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_by_id(self, id: int) -> Optional[T]:
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        rows, columns = self._execute_query(query, (id,))
        if rows:
            return self._row_to_entity(rows[0], columns)
        return None
    
    def get_by_ids(self, ids: List[int]) -> List[T]:
        """
        Birden fazla ID ile kayıt getirir (N+1 sorgu problemini çözer).
        
        Args:
            ids: ID listesi
            
        Returns:
            Entity listesi
        """
        if not ids:
            return []
        
        placeholders = ', '.join(['%s'] * len(ids))
        query = f"SELECT * FROM {self.table_name} WHERE id IN ({placeholders})"
        rows, columns = self._execute_query(query, tuple(ids))
        return [self._row_to_entity(row, columns) for row in rows]
    
    def delete(self, id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        try:
            self._execute_non_query(query, (id,))
            logger.info(f"Deleted from {self.table_name}: id={id}")
            return True
        except Exception as e:
            logger.error(f"Delete error: {e}")
            return False
    
    def delete_batch(self, ids: List[int]) -> int:
        """
        Birden fazla kaydı siler.
        
        Args:
            ids: Silinecek ID listesi
            
        Returns:
            int: Silinen kayıt sayısı
        """
        if not ids:
            return 0
        
        placeholders = ', '.join(['%s'] * len(ids))
        query = f"DELETE FROM {self.table_name} WHERE id IN ({placeholders})"
        
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, tuple(ids))
            affected = cursor.rowcount
            conn.commit()
            cursor.close()
            logger.info(f"Batch deleted from {self.table_name}: {affected} records")
            return affected
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Batch delete error: {e}")
            return 0
        finally:
            if conn:
                release_connection(conn)
    
    def count(self, where_clause: str = None, params: tuple = None) -> int:
        """
        Kayıt sayısını döndürür.
        
        Args:
            where_clause: WHERE koşulu (opsiyonel)
            params: WHERE parametreleri
        """
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        rows, _ = self._execute_query(query, params)
        return rows[0][0] if rows else 0
    
    def exists(self, id: int) -> bool:
        query = f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id = %s)"
        rows, _ = self._execute_query(query, (id,))
        return rows[0][0] if rows else False
    
    def search(self, column: str, value: Any, limit: int = 100) -> List[T]:
        """
        Sütunda arama yapar.
        
        Args:
            column: Aranacak sütun
            value: Aranacak değer
            limit: Maksimum sonuç sayısı
        """
        query = f"SELECT * FROM {self.table_name} WHERE {column} ILIKE %s LIMIT %s"
        rows, columns = self._execute_query(query, (f"%{value}%", limit))
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_with_relations(self, id: int, relations: List[str]) -> Optional[T]:
        """
        İlişkileriyle birlikte kayıt getirir (eager loading).
        
        Args:
            id: Kayıt ID
            relations: Yüklenecek ilişki adları
            
        Returns:
            İlişkileriyle yüklenmiş entity
            
        Not: Alt sınıflarda override edilmeli
        """
        # Varsayılan davranış: sadece entity'yi getir
        return self.get_by_id(id)
