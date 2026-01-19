"""
Birim testleri: SchedulerService içindeki çakışma kontrol fonksiyonlarını test eder
"""

import os
import sys
from datetime import date, time, datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.scheduler_service import SchedulerService
from src.repositories.course_repository import CourseRepository
from src.repositories.classroom_repository import ClassroomRepository
from src.repositories.lecturer_repository import LecturerRepository
from src.repositories.exam_schedule_repository import ExamScheduleRepository
from src.models.exam_schedule import ExamSchedule


def test_time_slot_overlap():
    from src.services.scheduler_service import TimeSlot
    
    # Çakışan durumlar
    slot1 = TimeSlot(time(9, 0), time(11, 0))
    slot2 = TimeSlot(time(10, 0), time(12, 0))  # Örtüşüyor
    assert slot1.overlaps(slot2), "9:00-11:00 ile 10:00-12:00 çakışmalı"
    
    # Hemen bitip başlayan durumlar
    slot3 = TimeSlot(time(9, 0), time(11, 0))
    slot4 = TimeSlot(time(11, 0), time(13, 0))  # Çakışmıyor
    assert not slot3.overlaps(slot4), "9:00-11:00 ile 11:00-13:00 çakışmamalı"
    
    # Tamamen ayrı durumlar
    slot5 = TimeSlot(time(9, 0), time(11, 0))
    slot6 = TimeSlot(time(14, 0), time(16, 0))  # Çakışmıyor
    assert not slot5.overlaps(slot6), "9:00-11:00 ile 14:00-16:00 çakışmamalı"
    
    # Tamamen iç içe durum
    slot7 = TimeSlot(time(9, 0), time(17, 0))
    slot8 = TimeSlot(time(11, 0), time(13, 0))  # Örtüşüyor
    assert slot7.overlaps(slot8), "9:00-17:00 ile 11:00-13:00 çakışmalı"
    
    print("✓ TimeSlot çakışma kontrol testleri başarılı")


def test_check_classroom_conflict():
    """Derslik çakışma kontrolünü test eder"""
    scheduler = SchedulerService()
    exam_date = date(2024, 1, 15)  # Pazartesi
    start_time = time(9, 0)
    end_time = time(11, 0)
    
    # Önce bir sınav oluşturalım
    exam_repo = ExamScheduleRepository()
    course_repo = CourseRepository()
    classroom_repo = ClassroomRepository()
    
    # Test için bir ders, derslik ve öğretim üyesi alalım
    course = course_repo.get_all()[0] if course_repo.get_all() else None
    classroom = classroom_repo.get_all()[0] if classroom_repo.get_all() else None
    
    if not course or not classroom:
        print("⚠ Test verisi bulunamadı: Ders veya derslik yok")
        return False
    
    # Önce var olan sınavları temizleyelim
    existing_exams = exam_repo.get_by_classroom_and_date(classroom.id, exam_date)
    for exam in existing_exams:
        exam_repo.delete(exam.id)
    
    # Aynı derslik için aynı zaman diliminde çakışma testi
    exam1 = ExamSchedule(
        course_id=course.id,
        classroom_id=classroom.id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        exam_type="test"
    )
    exam1_id = exam_repo.create(exam1)
    assert exam1_id is not None, "İlk sınav oluşturulamadı"
    
    has_conflict = scheduler._has_classroom_conflict(
        classroom.id, exam_date, start_time, end_time
    )
    assert has_conflict, "Aynı derslik ve aynı saat için çakışma tespit edilmeli"
    
    has_conflict = scheduler._has_classroom_conflict(
        classroom.id, exam_date, time(14, 0), time(16, 0)
    )
    assert not has_conflict, "Aynı derslik fakat farklı saat için çakışma olmamalı"
    
    exam_repo.delete(exam1_id)
    
    print("✓ Derslik çakışma kontrol testleri başarılı")
    return True


def test_check_student_conflict():
    """Aynı bölüm/yıl öğrencilerinin çakışma kontrolünü test eder"""
    scheduler = SchedulerService()
    exam_date = date(2024, 1, 16)  # Salı
    start_time = time(9, 0)
    end_time = time(11, 0)
    
    exam_repo = ExamScheduleRepository()
    course_repo = CourseRepository()
    classroom_repo = ClassroomRepository()
    
    courses = course_repo.get_all()
    if len(courses) < 2:
        print("⚠ Test verisi yetersiz: En az 2 ders gerekli")
        return False
    
    course1 = courses[0]
    course2 = None
    for c in courses[1:]:
        if c.department_id == course1.department_id and c.year == course1.year:
            course2 = c
            break
    
    if not course2:
        print("⚠ Test verisi bulunamadı: Aynı bölüm ve yılda iki ders yok")
        return False
    
    classrooms = classroom_repo.get_all()
    if len(classrooms) < 2:
        print("⚠ Test verisi yetersiz: En az 2 derslik gerekli")
        return False
    
    classroom1 = classrooms[0]
    classroom2 = classrooms[1]
    
    existing_exams = exam_repo.get_by_date(exam_date)
    for exam in existing_exams:
        if exam.course_id in [course1.id, course2.id]:
            exam_repo.delete(exam.id)
    
    exam1 = ExamSchedule(
        course_id=course1.id,
        classroom_id=classroom1.id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        exam_type="test"
    )
    exam1_id = exam_repo.create(exam1)
    assert exam1_id is not None, "İlk sınav oluşturulamadı"
    
    has_conflict = scheduler._has_student_conflict(
        course2.department_id, course2.year, exam_date, start_time, end_time, course2.id
    )
    assert has_conflict, "Aynı bölüm/yıl öğrencileri için aynı saatte çakışma tespit edilmeli"
    
    exam_repo.delete(exam1_id)
    
    print("✓ Öğrenci çakışma kontrol testleri başarılı")
    return True


def test_check_lecturer_conflict():
    """Öğretim üyesi çakışma kontrolünü test eder"""
    scheduler = SchedulerService()
    exam_date = date(2024, 1, 17)  # Çarşamba
    start_time = time(9, 0)
    end_time = time(11, 0)
    
    exam_repo = ExamScheduleRepository()
    course_repo = CourseRepository()
    classroom_repo = ClassroomRepository()
    lecturer_repo = LecturerRepository()
    
    lecturers = lecturer_repo.get_all()
    if not lecturers:
        print("⚠ Test verisi bulunamadı: Öğretim üyesi yok")
        return False
    
    lecturer = lecturers[0]
    courses = course_repo.get_by_lecturer_id(lecturer.id)
    if len(courses) < 2:
        print("⚠ Test verisi bulunamadı: Öğretim üyesine ait en az 2 ders yok")
        return False
    
    course1 = courses[0]
    course2 = courses[1]
    
    classrooms = classroom_repo.get_all()
    if len(classrooms) < 2:
        print("⚠ Test verileri yetersiz: En az 2 derslik gerekli")
        return False
    
    classroom1 = classrooms[0]
    classroom2 = classrooms[1]
    
    existing_exams = exam_repo.get_by_date(exam_date)
    for exam in existing_exams:
        if exam.course_id in [course1.id, course2.id]:
            exam_repo.delete(exam.id)
    
    exam1 = ExamSchedule(
        course_id=course1.id,
        classroom_id=classroom1.id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        exam_type="test"
    )
    exam1_id = exam_repo.create(exam1)
    assert exam1_id is not None, "İlk sınav oluşturulamadı"
    
    has_conflict = scheduler._has_lecturer_conflict(
        lecturer.id, exam_date, start_time, end_time
    )
    assert has_conflict, "Aynı öğretim üyesi için aynı saatte çakışma tespit edilmeli"
    
    exam_repo.delete(exam1_id)
    
    print("✓ Öğretim üyesi çakışma kontrol testleri başarılı")
    return True


def test_check_all_conflicts_integration():
    """Tüm çakışma kontrollerinin entegrasyon testi"""
    scheduler = SchedulerService()
    exam_date = date(2024, 1, 18)  # Perşembe
    start_time = time(9, 0)
    end_time = time(11, 0)
    
    exam_repo = ExamScheduleRepository()
    course_repo = CourseRepository()
    classroom_repo = ClassroomRepository()
    
    course = course_repo.get_all()[0] if course_repo.get_all() else None
    classroom = classroom_repo.get_all()[0] if classroom_repo.get_all() else None
    
    if not course or not classroom:
        print("⚠ Test verisi bulunamadı")
        return False
    
    existing_exams = exam_repo.get_by_classroom_and_date(classroom.id, exam_date)
    for exam in existing_exams:
        exam_repo.delete(exam.id)
    
    # 1. Çakışma yok durumu
    result = scheduler._check_all_conflicts(
        course_id=course.id,
        classroom_id=classroom.id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        department_id=course.department_id,
        course_year=course.year,
        lecturer_id=course.lecturer_id
    )
    assert not result['has_conflict'], f"Beklenmedik çakışma: {result['reason']}"
    
    # 2. Bir sınav oluşturup çakışma testi
    exam1 = ExamSchedule(
        course_id=course.id,
        classroom_id=classroom.id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        exam_type="test"
    )
    exam1_id = exam_repo.create(exam1)
    assert exam1_id is not None, "Sınav oluşturulamadı"
    
    # 3. Şimdi çakışma olmalı
    result = scheduler._check_all_conflicts(
        course_id=999,  # Farklı bir kurs ID'si
        classroom_id=classroom.id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        department_id=course.department_id,
        course_year=course.year,
        lecturer_id=course.lecturer_id
    )
    assert result['has_conflict'], "Çakışma tespit edilmeli"
    assert result['reason'] == 'Derslik çakışması', f"Yanlış çakışma sebebi: {result['reason']}"
    
    exam_repo.delete(exam1_id)
    
    print("✓ Tüm çakışma kontrolleri entegrasyon testi başarılı")
    return True


def main():
    """Tüm birim testlerini çalıştırır"""
    print("=" * 60)
    print("BİRİM TESTLERİ - SchedulerService Çakışma Kontrolleri")
    print("=" * 60)
    
    test_results = []
    
    # Testleri çalıştır
    test_results.append(("TimeSlot Çakışma Kontrolü", test_time_slot_overlap))
    test_results.append(("Derslik Çakışma Kontrolü", test_check_classroom_conflict))
    test_results.append(("Öğrenci Çakışma Kontrolü", test_check_student_conflict))
    test_results.append(("Öğretim Üyesi Çakışma Kontrolü", test_check_lecturer_conflict))
    test_results.append(("Tüm Çakışma Kontrolleri Entegrasyonu", test_check_all_conflicts_integration))
    
    # Sonuçları yazdır
    print("\n" + "=" * 60)
    print("TEST SONUÇLARI")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        if result:
            print(f"✓ {test_name}: BAŞARILI")
            passed += 1
        else:
            print(f"✗ {test_name}: BAŞARISIZ")
            failed += 1
    
    print("-" * 60)
    print(f"Toplam Test: {len(test_results)}")
    print(f"Başarılı: {passed}")
    print(f"Başarısız: {failed}")
    
    if failed == 0:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
    else:
        print(f"\n⚠ {failed} TEST BAŞARISIZ!")
    
    return failed == 0


if __name__ == "__main__":
    main()