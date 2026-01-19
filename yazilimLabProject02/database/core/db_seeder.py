import psycopg2
import random
import hashlib
import unicodedata
import re
from faker import Faker

fake = Faker('tr_TR')

ACADEMIC_TITLES = [
    'Prof. Dr.',
    'Doç. Dr.',
    'Dr. Öğr. Üyesi',
    'Öğr. Gör. Dr.',
    'Öğr. Gör.',
    'Arş. Gör. Dr.',
    'Arş. Gör.'
]

COURSE_TYPES = ['Zorunlu', 'Alan Seçmeli', 'Üniversite Seçmeli', 'Proje']

EXAM_TYPES = ['Yazılı', 'Test', 'Uygulama', 'Sözlü', 'Proje', 'Ödev']

WEEKDAYS = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']

COURSE_NAMES = {
    'MUH': [
        'Programlamaya Giriş', 'Veri Yapıları ve Algoritmalar', 'Veritabanı Sistemleri',
        'İşletim Sistemleri', 'Bilgisayar Ağları', 'Yapay Zeka', 'Makine Öğrenmesi',
        'Yazılım Mühendisliğine Giriş', 'Grafik ve Görselleştirme', 'Mobil Uygulama Geliştirme',
        'Web Programlama', 'Bilgisayar Mimarisi', 'Algoritma Analizi', 'Otomata Teorisi',
        'Sayısal Analiz', 'Lineer Cebir', 'Ayrık Matematik', 'Olasılık ve İstatistik'
    ],
    'IIBF': [
        'Muhasebe', 'Finansal Yönetim', 'İktisada Giriş', 'Mikroekonomi', 'Makroekonomi',
        'İşletme Yönetimi', 'Pazarlama İlkeleri', 'Uluslararası Ticaret', 'İnsan Kaynakları Yönetimi',
        'Stratejik Yönetim', 'Ticaret Hukuku', 'Türk Vergi Sistemi', 'Bankacılık ve Finans',
        'Ulusal Ekonomi', 'Siyasi Tarih', 'Anayasa Hukuku', 'Kamu Yönetimi'
    ],
    'TIP': [
        'Anatomi', 'Fizyoloji', 'Biyokimya', 'Tıbbi Biyoloji', 'Tıp Etiği ve Deontoloji',
        'Histoloji ve Embriyoloji', 'Tıbbi Farmakoloji', 'Tıbbi Mikrobiyoloji',
        'Patoloji', 'İç Hastalıkları', 'Cerrahi', 'Kardiyoloji', 'Nöroloji',
        'Çocuk Sağlığı ve Hastalıkları', 'Kadın Hastalıkları ve Doğum'
    ]
}


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


def generate_course_code(dept_code: str, year: int, semester: int, course_num: int) -> str:
    return f"{dept_code}{year}{semester:02d}{course_num:02d}"


DB_PARAMS = {
    "host": "localhost",
    "database": "universite_sinav_db",
    "user": "postgres",
    "password": "123"
}


def connect():
    return psycopg2.connect(**DB_PARAMS)


def seed_users(cur, department_ids):
    cur.execute("SELECT id, code, name FROM departments ORDER BY id")
    departments = cur.fetchall()
    dept_map = {dept[0]: (dept[1], dept[2]) for dept in departments}  # {id: (code, name)}
    
    users = []
    
    users.append(('admin', hashlib.sha256('admin123'.encode()).hexdigest(),
                  'admin@kstu.edu.tr', 'Admin', 'User', 'admin', None))
    
    for dept_id in department_ids:
        if dept_id in dept_map:
            dept_code = dept_map[dept_id][0].lower()
            dept_name = dept_map[dept_id][1]
            username = f"yetkili_{dept_code}"
            email = f"yetkili.{dept_code}@kstu.edu.tr"
            users.append((username, hashlib.sha256('123456'.encode()).hexdigest(),
                         email, f'{dept_name} Yetkilisi', '', 'bolum_yetkilisi', dept_id))
    
    for dept_id in department_ids:
        if dept_id in dept_map:
            dept_code = dept_map[dept_id][0].lower()
            for i in range(1, 3):
                username = f"hoca_{dept_code}_{i}"
                email = f"hoca.{dept_code}{i}@kstu.edu.tr"
                users.append((username, hashlib.sha256('123456'.encode()).hexdigest(),
                             email, f'{dept_code.upper()} Hoca {i}', '', 'hoca', dept_id))
    
    for dept_id in department_ids:
        if dept_id in dept_map:
            dept_code = dept_map[dept_id][0].lower()
            for i in range(1, 3):
                username = f"ogrenci_{dept_code}_{i}"
                email = f"ogrenci.{dept_code}{i}@kstu.edu.tr"
                users.append((username, hashlib.sha256('123456'.encode()).hexdigest(),
                             email, f'{dept_code.upper()} Öğrenci {i}', '', 'ogrenci', dept_id))
    
    for username, password_hash, email, first_name, last_name, role, dept_id in users:
        cur.execute("""
            INSERT INTO users (username, password_hash, email, first_name, last_name, role, department_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, (username, password_hash, email, first_name, last_name, role, dept_id))
    
    print(f"✓ {len(users)} kullanıcı eklendi")
    print("   Kullanıcı bilgileri:")
    print("   - admin: admin / admin123 (Tüm sistem yönetimi)")
    for dept_id in department_ids:
        if dept_id in dept_map:
            dept_code = dept_map[dept_id][0].lower()
            dept_name = dept_map[dept_id][1]
            print(f"   - yetkili_{dept_code}: {dept_name} Bölüm Yetkilisi (şifre: 123456)")
            print(f"   - hoca_{dept_code}_1, hoca_{dept_code}_2: {dept_name} Hocaları (şifre: 123456)")
            print(f"   - ogrenci_{dept_code}_1, ogrenci_{dept_code}_2: {dept_name} Öğrencileri (şifre: 123456)")


def seed_database():
    conn = connect()
    cursor = conn.cursor()

    print("🌱 Veri üretimi başlıyor...")

    print("🗑️ Mevcut veriler temizleniyor...")
    cursor.execute("""
        TRUNCATE TABLE exam_schedule, courses, lecturers, departments, faculties, classrooms, users
        RESTART IDENTITY CASCADE
    """)

    faculties_data = [
        ("Mühendislik Fakültesi", "MUH", "Prof. Dr. Ahmet Kaya"),
        ("İktisadi ve İdari Bilimler Fakültesi", "IIBF", "Prof. Dr. Hasan Şahin"),
        ("Tıp Fakültesi", "TIP", "Prof. Dr. Mustafa Eren"),
    ]
    
    departments_data = [
        ("Bilgisayar Mühendisliği", "BM", "Prof. Dr. Ayşe Yılmaz", "MUH"),
        ("Yazılım Mühendisliği", "YM", "Doç. Dr. Mehmet Demir", "MUH"),
        ("Endüstri Mühendisliği", "EM", "Dr. Öğr. Üyesi Fatma Çelik", "MUH"),
        
        ("İşletme", "ISL", "Prof. Dr. Ali Vural", "IIBF"),
        ("İktisat", "IKT", "Doç. Dr. Zeynep Aksoy", "IIBF"),
        ("Uluslararası İlişkiler", "ULI", "Dr. Öğr. Üyesi Burak Yıldız", "IIBF"),
        
        ("Temel Tıp Bilimleri", "TTB", "Prof. Dr. Kemal Öztürk", "TIP"),
    ]

    department_ids = {}
    faculty_ids = {} 
    
    print("... Fakülteler ekleniyor")
    for faculty_name, faculty_code, dean_name in faculties_data:
        cursor.execute(
            "INSERT INTO faculties (name, code, dean_name) VALUES (%s, %s, %s) RETURNING id",
            (faculty_name, faculty_code, dean_name)
        )
        faculty_id = cursor.fetchone()[0]
        faculty_ids[faculty_code] = faculty_id
    
    print("... Bölümler ekleniyor")
    for dept_name, dept_code, head_name, faculty_code in departments_data:
        faculty_id = faculty_ids[faculty_code]
        cursor.execute(
            "INSERT INTO departments (name, code, head_name, faculty_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (dept_name, dept_code, head_name, faculty_id)
        )
        department_ids[dept_code] = cursor.fetchone()[0]

    classrooms = []
    print("... Derslikler ekleniyor")
    
    for faculty_code, faculty_id in faculty_ids.items():
        for i in range(1, 8):
            name = f"{faculty_code}-D{i:02d}"
            capacity = random.choice([30, 40, 50, 60, 80, 100, 150])
            has_computer = random.choice([True, False]) if faculty_code == 'MUH' else False  # Mühendislikte daha fazla
            is_suitable = random.choice([True, True, True, False])  # %75 oranında uygun
            
            cursor.execute(
                """INSERT INTO classrooms (name, building, capacity, floor, has_projector, has_computer, is_active, is_suitable, faculty_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (name, f"{faculty_code} Blok", capacity, random.randint(1, 4),
                 random.choice([True, False]), has_computer, True, is_suitable, faculty_id)
            )
            classrooms.append(cursor.fetchone()[0])

    # --- 3. ÖĞRETİM ÜYELERİNİ OLUŞTUR ---
    lecturer_ids = []
    used_emails = set()
    print("... Öğretim Üyeleri ekleniyor")
    
    for dept_code, dept_id in department_ids.items():
        dean_title = 'Prof. Dr.'
        if dept_code == 'BM':
            first_name, last_name = 'Ayşe', 'Yılmaz'
        elif dept_code == 'YM':
            first_name, last_name = 'Mehmet', 'Demir'
        elif dept_code == 'EM':
            first_name, last_name = 'Fatma', 'Çelik'
        elif dept_code == 'ISL':
            first_name, last_name = 'Ali', 'Vural'
        elif dept_code == 'IKT':
            first_name, last_name = 'Zeynep', 'Aksoy'
        elif dept_code == 'ULI':
            first_name, last_name = 'Burak', 'Yıldız'
        elif dept_code == 'TTB':
            first_name, last_name = 'Kemal', 'Öztürk'
        else:
            first_name, last_name = fake.first_name(), fake.last_name()
            dean_title = random.choice(ACADEMIC_TITLES)
        
        email = generate_email(first_name, last_name)
        used_emails.add(email)
        available_days = random.sample(WEEKDAYS, k=random.randint(3, 5))
        
        cursor.execute(
            """INSERT INTO lecturers (department_id, first_name, last_name, title, email, available_days)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
            (dept_id, first_name, last_name, dean_title, email, available_days)
        )
        lecturer_ids.append(cursor.fetchone()[0])
        
        num_lecturers = random.randint(3, 5)
        for _ in range(num_lecturers):
            first_name = fake.first_name()
            last_name = fake.last_name()
            title = random.choice(ACADEMIC_TITLES)
            
            email = generate_email(first_name, last_name)
            base_email = email
            counter = 1
            while email in used_emails:
                email = base_email.replace('@', f'{counter}@')
                counter += 1
            used_emails.add(email)
            
            available_days = random.sample(WEEKDAYS, k=random.randint(3, 5))
            
            cursor.execute(
                """INSERT INTO lecturers (department_id, name, first_name, last_name, title, email, available_days)
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (dept_id, f"{first_name} {last_name}", first_name, last_name, title, email, available_days)
            )
            lecturer_ids.append(cursor.fetchone()[0])

    # --- 4. DERSLERİ OLUŞTUR ---
    print("... Dersler ekleniyor")
    course_count = 0
    
    for dept_code, dept_id in department_ids.items():
        faculty_code = None
        for fcode, fid in faculty_ids.items():
            if any(d[2] == fcode for d in departments_data if d[1] == dept_code):
                faculty_code = fcode
                break
        
        if faculty_code and faculty_code in COURSE_NAMES:
            course_names = COURSE_NAMES[faculty_code]
            num_courses = random.randint(6, 10)
            
            course_code_counter = {}
            
            for i in range(num_courses):
                course_name = random.choice(course_names)
                
                year = random.randint(1, 4)
                semester = random.randint(1, 2)
                
                key = f"{dept_code}{year}{semester}"
                course_code_counter[key] = course_code_counter.get(key, 0) + 1
                course_code = generate_course_code(dept_code, year, semester, course_code_counter[key])
                
                credit = random.choice([2, 3, 4, 5, 6])
                theory_hours = random.choice([2, 3, 4])
                lab_hours = random.choice([0, 0, 1, 2])  
                
                if year == 4:
                    course_type = random.choice(['Zorunlu', 'Proje'])
                else:
                    course_type = random.choice(COURSE_TYPES)
                
                student_count = random.randint(20, 120)
                
                if course_type == 'Proje':
                    has_exam = False
                    exam_type = 'Proje'
                    exam_duration = 0
                else:
                    has_exam = True
                    exam_type = random.choice(['Yazılı', 'Yazılı', 'Test', 'Uygulama'])  # Yazılı daha fazla
                    if exam_type == 'Test':
                        exam_duration = random.choice([30, 60])
                    else:
                        exam_duration = random.choice([60, 90, 120])
                
                lecturer_id = random.choice(lecturer_ids)
                
                lecturer_count = 1 if course_type != 'Proje' else random.randint(1, 3)
                
                cursor.execute("""
                    INSERT INTO courses (
                        name, lecturer_id, student_count, exam_duration, exam_type,
                        department_id, code, year, semester, period,
                        theory_hours, lab_hours, course_type, description,
                        lecturer_count, has_exam, credit, is_active
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (code) DO NOTHING
                """, (
                    course_name, lecturer_id, student_count, exam_duration, exam_type,
                    dept_id, course_code, year, semester, period,
                    theory_hours, lab_hours, course_type, f"{course_name} açıklaması",
                    lecturer_count, has_exam, credit, True
                ))
                course_count += 1

    # --- 5. KULLANICILARI OLUŞTUR ---
    print("... Kullanıcılar ekleniyor")
    seed_users(cursor, list(department_ids.values()))

    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n✅ Veritabanı başarıyla dolduruldu!")
    print(f"\n📊 Eklenen Veri Özeti:")
    print(f"  - Fakülteler: {len(faculty_ids)}")
    print(f"  - Bölümler: {len(department_ids)}")
    print(f"  - Derslikler: {len(classrooms)}")
    print(f"  - Öğretim Üyeleri: {len(lecturer_ids)}")
    print(f"  - Dersler: {course_count}")


if __name__ == "__main__":
    seed_database()