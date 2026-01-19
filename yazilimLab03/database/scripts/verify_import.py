#!/usr/bin/env python3
"""
Veritabanındaki verileri doğrulama scripti
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.repositories.faculty_repository import FacultyRepository
from src.repositories.department_repository import DepartmentRepository
from src.repositories.course_repository import CourseRepository
from src.repositories.lecturer_repository import LecturerRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.student_repository import StudentCourseRepository


def main():
    print('='*60)
    print('VERİTABANI ÖZETİ')
    print('='*60)

    # Sayımları yap
    faculty_repo = FacultyRepository()
    department_repo = DepartmentRepository()
    course_repo = CourseRepository()
    lecturer_repo = LecturerRepository()
    student_repo = StudentRepository()
    student_course_repo = StudentCourseRepository()

    faculties = faculty_repo.get_all()
    departments = department_repo.get_all_with_faculty()
    courses = course_repo.get_all_with_details()
    lecturers = lecturer_repo.get_all_with_details()
    students = student_repo.get_all_with_details()

    print(f'\n📊 ÖZET SAYIMLAR:')
    print(f'  Fakülte Sayısı: {len(faculties)}')
    print(f'  Bölüm Sayısı: {len(departments)}')
    print(f'  Ders Sayısı: {len(courses)}')
    print(f'  Hoca Sayısı: {len(lecturers)}')
    print(f'  Öğrenci Sayısı: {len(students)}')

    # Fakülteler
    print(f'\n🏛️  FAKÜLTELER:')
    for f in faculties:
        print(f'  • {f.code}: {f.name}')

    # Bölümler
    print(f'\n📚 BÖLÜMLER:')
    for d in departments:
        faculty_name = d.faculty_name if hasattr(d, 'faculty_name') else 'Belirtilmemiş'
        print(f'  • {d.code}: {d.name} ({faculty_name})')

    # Dersler
    print(f'\n📖 DERSLER:')
    for c in courses:
        dept_name = c.department_name if hasattr(c, 'department_name') else '-'
        lecturer_name = c.lecturer_name if hasattr(c, 'lecturer_name') else '-'
        print(f'  • {c.code}: {c.name}')
        print(f'    Bölüm: {dept_name}, Hoca: {lecturer_name}, Öğrenci: {c.student_count}')

    # Hocalar
    print(f'\n👨‍🏫 HOÇALAR:')
    for l in lecturers:
        dept_name = l.department_name if hasattr(l, 'department_name') else '-'
        print(f'  • {l.full_name} ({dept_name})')

    # Öğrenciler (ilk 10)
    print(f'\n���� ÖĞRENCİLER (İlk 10):')
    for s in students[:10]:
        dept_name = s.department_name if hasattr(s, 'department_name') else '-'
        print(f'  • {s.student_number}: {s.full_name} ({dept_name}, {s.year}. sınıf)')

    if len(students) > 10:
        print(f'  ... ve {len(students) - 10} öğrenci daha')

    # Öğrenci-Ders ilişkileri
    student_courses = student_course_repo.get_by_course_id(courses[0].id) if courses else []
    print(f'\n📝 ÖĞRENCİ-DERS İLİŞKİLERİ (İlk ders için örnek):')
    if courses:
        print(f'  Ders: {courses[0].code} - {courses[0].name}')
        for sc in student_courses[:5]:
            print(f'  • {sc.student_number}: {sc.student_name}')
        if len(student_courses) > 5:
            print(f'  ... ve {len(student_courses) - 5} öğrenci daha')

    print('\n' + '='*60)
    print('✅ DOĞRULAMA TAMAMLANDI')
    print('='*60)


if __name__ == '__main__':
    main()
