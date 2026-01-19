"""
Fakültelere dekan ekleme scripti.
Bu script mevcut veritabanındaki fakültelere uygun dekan bilgilerini ekler.
"""

import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "123",
    "database": "universite_sinav_db"
}


def add_faculty_deans():
    """Fakültelere dekan bilgisi ekler"""
    
    # Fakülte kodları ve atanacak dekan isimleri
    # Her fakülte için uygun bir dekan ismi belirliyoruz
    deans_data = {
        "MUH": "Prof. Dr. Ahmet Kaya",      # Mühendislik Fakültesi Dekanı
        "IIBF": "Prof. Dr. Hasan Şahin",    # İktisadi ve İdari Bilimler Fakültesi Dekanı
        "TIP": "Prof. Dr. Mustafa Eren",    # Tıp Fakültesi Dekanı
        "ECZ": "Prof. Dr. Aylin Yıldırım",  # Eczacılık Fakültesi Dekanı
    }
    
    conn = None
    try:
        print("[*] Veritabanına bağlanılıyor...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Önce mevcut fakülteleri listele
        print("\n[*] Mevcut fakülteler kontrol ediliyor...")
        cur.execute("SELECT id, code, name, dean_name FROM faculties ORDER BY id")
        faculties = cur.fetchall()
        
        if not faculties:
            print("[UYARI] Veritabanında fakülte bulunamadı!")
            print("[*] Önce db_seeder.py veya update_faculty_department_data.py çalıştırın.")
            return
        
        print(f"\n[*] {len(faculties)} fakülte bulundu:")
        for f_id, f_code, f_name, f_dean in faculties:
            dean_status = f_dean if f_dean else "DEKAN YOK"
            print(f"   ID: {f_id} | {f_code} - {f_name} | Dekan: {dean_status}")
        
        # Fakültelere dekan ata
        print("\n[*] Dekanlara atama yapılıyor...")
        updated_count = 0
        
        for f_id, f_code, f_name, current_dean in faculties:
            if f_code in deans_data:
                new_dean = deans_data[f_code]
                
                # Eğer zaten dekan varsa atlama (boş veya sadece "-" ise dekan yok sayılır)
                if current_dean and current_dean.strip() and current_dean.strip() != "-":
                    print(f"   [ATLANDI] {f_code}: Zaten dekan mevcut ({current_dean})")
                    continue
                
                cur.execute("""
                    UPDATE faculties 
                    SET dean_name = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (new_dean, f_id))
                
                print(f"   [OK] {f_code} - {f_name}: Dekan atandı -> {new_dean}")
                updated_count += 1
            else:
                print(f"   [UYARI] {f_code}: Bu fakülte için dekan bilgisi tanımlı değil")
        
        conn.commit()
        
        # Sonuçları göster
        print("\n" + "="*60)
        print(f"[OK] {updated_count} fakülteye dekan ataması yapıldı!")
        print("="*60)
        
        # Güncel durumu göster
        print("\n[GÜNCEL DURUM]:")
        print("-"*60)
        
        cur.execute("""
            SELECT f.id, f.code, f.name, f.dean_name,
                   (SELECT COUNT(*) FROM departments d WHERE d.faculty_id = f.id) as dept_count
            FROM faculties f
            ORDER BY f.id
        """)
        updated_faculties = cur.fetchall()
        
        for f_id, f_code, f_name, f_dean, dept_count in updated_faculties:
            print(f"\n[FAKÜLTE] {f_code} - {f_name}")
            print(f"   Dekan: {f_dean if f_dean else 'Atanmadı'}")
            print(f"   Bağlı Bölüm Sayısı: {dept_count}")
        
    except Exception as e:
        print(f"\n[HATA] Bir hata oluştu: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            print("\n[*] Veritabanı bağlantısı kapatıldı.")


if __name__ == "__main__":
    add_faculty_deans()
