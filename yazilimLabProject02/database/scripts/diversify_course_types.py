"""
Ders türlerini çeşitlendirme scripti
Zorunlu derslerin bir kısmını Alan Seçmeli, Üniversite Seçmeli ve Proje olarak günceller
"""

import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import psycopg2

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'universite_sinav_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )


def diversify_course_types(conn):
    print("\n[COURSE_TYPE] Ders türleri çeşitlendiriliyor...")
    cur = conn.cursor()
    
    cur.execute("SELECT id, name, code FROM courses ORDER BY id")
    courses = cur.fetchall()
    
    course_types_distribution = ['Zorunlu'] * 60 + ['Alan Seçmeli'] * 20 + ['Üniversite Seçmeli'] * 10 + ['Proje'] * 10
    
    updated_counts = {'Zorunlu': 0, 'Alan Seçmeli': 0, 'Üniversite Seçmeli': 0, 'Proje': 0}
    
    for course_id, name, code in courses:
        name_lower = name.lower() if name else ""
        
        if any(keyword in name_lower for keyword in ['proje', 'bitirme', 'tasarım', 'staj']):
            new_type = 'Proje'
        elif any(keyword in name_lower for keyword in ['matematik', 'fizik', 'algoritma', 'veri yapı', 'programlama', 'veritaban']):
            new_type = 'Zorunlu'
        else:
            new_type = random.choice(course_types_distribution)
        
        cur.execute(
            "UPDATE courses SET course_type = %s WHERE id = %s",
            (new_type, course_id)
        )
        updated_counts[new_type] += 1
    
    conn.commit()
    
    print("  Ders Türü Dağılımı:")
    for type_name, count in updated_counts.items():
        print(f"    - {type_name}: {count} ders")
    
    return sum(updated_counts.values())


def update_has_exam_for_project_courses(conn):
    print("\n[HAS_EXAM] Proje derslerinde sınav durumu güncelleniyor...")
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE courses 
        SET has_exam = FALSE 
        WHERE course_type = 'Proje'
    """)
    project_count = cur.rowcount
    
    cur.execute("""
        UPDATE courses 
        SET has_exam = TRUE 
        WHERE course_type != 'Proje'
    """)
    exam_count = cur.rowcount
    
    conn.commit()
    print(f"  - {project_count} proje dersinde sınav yok")
    print(f"  - {exam_count} derste sınav var")
    
    return project_count


def show_final_stats(conn):
    """Son durumu göster"""
    cur = conn.cursor()
    
    print("\n" + "=" * 60)
    print("GÜNCEL DERS İSTATİSTİKLERİ")
    print("=" * 60)
    
    # Ders türü dağılımı
    cur.execute("""
        SELECT course_type, COUNT(*), 
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM courses), 1) as yuzde
        FROM courses 
        GROUP BY course_type 
        ORDER BY COUNT(*) DESC
    """)
    print("\nDers Türü Dağılımı:")
    for row in cur.fetchall():
        print(f"  - {row[0]}: {row[1]} ders (%{row[2]})")
    
    # Sınav durumu
    cur.execute("""
        SELECT 
            SUM(CASE WHEN has_exam THEN 1 ELSE 0 END) as sinavli,
            SUM(CASE WHEN NOT has_exam THEN 1 ELSE 0 END) as sinavsiz
        FROM courses
    """)
    result = cur.fetchone()
    print(f"\nSınav Durumu:")
    print(f"  - Sınavlı: {result[0]} ders")
    print(f"  - Sınavsız: {result[1]} ders")
    
    cur.execute("""
        SELECT credit, COUNT(*) 
        FROM courses 
        GROUP BY credit 
        ORDER BY credit
    """)
    print("\nKredi Dağılımı:")
    for row in cur.fetchall():
        print(f"  - {row[0]} kredi: {row[1]} ders")
    
    print("=" * 60)


def main():
    print("=" * 60)
    print("DERS TÜRLERİ ÇEŞİTLENDİRME")
    print("=" * 60)
    
    try:
        conn = get_connection()
        print("[OK] Veritabanına bağlandı.")
        
        diversify_course_types(conn)
        update_has_exam_for_project_courses(conn)
        show_final_stats(conn)
        
        conn.close()
        print("\n[OK] İşlem tamamlandı!")
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
