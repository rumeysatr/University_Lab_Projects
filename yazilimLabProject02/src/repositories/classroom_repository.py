"""
Derslik repository sınıfı
"""

from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.models.classroom import Classroom


class ClassroomRepository(BaseRepository[Classroom]):
    """Derslik veritabanı erişim sınıfı"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "classrooms"
    
    def _row_to_entity(self, row: tuple, columns: List[str]) -> Classroom:
        data = dict(zip(columns, row))
        return Classroom.from_dict(data)
    
    def _entity_to_values(self, entity: Classroom) -> tuple:
        return (
            entity.name,
            entity.faculty_id,
            entity.capacity,
            entity.has_computer,
            entity.is_suitable
        )
    
    def get_all(self) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            ORDER BY f.name, c.name
        """
        rows, columns = self._execute_query(query)
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_by_id(self, id: int) -> Optional[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.id = %s
        """
        rows, columns = self._execute_query(query, (id,))
        if rows:
            return self._row_to_entity(rows[0], columns)
        return None
    
    def create(self, classroom: Classroom) -> int:
        query = """
            INSERT INTO classrooms (name, faculty_id, capacity, has_computer, is_suitable)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        values = self._entity_to_values(classroom)
        return self._execute_non_query(query, values, return_id=True)
    
    def update(self, classroom: Classroom) -> bool:
        query = """
            UPDATE classrooms
            SET name = %s, faculty_id = %s, capacity = %s, has_computer = %s, is_suitable = %s
            WHERE id = %s
        """
        values = self._entity_to_values(classroom) + (classroom.id,)
        try:
            self._execute_non_query(query, values)
            return True
        except Exception:
            return False
    
    def get_by_faculty(self, faculty_id: int) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.faculty_id = %s
            ORDER BY c.name
        """
        rows, columns = self._execute_query(query, (faculty_id,))
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_by_min_capacity(self, min_capacity: int) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.capacity >= %s
            ORDER BY c.capacity
        """
        rows, columns = self._execute_query(query, (min_capacity,))
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_available_for_exam(self, exam_date: str, start_time: str, end_time: str) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.is_suitable = TRUE
            AND c.id NOT IN (
                SELECT es.classroom_id FROM exam_schedule es
                WHERE es.exam_date = %s
                AND es.status != 'cancelled'
                AND (
                    (es.start_time <= %s AND es.end_time > %s)
                    OR (es.start_time < %s AND es.end_time >= %s)
                    OR (es.start_time >= %s AND es.end_time <= %s)
                )
            )
            ORDER BY c.capacity
        """
        rows, columns = self._execute_query(
            query,
            (exam_date, start_time, start_time, end_time, end_time, start_time, end_time)
        )
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_faculties(self) -> List[dict]:
        query = """
            SELECT DISTINCT f.id, f.name
            FROM classrooms c
            JOIN faculties f ON c.faculty_id = f.id
            ORDER BY f.name
        """
        rows, _ = self._execute_query(query)
        return [{'id': row[0], 'name': row[1]} for row in rows]
    
    def get_suitable_classrooms(self, min_capacity: int = 0) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.is_suitable = TRUE AND c.capacity >= %s
            ORDER BY c.capacity
        """
        rows, columns = self._execute_query(query, (min_capacity,))
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_exam_suitable_classrooms(self) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.is_suitable = TRUE
            ORDER BY f.name, c.name
        """
        rows, columns = self._execute_query(query)
        return [self._row_to_entity(row, columns) for row in rows]
    
    def get_available_classrooms(self, exam_date: str, start_time: str, end_time: str) -> List[Classroom]:
        query = """
            SELECT c.id, c.name, c.faculty_id, c.capacity, c.has_computer, c.is_suitable,
                   f.name as faculty_name
            FROM classrooms c
            LEFT JOIN faculties f ON c.faculty_id = f.id
            WHERE c.is_suitable = TRUE
            AND c.id NOT IN (
                SELECT es.classroom_id FROM exam_schedule es
                WHERE es.exam_date = %s
                AND es.status != 'cancelled'
                AND (
                    (es.start_time < %s AND es.end_time > %s)
                    OR (es.start_time < %s AND es.end_time > %s)
                    OR (es.start_time >= %s AND es.end_time <= %s)
                )
            )
            ORDER BY f.name, c.name
        """
        rows, columns = self._execute_query(
            query,
            (exam_date, end_time, start_time, end_time, start_time, start_time, end_time)
        )
        return [self._row_to_entity(row, columns) for row in rows]
