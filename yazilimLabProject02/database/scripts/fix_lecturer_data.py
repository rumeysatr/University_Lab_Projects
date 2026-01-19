"""
Ogretim uyesi verilerindeki sorunlari duzelten migration scripti.
Bu script mevcut kayitlardaki first_name alanindan unvanlari ayirip title alanina tasir.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "123"),
    "database": os.getenv("DB_NAME", "universite_sinav_db")
}

ACADEMIC_TITLES = [
    # Turkce karakterli versiyonlar
    'Dr. Öğr. Üyesi',
    'Öğr. Gör. Dr.',
    'Arş. Gör. Dr.',
    'Yrd. Doç. Dr.',
    'Prof. Dr.',
    'Doç. Dr.',
    'Öğr. Gör.',
    'Arş. Gör.',
    # ASCII versiyonlar
    'Dr. Ogr. Uyesi',
    'Ogr. Gor. Dr.',
    'Ars. Gor. Dr.',
    'Yrd. Doc. Dr.',
    'Doc. Dr.',
    'Ogr. Gor.',
    'Ars. Gor.',
    # Kisaltmalar
    'Yrd. Doç.',
    'Yrd. Doc.',
    'Prof.',
    'Doç.',
    'Doc.',
    'Dr.',
    'Okt.',
    'Uz.',
    'Av.',
    'Bay',
    'Çev.',
    'Cev.',
    'Öğr.',
    'Ogr.',
]


def fix_lecturer_titles():
    conn = None
    try:
        print("=" * 100)
        print("Ogretim Uyesi Unvan Duzeltme Scripti")
        print("=" * 100)
        
        print(f"\nVeritabanina baglaniliyor: {DB_CONFIG['database']}@{DB_CONFIG['host']}...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("\nOgretim uyeleri aliniyor...")
        cur.execute("SELECT id, first_name, last_name, title FROM lecturers ORDER BY id")
        lecturers = cur.fetchall()
        
        print(f"Toplam {len(lecturers)} ogretim uyesi bulundu.\n")
        print("-" * 100)
        
        fixed_count = 0
        for lecturer_id, first_name, last_name, title in lecturers:
            if not first_name:
                continue
                
            new_first_name = first_name
            new_last_name = last_name or ""
            new_title = title or ""
            changed = False
            
            full_name = f"{first_name} {last_name}".strip() if last_name else first_name
            
            for academic_title in ACADEMIC_TITLES:
                if full_name.startswith(academic_title + ' '):
                    remaining = full_name[len(academic_title):].strip()
                    parts = remaining.split(' ', 1)
                    new_first_name = parts[0] if parts else ''
                    new_last_name = parts[1] if len(parts) > 1 else ''
                    new_title = academic_title
                    changed = True
                    break
                elif first_name.startswith(academic_title + ' '):
                    remaining = first_name[len(academic_title):].strip()
                    new_first_name = remaining
                    new_title = academic_title
                    changed = True
                    break
            
            if changed:
                print(f"[FIX] ID={lecturer_id}")
                print(f"      Eski: first_name='{first_name}', last_name='{last_name}', title='{title}'")
                print(f"      Yeni: first_name='{new_first_name}', last_name='{new_last_name}', title='{new_title}'")
                print()
                
                cur.execute("""
                    UPDATE lecturers 
                    SET first_name = %s, last_name = %s, title = %s
                    WHERE id = %s
                """, (new_first_name, new_last_name, new_title, lecturer_id))
                fixed_count += 1
        
        print("-" * 100)
        
        if fixed_count > 0:
            conn.commit()
            print(f"\n[OK] Toplam {fixed_count} kayit duzeltildi!")
        else:
            print("\n[INFO] Duzeltilecek kayit bulunamadi.")
        
        print("\n[3] Guncellenmis ogretim uyesi verileri:")
        print("-" * 100)
        
        cur.execute("""
            SELECT id, title, first_name, last_name, email 
            FROM lecturers 
            ORDER BY id
        """)
        
        lecturers = cur.fetchall()
        
        print(f"{'ID':<5} {'Unvan':<20} {'Ad':<20} {'Soyad':<25} {'E-posta':<30}")
        print("-" * 100)
        
        for lecturer in lecturers:
            lid, ltitle, first_name, last_name, email = lecturer
            print(f"{lid:<5} {(ltitle or '-'):<20} {(first_name or '-'):<20} {(last_name or '-'):<25} {(email or '-'):<30}")
        
        print("-" * 100)
        print("\n[OK] Tum islemler basariyla tamamlandi!")
        
    except Exception as e:
        print(f"\n[ERROR] Hata: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            print("\nVeritabani baglantisi kapatildi.")


if __name__ == '__main__':
    fix_lecturer_titles()
