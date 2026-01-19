#!/usr/bin/env python3
"""
Tüm Excel dosyalarını analiz eder
"""
import os
import sys
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import xlrd
import re

def extract_course_code(filename):
    """Dosya adından ders kodunu çıkarır"""
    # Dosya adından desen: SınıfListesi[KOD].xls veya SınıfListesi[KOD] (N).xls
    match = re.search(r'\[([A-Z0-9]+)\]', filename)
    if match:
        return match.group(1)
    return None

def analyze_all_files():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    excel_dir = os.path.join(base_dir, 'exceller')
    
    # Tüm xls dosyalarını bul
    pattern = os.path.join(excel_dir, '*.xls')
    files = sorted(glob.glob(pattern))
    
    print(f"📁 Toplam {len(files)} Excel dosyası bulundu\n")
    
    results = []
    
    for file_path in files:
        filename = os.path.basename(file_path)
        course_code = extract_course_code(filename)
        
        try:
            wb = xlrd.open_workbook(file_path, formatting_info=False)
            sheet = wb.sheet_by_index(0)
            
            # Bölüm adını bul
            department_name = None
            for row_idx in range(min(10, sheet.nrows)):
                for col_idx in range(sheet.ncols):
                    val = str(sheet.cell_value(row_idx, col_idx))
                    if 'MÜHENDİSLİĞİ' in val or 'MÜHENDISLIGI' in val:
                        department_name = val.strip()
                        break
                if department_name:
                    break
            
            # Öğrenci sayısını hesapla (Row 5'ten başlayıp)
            student_count = 0
            for row_idx in range(5, sheet.nrows):
                # Öğrenci no sütunu (index 4) kontrol et
                if sheet.ncols > 4:
                    student_no = str(sheet.cell_value(row_idx, 4)).strip()
                    if student_no and student_no.isdigit() and len(student_no) == 9:
                        student_count += 1
            
            results.append({
                'filename': filename,
                'course_code': course_code,
                'department': department_name,
                'student_count': student_count,
                'total_rows': sheet.nrows
            })
            
            print(f"📄 {filename:35} | {course_code or 'N/A':8} | {department_name or 'N/A':30} | {student_count:3} öğrenci")
            
        except Exception as e:
            print(f"❌ {filename}: {str(e)}")
    
    print(f"\n{'='*100}")
    print("📊 ÖZET")
    print(f"{'='*100}")
    
    # Bölümlere göre grupla
    depts = {}
    for r in results:
        if r['department']:
            dept = r['department']
            if dept not in depts:
                depts[dept] = {'courses': [], 'total_students': 0}
            depts[dept]['courses'].append(r['course_code'])
            depts[dept]['total_students'] += r['student_count']
    
    print("\n🎓 Bölümler ve Dersler:")
    for dept, info in sorted(depts.items()):
        print(f"  • {dept}")
        print(f"    Dersler: {', '.join(info['courses'])}")
        print(f"    Toplam Öğrenci: {info['total_students']}")
    
    print(f"\n🔍 Ders Kodları:")
    all_codes = sorted(set([r['course_code'] for r in results if r['course_code']]))
    for code in all_codes:
        matching = [r for r in results if r['course_code'] == code]
        for m in matching:
            print(f"  • {code}: {m['filename']} ({m['student_count']} öğrenci)")

if __name__ == "__main__":
    analyze_all_files()
