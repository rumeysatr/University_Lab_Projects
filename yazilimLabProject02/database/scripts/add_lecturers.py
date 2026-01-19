"""
Öğretim üyelerini lecturers tablosuna ekleyen migration scripti
"""

import psycopg2
import re


def normalize_turkish_chars(text: str) -> str:
    replacements = {
        'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ş': 's', 'Ş': 'S',
        'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
    }
    for tr_char, ascii_char in replacements.items():
        text = text.replace(tr_char, ascii_char)
    return text.lower()


def generate_email(first_name: str, last_name: str) -> str:
    first = normalize_turkish_chars(first_name.strip())
    last = normalize_turkish_chars(last_name.strip())
    first = re.sub(r'[^a-z]', '', first)
    last = re.sub(r'[^a-z]', '', last)
    return f"{first}.{last}@kstu.edu.tr"


DB_PARAMS = {
    "host": "localhost",
    "database": "universite_sinav_db",
    "user": "postgres",
    "password": "123"
}


def connect():
    return psycopg2.connect(**DB_PARAMS)


def add_lecturers():
    conn = connect()
    cursor = conn.cursor()
    
    print("[INFO] Ogretim uyeleri ekleniyor...")
    
    cursor.execute("SELECT id, name FROM departments")
    departments = cursor.fetchall()
    dept_map = {dept[1]: dept[0] for dept in departments} 
    
    print(f"Mevcut bölümler: {list(dept_map.keys())}")
    
    if "Ortak Dersler" not in dept_map:
        cursor.execute("SELECT id FROM faculties WHERE code = 'MUH'")
        result = cursor.fetchone()
        if result:
            muh_faculty_id = result[0]
            cursor.execute("""
                INSERT INTO departments (name, code, head_name, faculty_id)
                VALUES ('Ortak Dersler', 'OD', 'Dr. Öğr. Üyesi Murat Can', %s)
                RETURNING id
            """, (muh_faculty_id,))
            ortak_dersler_id = cursor.fetchone()[0]
            dept_map["Ortak Dersler"] = ortak_dersler_id
            print(f"[OK] 'Ortak Dersler' bolumu olusturuldu (ID: {ortak_dersler_id})")
    

    lecturers_data = [
        ("Prof. Dr.", "Ahmet", "Yilmaz", "Bilgisayar Muhendisligi", ["Pazartesi", "Sali", "Carsamba"]),
        ("Doc. Dr.", "Ayse", "Kaya", "Bilgisayar Muhendisligi", ["Sali", "Persembe", "Cuma"]),
        ("Dr. Ogr. Uyesi", "Mehmet", "Demir", "Bilgisayar Muhendisligi", ["Pazartesi", "Carsamba"]),
        ("Ars. Gor.", "Selin", "Ozturk", "Bilgisayar Muhendisligi", ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]),
        ("Prof. Dr.", "Fatma", "Celik", "Yazilim Muhendisligi", ["Carsamba", "Persembe"]),
        ("Doc. Dr.", "Ali", "Vural", "Yazilim Muhendisligi", ["Pazartesi", "Sali"]),
        ("Dr. Ogr. Uyesi", "Burak", "Yildiz", "Yazilim Muhendisligi", ["Sali", "Cuma"]),
        ("Ogr. Gor.", "Canan", "Kara", "Yazilim Muhendisligi", ["Pazartesi", "Persembe"]),
        ("Prof. Dr.", "Zeynep", "Aksoy", "Endustri Muhendisligi", ["Pazartesi", "Sali", "Carsamba"]),
        ("Dr. Ogr. Uyesi", "Mustafa", "Sahin", "Endustri Muhendisligi", ["Persembe", "Cuma"]),
        ("Doc. Dr.", "Kemal", "Ozturk", "Endustri Muhendisligi", ["Pazartesi", "Carsamba"]),
        ("Dr. Ogr. Uyesi", "Leyla", "Sonmez", "Bilgisayar Muhendisligi", ["Sali", "Persembe"]),
        ("Prof. Dr.", "Hasan", "Yurt", "Yazilim Muhendisligi", ["Cuma"]),
        ("Ars. Gor.", "Elif", "Demir", "Endustri Muhendisligi", ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]),
        ("Dr. Ogr. Uyesi", "Murat", "Can", "Ortak Dersler", ["Carsamba", "Cuma"]),
    ]
    
    added_count = 0
    for title, first_name, last_name, dept_name, available_days in lecturers_data:
        dept_id = dept_map.get(dept_name)
        if dept_id is None:
            print(f"[WARN] Bolum bulunamadi: {dept_name} - {title} {first_name} {last_name} atlaniyor")
            continue
        
        email = generate_email(first_name, last_name)
        
        cursor.execute("SELECT id FROM lecturers WHERE email = %s", (email,))
        if cursor.fetchone():
            counter = 1
            base_email = email
            while True:
                email = base_email.replace('@', f'{counter}@')
                cursor.execute("SELECT id FROM lecturers WHERE email = %s", (email,))
                if not cursor.fetchone():
                    break
                counter += 1
        
        cursor.execute("""
            INSERT INTO lecturers (department_id, first_name, last_name, title, email, available_days)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (dept_id, first_name, last_name, title, email, available_days))
        
        lecturer_id = cursor.fetchone()[0]
        added_count += 1
        print(f"[OK] {title} {first_name} {last_name} eklendi (ID: {lecturer_id}, Bolum: {dept_name}, Email: {email})")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n[DONE] Toplam {added_count} ogretim uyesi basariyla eklendi!")


if __name__ == "__main__":
    add_lecturers()
