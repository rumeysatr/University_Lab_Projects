"""
Fakülte ve Bölüm verilerini güncelleme scripti.
Bu script mevcut veritabanındaki fakülte ve bölüm kayıtlarını
doğru code ve head_name/dean_name değerleri ile günceller.
"""

import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "123",
    "database": "universite_sinav_db"
}


def update_faculty_department_data():
    
    # Fakülte verileri: (name, code, dean_name)
    faculties_data = [
        ("Mühendislik Fakültesi", "MUH", "Prof. Dr. Ahmet Kaya"),
        ("İktisadi ve İdari Bilimler Fakültesi", "IIBF", "Prof. Dr. Hasan Şahin"),
        ("Tıp Fakültesi", "TIP", "Prof. Dr. Mustafa Eren"),
    ]
    
    # Bölüm verileri: (name, code, head_name, faculty_code)
    departments_data = [
        # Mühendislik Fakültesi bölümleri
        ("Bilgisayar Mühendisliği", "BM", "Prof. Dr. Ayşe Yılmaz", "MUH"),
        ("Yazılım Mühendisliği", "YM", "Doç. Dr. Mehmet Demir", "MUH"),
        ("Endüstri Mühendisliği", "EM", "Dr. Öğr. Üyesi Fatma Çelik", "MUH"),
        
        # İktisadi ve İdari Bilimler Fakültesi bölümleri
        ("İşletme", "ISL", "Prof. Dr. Ali Vural", "IIBF"),
        ("İktisat", "IKT", "Doç. Dr. Zeynep Aksoy", "IIBF"),
        ("Uluslararası İlişkiler", "ULI", "Dr. Öğr. Üyesi Burak Yıldız", "IIBF"),
        
        # Tıp Fakültesi bölümleri
        ("Temel Tıp Bilimleri", "TTB", "Prof. Dr. Kemal Öztürk", "TIP"),
    ]
    
    conn = None
    try:
        print("[*] Veritabanına bağlanılıyor...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("\n[*] Mevcut fakülte ve bölüm verileri temizleniyor...")
        
        cur.execute("UPDATE lecturers SET department_id = NULL")
        print(f"  [OK] {cur.rowcount} öğretim üyesinin bölüm bağlantısı kaldırıldı")
        
        cur.execute("UPDATE courses SET department_id = NULL")
        print(f"  [OK] {cur.rowcount} dersin bölüm bağlantısı kaldırıldı")
        
        cur.execute("UPDATE users SET department_id = NULL")
        print(f"  [OK] {cur.rowcount} kullanıcının bölüm bağlantısı kaldırıldı")
        
        cur.execute("DELETE FROM departments")
        print(f"  [OK] {cur.rowcount} bölüm silindi")
        
        cur.execute("DELETE FROM faculties")
        print(f"  [OK] {cur.rowcount} fakülte silindi")
        
        print("\n[*] Fakülteler ekleniyor...")
        faculty_ids = {}  
        
        for name, code, dean_name in faculties_data:
            cur.execute("""
                INSERT INTO faculties (name, code, dean_name, is_active)
                VALUES (%s, %s, %s, TRUE)
                RETURNING id
            """, (name, code, dean_name))
            faculty_id = cur.fetchone()[0]
            faculty_ids[code] = faculty_id
            print(f"  [OK] Fakülte eklendi: {code} - {name} (ID: {faculty_id})")
        
        print("\n[*] Bölümler ekleniyor...")
        department_ids = {} 
        
        for name, code, head_name, faculty_code in departments_data:
            faculty_id = faculty_ids.get(faculty_code)
            if faculty_id is None:
                print(f"  [HATA] Fakülte bulunamadı: {faculty_code}")
                continue
                
            cur.execute("""
                INSERT INTO departments (name, code, head_name, faculty_id, is_active)
                VALUES (%s, %s, %s, %s, TRUE)
                RETURNING id
            """, (name, code, head_name, faculty_id))
            dept_id = cur.fetchone()[0]
            department_ids[code] = dept_id
            print(f"  [OK] Bölüm eklendi: {code} - {name} (Başkan: {head_name}, ID: {dept_id})")
        
        print("\n[*] Öğretim üyeleri bölümlere atanıyor...")
        dept_id_list = list(department_ids.values())
        
        if dept_id_list:
            cur.execute("SELECT id FROM lecturers")
            lecturers = cur.fetchall()
            
            for i, (lecturer_id,) in enumerate(lecturers):
                assigned_dept_id = dept_id_list[i % len(dept_id_list)]
                cur.execute("""
                    UPDATE lecturers SET department_id = %s WHERE id = %s
                """, (assigned_dept_id, lecturer_id))
            
            print(f"  [OK] {len(lecturers)} öğretim üyesi bölümlere atandı")
        
        print("\n[*] Dersler bölümlere atanıyor...")
        if dept_id_list:
            cur.execute("SELECT id FROM courses")
            courses = cur.fetchall()
            
            for i, (course_id,) in enumerate(courses):
                assigned_dept_id = dept_id_list[i % len(dept_id_list)]
                cur.execute("""
                    UPDATE courses SET department_id = %s WHERE id = %s
                """, (assigned_dept_id, course_id))
            
            print(f"  [OK] {len(courses)} ders bölümlere atandı")
        
        print("\n[*] Kullanıcılar bölümlere atanıyor...")
        if dept_id_list:
            cur.execute("SELECT id FROM users WHERE role != 'admin'")
            users = cur.fetchall()
            
            for i, (user_id,) in enumerate(users):
                assigned_dept_id = dept_id_list[i % len(dept_id_list)]
                cur.execute("""
                    UPDATE users SET department_id = %s WHERE id = %s
                """, (assigned_dept_id, user_id))
            
            print(f"  [OK] {len(users)} kullanıcı bölümlere atandı")
        
        conn.commit()
        print("\n" + "="*50)
        print("[OK] Tum fakulte ve bolum verileri basariyla guncellendi!")
        print("="*50)
        
        print("\n[OZET]:")
        print("-"*50)
        
        cur.execute("""
            SELECT f.code, f.name, f.dean_name
            FROM faculties f
            ORDER BY f.id
        """)
        faculties = cur.fetchall()
        
        for f_code, f_name, f_dean in faculties:
            dean_info = f" (Dekan: {f_dean})" if f_dean else ""
            print(f"\n[FAKULTE] {f_code} - {f_name}{dean_info}")
            
            cur.execute("""
                SELECT d.code, d.name, d.head_name
                FROM departments d
                WHERE d.faculty_id = (SELECT id FROM faculties WHERE code = %s)
                ORDER BY d.id
            """, (f_code,))
            departments = cur.fetchall()
            
            for d_code, d_name, d_head in departments:
                print(f"   +-- {d_code} - {d_name}")
                print(f"       Bolum Baskani: {d_head}")
        
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
    update_faculty_department_data()
