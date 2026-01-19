"""
Ders verilerini duzeltme scripti
- Ders adlarindaki rastgele sayilari temizler
- Ogretim uyesi eksik olan dersler icin yeni ogretim uyeleri olusturur
"""

import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'universite_sinav_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )


def clean_course_name(name):
    if not name:
        return name

    cleaned = re.sub(r'\s+\d{3,}$', '', name.strip())
    return cleaned.strip()


def fix_course_names(conn):
    print("\n[DERS ADLARI] Duzeltiliyor...")
    
    cur = conn.cursor()
    
    cur.execute("SELECT id, name FROM courses ORDER BY id")
    courses = cur.fetchall()
    
    updated_count = 0
    for course_id, name in courses:
        cleaned_name = clean_course_name(name)
        
        if cleaned_name != name:
            print(f"  - Duzeltildi: '{name}' -> '{cleaned_name}'")
            cur.execute(
                "UPDATE courses SET name = %s WHERE id = %s",
                (cleaned_name, course_id)
            )
            updated_count += 1
    
    conn.commit()
    print(f"  [OK] {updated_count} ders adi duzeltildi.")
    return updated_count


def normalize_turkish_chars(text):
    replacements = {
        'i': 'i', 'I': 'i', 'g': 'g', 'G': 'g',
        'u': 'u', 'U': 'u', 's': 's', 'S': 's',
        'o': 'o', 'O': 'o', 'c': 'c', 'C': 'c',
        # Turkce ozel karakterler
        '\u0131': 'i',  # dotless i
        '\u0130': 'i',  # capital I with dot
        '\u011f': 'g',  # g with breve
        '\u011e': 'g',  # G with breve
        '\u00fc': 'u',  # u with diaeresis
        '\u00dc': 'u',  # U with diaeresis
        '\u015f': 's',  # s with cedilla
        '\u015e': 's',  # S with cedilla
        '\u00f6': 'o',  # o with diaeresis
        '\u00d6': 'o',  # O with diaeresis
        '\u00e7': 'c',  # c with cedilla
        '\u00c7': 'c',  # C with cedilla
    }
    result = text
    for tr_char, ascii_char in replacements.items():
        result = result.replace(tr_char, ascii_char)
    return result.lower()


def generate_email(first_name, last_name):
    first = normalize_turkish_chars(first_name.strip())
    last = normalize_turkish_chars(last_name.strip())
    first = re.sub(r'[^a-z]', '', first)
    last = re.sub(r'[^a-z]', '', last)
    return f"{first}.{last}@kstu.edu.tr"


def get_department_info(conn, department_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT d.id, d.name, d.code, f.id as faculty_id, f.name as faculty_name
        FROM departments d
        LEFT JOIN faculties f ON d.faculty_id = f.id
        WHERE d.id = %s
    """, (department_id,))
    return cur.fetchone()


def create_lecturer_for_course(conn, course_name, department_id):
    cur = conn.cursor()
    
    dept_info = get_department_info(conn, department_id)
    if not dept_info:
        print(f"    [UYARI] Bolum bulunamadi (ID: {department_id})")
        return None
    
    dept_id, dept_name, dept_code, faculty_id, faculty_name = dept_info
    

    course_words = course_name.split()
    if len(course_words) >= 2:
        first_name = course_words[0].capitalize()
        last_name = course_words[1].capitalize()
    else:
        first_name = course_words[0].capitalize() if course_words else "Ogretim"
        last_name = "Uyesi"
    
    titles = ["Prof. Dr.", "Doc. Dr.", "Dr. Ogr. Uyesi", "Ogr. Gor."]
    title_index = hash(course_name) % len(titles)
    title = titles[title_index]
    
    email = generate_email(first_name, last_name)
    
    cur.execute("SELECT id FROM lecturers WHERE email = %s", (email,))
    existing = cur.fetchone()
    counter = 1
    original_email = email
    while existing:
        email = original_email.replace('@', f'{counter}@')
        counter += 1
        cur.execute("SELECT id FROM lecturers WHERE email = %s", (email,))
        existing = cur.fetchone()
    
    available_days = ['Pazartesi', 'Sali', 'Carsamba', 'Persembe', 'Cuma']
    
    cur.execute("""
        INSERT INTO lecturers (department_id, first_name, last_name, title, email, available_days)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (department_id, first_name, last_name, title, email, available_days))
    
    lecturer_id = cur.fetchone()[0]
    conn.commit()
    
    print(f"    [OK] Yeni ogretim uyesi: {title} {first_name} {last_name} ({email})")
    return lecturer_id


def fix_courses_without_lecturers(conn):
    print("\n[OGRETIM UYELERI] Eksik dersler duzeltiliyor...")
    
    cur = conn.cursor()
    
    cur.execute("""
        SELECT c.id, c.code, c.name, c.department_id, d.name as dept_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        WHERE c.lecturer_id IS NULL
        ORDER BY c.department_id, c.code
    """)
    courses_without_lecturers = cur.fetchall()
    
    if not courses_without_lecturers:
        print("  [OK] Tum derslerin ogretim uyesi mevcut.")
        return 0
    
    print(f"  [INFO] {len(courses_without_lecturers)} ders icin ogretim uyesi atanacak...")
    
    created_count = 0
    assigned_count = 0
    
    current_dept = None
    dept_lecturers = []
    
    for course_id, code, name, department_id, dept_name in courses_without_lecturers:
        print(f"\n  [DERS] {code} - {name} ({dept_name or 'Bilinmeyen Bolum'})")
        
        if department_id != current_dept:
            current_dept = department_id
            cur.execute("""
                SELECT id, title, first_name, last_name
                FROM lecturers
                WHERE department_id = %s
                ORDER BY id
            """, (department_id,))
            dept_lecturers = cur.fetchall()
        
        if dept_lecturers:
            cur.execute("""
                SELECT l.id, COUNT(c.id) as course_count
                FROM lecturers l
                LEFT JOIN courses c ON c.lecturer_id = l.id
                WHERE l.department_id = %s
                GROUP BY l.id
                ORDER BY course_count ASC
                LIMIT 1
            """, (department_id,))
            result = cur.fetchone()
            
            if result:
                lecturer_id = result[0]
                cur.execute(
                    "UPDATE courses SET lecturer_id = %s WHERE id = %s",
                    (lecturer_id, course_id)
                )
                conn.commit()
                
                cur.execute(
                    "SELECT title, first_name, last_name FROM lecturers WHERE id = %s",
                    (lecturer_id,)
                )
                lec_info = cur.fetchone()
                if lec_info:
                    print(f"    [OK] Atandi: {lec_info[0]} {lec_info[1]} {lec_info[2]}")
                assigned_count += 1
                continue
        
        if department_id:
            lecturer_id = create_lecturer_for_course(conn, name, department_id)
            if lecturer_id:
                cur.execute(
                    "UPDATE courses SET lecturer_id = %s WHERE id = %s",
                    (lecturer_id, course_id)
                )
                conn.commit()
                created_count += 1
                assigned_count += 1
                
                cur.execute(
                    "SELECT id, title, first_name, last_name FROM lecturers WHERE id = %s",
                    (lecturer_id,)
                )
                new_lec = cur.fetchone()
                if new_lec:
                    dept_lecturers.append(new_lec)
        else:
            print(f"    [UYARI] Bolum atanmamis, ogretim uyesi olusturulamadi")
    
    print(f"\n  [SONUC] {created_count} yeni ogretim uyesi olusturuldu, {assigned_count} ders atandi.")
    return assigned_count


def show_current_status(conn):
    cur = conn.cursor()
    
    print("\n[DURUM] Mevcut Durum:")
    print("-" * 50)
    
    cur.execute("SELECT COUNT(*) FROM courses")
    total_courses = cur.fetchone()[0]
    print(f"  Toplam ders: {total_courses}")
    
    cur.execute("SELECT COUNT(*) FROM courses WHERE lecturer_id IS NULL")
    no_lecturer = cur.fetchone()[0]
    print(f"  Ogretim uyesi olmayan ders: {no_lecturer}")
    
    cur.execute("SELECT COUNT(*) FROM lecturers")
    total_lecturers = cur.fetchone()[0]
    print(f"  Toplam ogretim uyesi: {total_lecturers}")
    
    cur.execute("SELECT COUNT(*) FROM courses WHERE name ~ '\\d{3,}$'")
    with_numbers = cur.fetchone()[0]
    print(f"  Adinda rastgele sayi olan ders: {with_numbers}")
    
    print("-" * 50)


def main():
    print("=" * 60)
    print("DERS VERILERI DUZELTME SCRIPTI")
    print("=" * 60)
    
    try:
        conn = get_connection()
        print("[OK] Veritabanina baglandi.")
        
        show_current_status(conn)
        
        fix_course_names(conn)
        
        fix_courses_without_lecturers(conn)
        
        print("\n" + "=" * 60)
        show_current_status(conn)
        
        conn.close()
        print("\n[OK] Islem tamamlandi!")
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
