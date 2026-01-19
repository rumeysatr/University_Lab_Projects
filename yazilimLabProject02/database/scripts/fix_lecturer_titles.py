"""
Öğretim üyesi verilerindeki unvan sorununu düzelten migration scripti.
Bu script mevcut kayıtlardaki first_name alanından unvanları ayırıp title alanına taşır.
"""

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "123",
    "database": "universite_sinav_db"
}

ACADEMIC_TITLES = [
    'Dr. Öğr. Üyesi',
    'Öğr. Gör. Dr.',
    'Arş. Gör. Dr.',
    'Prof. Dr.',
    'Doç. Dr.',
    'Öğr. Gör.',
    'Arş. Gör.',
]


def fix_lecturer_titles():
    conn = None
    try:
        print("Veritabanına bağlanılıyor...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("Öğretim üyeleri alınıyor...")
        cur.execute("SELECT id, first_name, last_name, title FROM lecturers")
        lecturers = cur.fetchall()
        
        print(f"Toplam {len(lecturers)} öğretim üyesi bulundu.")
        
        fixed_count = 0
        for lecturer_id, first_name, last_name, title in lecturers:
            if not first_name:
                continue
                
            new_first_name = first_name
            new_last_name = last_name
            new_title = title
            changed = False
            
            full_name = f"{first_name} {last_name}" if last_name else first_name
            
            for academic_title in ACADEMIC_TITLES:
                if full_name.startswith(academic_title + ' '):
                    remaining = full_name[len(academic_title):].strip()
                    parts = remaining.split(' ', 1)
                    new_first_name = parts[0] if parts else ''
                    new_last_name = parts[1] if len(parts) > 1 else ''
                    
                    if not new_title or new_title != academic_title:
                        new_title = academic_title
                    
                    changed = True
                    break
            
            if not changed:
                for academic_title in ACADEMIC_TITLES:
                    if first_name.startswith(academic_title + ' '):
                        remaining = first_name[len(academic_title):].strip()
                        new_first_name = remaining
                        if not new_title or new_title != academic_title:
                            new_title = academic_title
                        changed = True
                        break
            
            if changed:
                print(f"  Düzeltiliyor: '{first_name} {last_name}' -> Title: '{new_title}', Ad: '{new_first_name}', Soyad: '{new_last_name}'")
                cur.execute("""
                    UPDATE lecturers 
                    SET first_name = %s, last_name = %s, title = %s
                    WHERE id = %s
                """, (new_first_name, new_last_name, new_title, lecturer_id))
                fixed_count += 1
        
        conn.commit()
        print(f"\n✅ Toplam {fixed_count} kayıt düzeltildi!")
        
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Bağlantı kapatıldı.")


if __name__ == '__main__':
    fix_lecturer_titles()
