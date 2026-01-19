"""
Ders tablosuna tum dersleri ekleyen migration scripti
Mock data kullanilmadan gercek ders bilgileri eklenir

Dersler:
- Bilgisayar Muhendisligi (BLM)
- Yazilim Muhendisligi (YAZ)
- Endustri Muhendisligi (END)
- Ortak Zorunlu Dersler (MATH, PHYS, TURK, HIST, ENG)
- Tip Fakultesi (TIP)
- IIBF: Isletme (BUS), Iktisat (ECON), Uluslararasi Iliskiler (INT)
"""

import psycopg2
import random

DB_PARAMS = {
    "host": "localhost",
    "database": "universite_sinav_db",
    "user": "postgres",
    "password": "123"
}


def connect():
    return psycopg2.connect(**DB_PARAMS)


def add_all_courses():
    conn = connect()
    cursor = conn.cursor()
    
    print("[INFO] Tum dersler ekleniyor...")
    
    cursor.execute("SELECT id, name, code FROM departments")
    departments = cursor.fetchall()
    dept_map = {}
    dept_code_map = {}
    for dept in departments:
        dept_map[dept[1]] = dept[0]
        if dept[2]:
            dept_code_map[dept[2]] = dept[0]
    
    print(f"Mevcut bolumler: {list(dept_map.keys())}")
    
    cursor.execute("""
        SELECT l.id, l.department_id, l.title, l.first_name, l.last_name, d.name as dept_name
        FROM lecturers l
        LEFT JOIN departments d ON l.department_id = d.id
    """)
    lecturers = cursor.fetchall()
    
    dept_lecturers = {}
    for lec in lecturers:
        dept_id = lec[1]
        if dept_id not in dept_lecturers:
            dept_lecturers[dept_id] = []
        dept_lecturers[dept_id].append({
            'id': lec[0],
            'title': lec[2],
            'first_name': lec[3],
            'last_name': lec[4],
            'dept_name': lec[5]
        })
    
    print(f"Toplam ogretim uyesi: {len(lecturers)}")
    for dept_id, lecs in dept_lecturers.items():
        if lecs:
            print(f"  - {lecs[0]['dept_name']}: {len(lecs)} hoca")
    
    def get_dept_id(dept_name_pattern):
        for name, did in dept_map.items():
            if dept_name_pattern.lower() in name.lower():
                return did
        return None
    
    blm_dept_id = get_dept_id("Bilgisayar")
    yaz_dept_id = get_dept_id("Yazilim")
    end_dept_id = get_dept_id("Endustri")
    ortak_dept_id = get_dept_id("Ortak")
    tip_dept_id = get_dept_id("Temel Tip")
    isletme_dept_id = get_dept_id("Isletme")
    iktisat_dept_id = get_dept_id("Iktisat")
    uli_dept_id = get_dept_id("Uluslararasi")
    
    if ortak_dept_id is None:
        cursor.execute("""
            SELECT f.id FROM faculties f
            JOIN departments d ON d.faculty_id = f.id
            WHERE d.id = %s
        """, (blm_dept_id,))
        result = cursor.fetchone()
        if result:
            muh_faculty_id = result[0]
            cursor.execute("""
                INSERT INTO departments (name, code, head_name, faculty_id)
                VALUES ('Ortak Dersler', 'OD', 'Dr. Ogr. Uyesi Murat Can', %s)
                RETURNING id
            """, (muh_faculty_id,))
            ortak_dept_id = cursor.fetchone()[0]
            dept_map["Ortak Dersler"] = ortak_dept_id
            print(f"[OK] 'Ortak Dersler' bolumu olusturuldu (ID: {ortak_dept_id})")
    
    def get_random_lecturer(dept_id):
        """Bolumden rastgele bir hoca sec"""
        if dept_id and dept_id in dept_lecturers and len(dept_lecturers[dept_id]) > 0:
            return random.choice(dept_lecturers[dept_id])['id']
        return None
    
    def get_lecturer_for_dept(dept_id, index=0):
        """Bolumden sirali hoca sec"""
        if dept_id and dept_id in dept_lecturers and len(dept_lecturers[dept_id]) > 0:
            idx = index % len(dept_lecturers[dept_id])
            return dept_lecturers[dept_id][idx]['id']
        return None
    
    
    courses_data = []
    
    # ============================================
    # BILGISAYAR MUHENDISLIGI DERSLERI (BLM)
    # ============================================
    
    # 1. Sinif 1. Donem
    courses_data.extend([
        ("BLM101", "Algoritma ve Programlamaya Giris", blm_dept_id, 1, 1, 4, "Yazili", 90, "Zorunlu", True, 120, 3, 2),
        ("BLM103", "Bilgisayar Muhendisligine Giris", blm_dept_id, 1, 1, 3, "Test", 60, "Zorunlu", True, 120, 2, 0),
    ])
    
    # 1. Sinif 2. Donem
    courses_data.extend([
        ("BLM102", "Nesne Yonelimli Programlama", blm_dept_id, 1, 2, 4, "Yazili", 90, "Zorunlu", True, 110, 3, 2),
    ])
    
    # 2. Sinif 3. Donem
    courses_data.extend([
        ("BLM201", "Veri Yapilari", blm_dept_id, 2, 3, 4, "Yazili", 90, "Zorunlu", True, 100, 3, 2),
        ("BLM203", "Mantik Devreleri", blm_dept_id, 2, 3, 3, "Yazili", 60, "Zorunlu", True, 100, 2, 2),
    ])
    
    # 2. Sinif 4. Donem
    courses_data.extend([
        ("BLM202", "Veritabani Yonetim Sistemleri", blm_dept_id, 2, 4, 4, "Yazili", 90, "Zorunlu", True, 95, 3, 2),
        ("BLM204", "Programlama Dilleri Prensipleri", blm_dept_id, 2, 4, 3, "Test", 60, "Zorunlu", True, 95, 3, 0),
    ])
    
    # 3. Sinif 5. Donem
    courses_data.extend([
        ("BLM301", "Isletim Sistemleri", blm_dept_id, 3, 5, 4, "Yazili", 90, "Zorunlu", True, 85, 3, 2),
        ("BLM303", "Algoritma Analizi", blm_dept_id, 3, 5, 3, "Yazili", 60, "Zorunlu", True, 85, 3, 0),
    ])
    
    # 3. Sinif 6. Donem
    courses_data.extend([
        ("BLM302", "Bilgisayar Aglari", blm_dept_id, 3, 6, 4, "Yazili", 90, "Zorunlu", True, 80, 3, 2),
        ("BLM304", "Otomata Teorisi", blm_dept_id, 3, 6, 3, "Yazili", 60, "Zorunlu", True, 80, 3, 0),
    ])
    
    # 4. Sinif 7. Donem
    courses_data.extend([
        ("BLM401", "Bitirme Projesi I", blm_dept_id, 4, 7, 4, "Proje", 0, "Proje", False, 70, 0, 4),
        ("BLM405", "Yapay Zeka", blm_dept_id, 4, 7, 3, "Yazili", 90, "Alan Secmeli", True, 45, 3, 0),
        ("BLM407", "Siber Guvenlik", blm_dept_id, 4, 7, 3, "Yazili", 90, "Alan Secmeli", True, 40, 3, 0),
    ])
    
    # ============================================
    # YAZILIM MUHENDISLIGI DERSLERI (YAZ)
    # ============================================
    
    # 1. Sinif 1. Donem
    courses_data.extend([
        ("YAZ101", "Yazilim Muhendisligi Temelleri", yaz_dept_id, 1, 1, 3, "Test", 60, "Zorunlu", True, 100, 3, 0),
    ])
    
    # 1. Sinif 2. Donem
    courses_data.extend([
        ("YAZ104", "Ileri Programlama Teknikleri", yaz_dept_id, 1, 2, 4, "Yazili", 90, "Zorunlu", True, 95, 3, 2),
    ])
    
    # 2. Sinif 3. Donem
    courses_data.extend([
        ("YAZ201", "Yazilim Gereksinim Analizi", yaz_dept_id, 2, 3, 3, "Yazili", 60, "Zorunlu", True, 85, 3, 0),
        ("YAZ203", "Insan Bilgisayar Etkilesimi", yaz_dept_id, 2, 3, 3, "Test", 60, "Zorunlu", True, 85, 2, 2),
    ])
    
    # 2. Sinif 4. Donem
    courses_data.extend([
        ("YAZ204", "Yazilim Dogrulama ve Test", yaz_dept_id, 2, 4, 3, "Yazili", 60, "Zorunlu", True, 80, 2, 2),
    ])
    
    # 3. Sinif 5. Donem
    courses_data.extend([
        ("YAZ301", "Yazilim Mimarisi ve Tasarimi", yaz_dept_id, 3, 5, 4, "Yazili", 90, "Zorunlu", True, 75, 3, 2),
    ])
    
    # 3. Sinif 6. Donem
    courses_data.extend([
        ("YAZ305", "Web Uygulama Gelistirme", yaz_dept_id, 3, 6, 4, "Uygulama", 90, "Zorunlu", True, 70, 2, 4),
        ("YAZ306", "Mobil Uygulama Gelistirme", yaz_dept_id, 3, 6, 4, "Uygulama", 90, "Zorunlu", True, 65, 2, 4),
    ])
    
    # 4. Sinif 7. Donem
    courses_data.extend([
        ("YAZ401", "Yazilim Proje Yonetimi", yaz_dept_id, 4, 7, 3, "Yazili", 60, "Zorunlu", True, 60, 3, 0),
    ])
    
    # 4. Sinif 8. Donem
    courses_data.extend([
        ("YAZ404", "Veri Madenciligi", yaz_dept_id, 4, 8, 3, "Yazili", 90, "Alan Secmeli", True, 35, 3, 0),
    ])
    
    # ============================================
    # ENDUSTRI MUHENDISLIGI DERSLERI (END)
    # ============================================
    
    # 1. Sinif 1. Donem
    courses_data.extend([
        ("END101", "Endustri Muhendisligine Giris", end_dept_id, 1, 1, 3, "Test", 60, "Zorunlu", True, 90, 3, 0),
    ])
    
    # 2. Sinif 3. Donem
    courses_data.extend([
        ("END201", "Yoneylem Arastirmasi I", end_dept_id, 2, 3, 4, "Yazili", 90, "Zorunlu", True, 80, 3, 2),
        ("END202", "Istatistik ve Olasilik", end_dept_id, 2, 4, 4, "Yazili", 90, "Zorunlu", True, 80, 3, 2),
    ])
    
    # 3. Sinif 5. Donem
    courses_data.extend([
        ("END301", "Uretim Planlama ve Kontrol", end_dept_id, 3, 5, 4, "Yazili", 90, "Zorunlu", True, 70, 3, 2),
        ("END304", "Ergonomi", end_dept_id, 3, 6, 3, "Test", 60, "Zorunlu", True, 70, 3, 0),
    ])
    
    # 4. Sinif 7. Donem
    courses_data.extend([
        ("END401", "Tedarik Zinciri Yonetimi", end_dept_id, 4, 7, 3, "Yazili", 60, "Zorunlu", True, 55, 3, 0),
    ])
    
    # ============================================
    # ORTAK ZORUNLU DERSLER (Tum Muhendislikler)
    # ============================================
    
    # 1. Sinif 1. Donem
    courses_data.extend([
        ("MATH101", "Matematik I", ortak_dept_id, 1, 1, 4, "Yazili", 90, "Zorunlu", True, 300, 4, 0),
        ("PHYS101", "Fizik I", ortak_dept_id, 1, 1, 4, "Yazili", 90, "Zorunlu", True, 300, 3, 2),
        ("TURK101", "Turk Dili I", ortak_dept_id, 1, 1, 2, "Test", 60, "Zorunlu", True, 300, 2, 0),
        ("HIST101", "Ataturk Ilkeleri ve Inkilap Tarihi I", ortak_dept_id, 1, 1, 2, "Test", 60, "Zorunlu", True, 300, 2, 0),
        ("ENG101", "Academic English I", ortak_dept_id, 1, 1, 3, "Yazili", 60, "Zorunlu", True, 300, 3, 0),
    ])
    
    # 1. Sinif 2. Donem
    courses_data.extend([
        ("MATH102", "Matematik II", ortak_dept_id, 1, 2, 4, "Yazili", 90, "Zorunlu", True, 280, 4, 0),
        ("PHYS102", "Fizik II", ortak_dept_id, 1, 2, 4, "Yazili", 90, "Zorunlu", True, 280, 3, 2),
    ])
    
    # ============================================
    # TIP FAKULTESI DERSLERI (TIP)
    # ============================================
    
    courses_data.extend([
        ("TIP101", "Tibbi Biyoloji ve Genetik", tip_dept_id, 1, 1, 5, "Yazili", 90, "Zorunlu", True, 150, 4, 2),
        ("TIP103", "Anatomi I", tip_dept_id, 1, 1, 6, "Yazili", 120, "Zorunlu", True, 150, 4, 4),
        ("TIP201", "Fizyoloji", tip_dept_id, 2, 3, 5, "Yazili", 90, "Zorunlu", True, 140, 4, 2),
        ("TIP305", "Patoloji", tip_dept_id, 3, 5, 4, "Yazili", 90, "Zorunlu", True, 130, 3, 2),
        ("TIP402", "Dahiliye Staji", tip_dept_id, 4, 7, 6, "Sozlu", 30, "Zorunlu", True, 120, 0, 8),
    ])
    
    # ============================================
    # IIBF - ISLETME DERSLERI (BUS)
    # ============================================
    
    courses_data.extend([
        ("BUS101", "Isletmeye Giris", isletme_dept_id, 1, 1, 3, "Yazili", 60, "Zorunlu", True, 180, 3, 0),
        ("BUS205", "Pazarlama Yonetimi", isletme_dept_id, 2, 3, 3, "Yazili", 60, "Zorunlu", True, 160, 3, 0),
    ])
    
    # ============================================
    # IIBF - IKTISAT DERSLERI (ECON)
    # ============================================
    
    courses_data.extend([
        ("ECON101", "Mikroekonomi", iktisat_dept_id, 1, 1, 3, "Yazili", 60, "Zorunlu", True, 170, 3, 0),
        ("ECON102", "Makroekonomi", iktisat_dept_id, 1, 2, 3, "Yazili", 60, "Zorunlu", True, 165, 3, 0),
    ])
    
    # ============================================
    # IIBF - ULUSLARARASI ILISKILER DERSLERI (INT)
    # ============================================
    
    courses_data.extend([
        ("INT101", "Siyaset Bilimi", uli_dept_id, 1, 1, 3, "Yazili", 60, "Zorunlu", True, 150, 3, 0),
        ("INT203", "Diplomasi Tarihi", uli_dept_id, 2, 3, 3, "Test", 60, "Zorunlu", True, 130, 3, 0),
    ])
    
    added_count = 0
    lecturer_index = {}  # Her bolum icin hoca indeksi
    
    for course in courses_data:
        code, name, dept_id, year, period, credit, exam_type, exam_duration, course_type, has_exam, student_count, theory_hours, lab_hours = course
        
        if dept_id is None:
            print(f"[WARN] Bolum ID bulunamadi: {code} - {name} atlaniyor")
            continue
        
        if dept_id not in lecturer_index:
            lecturer_index[dept_id] = 0
        lecturer_id = get_lecturer_for_dept(dept_id, lecturer_index[dept_id])
        lecturer_index[dept_id] += 1
        
        semester = 1 if period % 2 == 1 else 2
        
        cursor.execute("SELECT id FROM courses WHERE code = %s", (code,))
        if cursor.fetchone():
            print(f"[SKIP] Ders kodu zaten mevcut: {code}")
            continue
        
        lecturer_count = 1
        if student_count >= 200:
            lecturer_count = 3
        elif student_count >= 100:
            lecturer_count = 2
        
        cursor.execute("""
            INSERT INTO courses (
                department_id, lecturer_id, code, name, credit, year, semester, period,
                theory_hours, lab_hours, course_type, student_count, lecturer_count,
                exam_type, exam_duration, has_exam
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            dept_id, lecturer_id, code, name, credit, year, semester, period,
            theory_hours, lab_hours, course_type, student_count, lecturer_count,
            exam_type, exam_duration, has_exam
        ))
        
        course_id = cursor.fetchone()[0]
        added_count += 1
        
        hoca_info = "Atanmamis"
        if lecturer_id and dept_id in dept_lecturers:
            for lec in dept_lecturers[dept_id]:
                if lec['id'] == lecturer_id:
                    hoca_info = f"{lec['title']} {lec['first_name']} {lec['last_name']}"
                    break
        
        print(f"[OK] {code} - {name} (ID: {course_id}, Donem: {period}, Hoca: {hoca_info})")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n[DONE] Toplam {added_count} ders basariyla eklendi!")


if __name__ == "__main__":
    add_all_courses()
