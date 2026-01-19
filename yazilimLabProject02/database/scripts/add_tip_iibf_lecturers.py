"""
Yeni ogretim uyelerini lecturers tablosuna ekleyen migration scripti
Tip Fakultesi, IIBF ve diger bolumlere yeni hocalar ekler
"""

import psycopg2
import re


def normalize_turkish_chars(text: str) -> str:
    replacements = {
        'i': 'i', 'I': 'I', 'g': 'g', 'G': 'G',
        'u': 'u', 'U': 'U', 's': 's', 'S': 'S',
        'o': 'o', 'O': 'O', 'c': 'c', 'C': 'C',
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


def add_tip_and_iibf_lecturers():
    conn = connect()
    cursor = conn.cursor()
    
    print("[INFO] Yeni ogretim uyeleri ekleniyor...")
    
    # Bolum ID'lerini al
    cursor.execute("SELECT id, name FROM departments")
    departments = cursor.fetchall()
    dept_map = {dept[1]: dept[0] for dept in departments}  # {name: id}
    
    # Fakulte ID'lerini al
    cursor.execute("SELECT id, name FROM faculties")
    faculties = cursor.fetchall()
    faculty_map = {fac[1]: fac[0] for fac in faculties}
    
    print(f"Mevcut bolumler: {list(dept_map.keys())}")
    print(f"Mevcut fakulteler: {list(faculty_map.keys())}")
    
    # Tip Fakultesi ID'sini bul
    tip_faculty_id = None
    for name, fid in faculty_map.items():
        if 'Tip' in name or 'TIP' in name:
            tip_faculty_id = fid
            break
    
    if tip_faculty_id is None:
        print("[ERROR] Tip Fakultesi bulunamadi!")
        return
    
    # IIBF ID'sini bul
    iibf_faculty_id = None
    for name, fid in faculty_map.items():
        if 'Iktisadi' in name or 'IIBF' in name or 'Idari' in name:
            iibf_faculty_id = fid
            break
    
    if iibf_faculty_id is None:
        print("[ERROR] IIBF bulunamadi!")
        return
    
    # Cerrahi Tip Bilimleri bolumu yoksa olustur
    cerrahi_bolum_id = None
    for name, did in dept_map.items():
        if 'Cerrahi' in name:
            cerrahi_bolum_id = did
            break
    
    if cerrahi_bolum_id is None:
        cursor.execute("""
            INSERT INTO departments (name, code, head_name, faculty_id)
            VALUES ('Cerrahi Tip Bilimleri', 'CTB', 'Prof. Dr. Kemal Yondem', %s)
            RETURNING id
        """, (tip_faculty_id,))
        cerrahi_bolum_id = cursor.fetchone()[0]
        dept_map["Cerrahi Tip Bilimleri"] = cerrahi_bolum_id
        print(f"[OK] 'Cerrahi Tip Bilimleri' bolumu olusturuldu (ID: {cerrahi_bolum_id})")
    
    # Siyaset Bilimi ve Kamu Yonetimi bolumu yoksa olustur
    siyaset_bolum_id = None
    for name, did in dept_map.items():
        if 'Siyaset' in name or 'Kamu' in name:
            siyaset_bolum_id = did
            break
    
    if siyaset_bolum_id is None:
        cursor.execute("""
            INSERT INTO departments (name, code, head_name, faculty_id)
            VALUES ('Siyaset Bilimi ve Kamu Yonetimi', 'SBKY', 'Prof. Dr. Yucem Aydin', %s)
            RETURNING id
        """, (iibf_faculty_id,))
        siyaset_bolum_id = cursor.fetchone()[0]
        dept_map["Siyaset Bilimi ve Kamu Yonetimi"] = siyaset_bolum_id
        print(f"[OK] 'Siyaset Bilimi ve Kamu Yonetimi' bolumu olusturuldu (ID: {siyaset_bolum_id})")
    
    # Tip Fakultesi icin ozel bolum ID'si bul (Temel Tip Bilimleri)
    tip_bolum_id = None
    for name, did in dept_map.items():
        if 'Temel Tip' in name or 'TTB' in name:
            tip_bolum_id = did
            break
    
    # Isletme bolum ID'si
    isletme_bolum_id = None
    for name, did in dept_map.items():
        if 'Isletme' in name or 'ISL' in name:
            isletme_bolum_id = did
            break
    
    # Iktisat bolum ID'si
    iktisat_bolum_id = None
    for name, did in dept_map.items():
        if 'Iktisat' in name or 'IKT' in name:
            iktisat_bolum_id = did
            break
    
    # Uluslararasi Iliskiler bolum ID'si
    uli_bolum_id = None
    for name, did in dept_map.items():
        if 'Uluslararasi' in name or 'ULI' in name:
            uli_bolum_id = did
            break
    
    # Eklenecek ogretim uyeleri listesi
    # (title, first_name, last_name, department_id, available_days)
    lecturers_data = [
        # Tip Fakultesi hocalari - Temel Tip Bilimleri'ne atayalim
        ("Prof. Dr.", "Ilknur", "Adali", tip_bolum_id, ["Pazartesi", "Carsamba", "Cuma"]),
        ("Doc. Dr.", "Mehmet", "Ozdemir", tip_bolum_id, ["Sali", "Persembe"]),
        ("Dr. Ogr. Uyesi", "Ayse", "Yilmaz", tip_bolum_id, ["Pazartesi", "Sali", "Carsamba"]),
        ("Prof. Dr.", "Osman", "Ak", tip_bolum_id, ["Persembe", "Cuma"]),
        ("Ars. Gor.", "Elif", "Tutar", tip_bolum_id, ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]),
        
        # Cerrahi Tip Bilimleri
        ("Prof. Dr.", "Kemal", "Yondem", cerrahi_bolum_id, ["Carsamba", "Cuma"]),
        
        # Uluslararasi Iliskiler
        ("Prof. Dr.", "Ilker", "Yerturk", uli_bolum_id, ["Sali", "Carsamba"]),
        ("Ars. Gor.", "Ahmet", "Vural", uli_bolum_id, ["Sali", "Persembe"]),
        
        # Iktisat
        ("Doc. Dr.", "Muhammet", "Ozyaprak", iktisat_bolum_id, ["Pazartesi", "Persembe"]),
        ("Dr. Ogr. Uyesi", "Tuna", "Basar", iktisat_bolum_id, ["Carsamba", "Cuma"]),
        ("Doc. Dr.", "Derya", "Acar", iktisat_bolum_id, ["Pazartesi", "Sali", "Carsamba"]),
        ("Dr. Ogr. Uyesi", "Selin", "Uysal", iktisat_bolum_id, ["Pazartesi", "Carsamba"]),
        
        # Siyaset Bilimi ve Kamu Yonetimi
        ("Prof. Dr.", "Yucem", "Aydin", siyaset_bolum_id, ["Pazartesi", "Sali"]),
        
        # Isletme
        ("Dr. Ogr. Uyesi", "Emre", "Akin", isletme_bolum_id, ["Sali", "Persembe", "Cuma"]),
        ("Ars. Gor.", "Burak", "Sodali", isletme_bolum_id, ["Pazartesi", "Carsamba", "Cuma"]),
    ]
    
    added_count = 0
    for title, first_name, last_name, dept_id, available_days in lecturers_data:
        if dept_id is None:
            print(f"[WARN] Bolum ID bulunamadi: {title} {first_name} {last_name} atlaniyor")
            continue
        
        email = generate_email(first_name, last_name)
        
        # Email benzersizligini kontrol et
        cursor.execute("SELECT id FROM lecturers WHERE email = %s", (email,))
        if cursor.fetchone():
            # Email varsa numara ekle
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
        print(f"[OK] {title} {first_name} {last_name} eklendi (ID: {lecturer_id}, Email: {email})")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n[DONE] Toplam {added_count} ogretim uyesi basariyla eklendi!")


if __name__ == "__main__":
    add_tip_and_iibf_lecturers()
