import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "123",
    "database": "universite_sinav_db"
}

def migrate_all_tables():
    conn = None
    try:
        print("Veritabanina baglaniliyor...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("\nCourses tablosu kontrol ediliyor...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'courses'
        """)
        course_columns = [row[0] for row in cur.fetchall()]
        print("  Mevcut kolonlar:", course_columns)
        
        if 'code' not in course_columns:
            cur.execute("ALTER TABLE courses ADD COLUMN code VARCHAR(20)")
            print("  code kolonu eklendi")
        
        if 'department_id' not in course_columns:
            cur.execute("ALTER TABLE courses ADD COLUMN department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL")
            print("  department_id kolonu eklendi")
        
        if 'is_active' not in course_columns:
            cur.execute("ALTER TABLE courses ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
            print("  is_active kolonu eklendi")
        
        if 'created_at' not in course_columns:
            cur.execute("ALTER TABLE courses ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("  created_at kolonu eklendi")
        
        if 'updated_at' not in course_columns:
            cur.execute("ALTER TABLE courses ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("  updated_at kolonu eklendi")
            
            cur.execute("""
                CREATE TRIGGER update_courses_updated_at
                    BEFORE UPDATE ON courses
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
            """)
            print("  updated_at trigger eklendi")
        
        cur.execute("SELECT COUNT(*) FROM courses WHERE code IS NULL OR code = ''")
        if cur.fetchone()[0] > 0:
            print("  Derslere otomatik kod ataniyor...")
            cur.execute("""
                UPDATE courses 
                SET code = 'DERS' || LPAD(id::text, 3, '0')
                WHERE code IS NULL OR code = ''
            """)
            print(f"  {cur.rowcount} ders için kod atandi")
        
        print("\nExam_schedule tablosu tamamlaniyor...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'exam_schedule'")
        exam_columns = [row[0] for row in cur.fetchall()]
        
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'classrooms' AND column_name = 'building'
        """)
        building_exists = cur.fetchone()
        
        if building_exists:
            cur.execute("""
                SELECT DISTINCT es.id, c.building
                FROM exam_schedule es
                JOIN classrooms c ON es.classroom_id = c.id
                WHERE (SELECT COUNT(*) FROM information_schema.columns
                       WHERE table_name = 'exam_schedule' AND column_name = 'building') = 0
            """)
            building_data = cur.fetchall()
            
            if building_data and 'building' not in exam_columns:
                cur.execute("ALTER TABLE exam_schedule ADD COLUMN building VARCHAR(50)")
                for exam_id, building in building_data:
                    cur.execute("UPDATE exam_schedule SET building = %s WHERE id = %s", (building, exam_id))
                print(f"  {len(building_data)} sinav icin building bilgisi eklendi")
        
        cur.execute("""
            SELECT DISTINCT es.id, c.name 
            FROM exam_schedule es
            JOIN classrooms c ON es.classroom_id = c.id
            WHERE (SELECT COUNT(*) FROM information_schema.columns 
                   WHERE table_name = 'exam_schedule' AND column_name = 'classroom_name') = 0
        """)
        classroom_data = cur.fetchall()
        
        if classroom_data and 'classroom_name' not in exam_columns:
            cur.execute("ALTER TABLE exam_schedule ADD COLUMN classroom_name VARCHAR(50)")
            for exam_id, classroom_name in classroom_data:
                cur.execute("UPDATE exam_schedule SET classroom_name = %s WHERE id = %s", (classroom_name, exam_id))
            print(f"  {len(classroom_data)} sinav icin classroom_name bilgisi eklendi")
        
        cur.execute("""
            SELECT DISTINCT es.id, l.first_name, l.last_name 
            FROM exam_schedule es
            JOIN courses c ON es.course_id = c.id
            JOIN lecturers l ON c.lecturer_id = l.id
            WHERE (SELECT COUNT(*) FROM information_schema.columns 
                   WHERE table_name = 'exam_schedule' AND column_name = 'lecturer_name') = 0
        """)
        lecturer_data = cur.fetchall()
        
        if lecturer_data and 'lecturer_name' not in exam_columns:
            cur.execute("ALTER TABLE exam_schedule ADD COLUMN lecturer_name VARCHAR(100)")
            for exam_id, first_name, last_name in lecturer_data:
                lecturer_name = f"{first_name} {last_name}".strip()
                cur.execute("UPDATE exam_schedule SET lecturer_name = %s WHERE id = %s", (lecturer_name, exam_id))
            print(f"  {len(lecturer_data)} sinav icin lecturer_name bilgisi eklendi")
        
        cur.execute("""
            SELECT DISTINCT es.id, c.code, c.name 
            FROM exam_schedule es
            JOIN courses c ON es.course_id = c.id
            WHERE (SELECT COUNT(*) FROM information_schema.columns 
                   WHERE table_name = 'exam_schedule' AND column_name = 'course_code') = 0
        """)
        course_data = cur.fetchall()
        
        if course_data:
            if 'course_code' not in exam_columns:
                cur.execute("ALTER TABLE exam_schedule ADD COLUMN course_code VARCHAR(20)")
                print("  course_code kolonu eklendi")
            if 'course_name' not in exam_columns:
                cur.execute("ALTER TABLE exam_schedule ADD COLUMN course_name VARCHAR(100)")
                print("  course_name kolonu eklendi")
                
            for exam_id, course_code, course_name in course_data:
                cur.execute("""
                    UPDATE exam_schedule 
                    SET course_code = %s, course_name = %s
                    WHERE id = %s
                """, (course_code, course_name, exam_id))
            print(f"  {len(course_data)} sinav icin kurs bilgileri eklendi")
        
        conn.commit()
        print("\nTum migration islemleri basariyla tamamlandi!")
        
    except Exception as e:
        print(f"\nHata: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print("Baglanti kapatildi.")

if __name__ == '__main__':
    migrate_all_tables()