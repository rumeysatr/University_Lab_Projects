import unittest
import os
import sys
from unittest.mock import MagicMock, patch
from datetime import date, time, datetime
from io import StringIO

from src.services.scheduler_service import SchedulerService
from src.models.course import Course
from src.models.classroom import Classroom
from src.models.lecturer import Lecturer
from src.models.exam_schedule import ExamSchedule

class TestExamScheduler(unittest.TestCase):
    
    def setUp(self):
        """Her testten önce çalışır: Servisi ve Mock Repository'leri hazırlar"""
        
        # Repository'leri patch'leyerek gerçek veritabanı bağlantısını kesme işlemi
        self.patcher_course = patch('src.services.scheduler_service.CourseRepository')
        self.patcher_class = patch('src.services.scheduler_service.ClassroomRepository')
        self.patcher_exam = patch('src.services.scheduler_service.ExamScheduleRepository')
        self.patcher_lec = patch('src.services.scheduler_service.LecturerRepository')
        self.patcher_dept = patch('src.services.scheduler_service.DepartmentRepository')

        self.MockCourseRepo = self.patcher_course.start()
        self.MockClassRepo = self.patcher_class.start()
        self.MockExamRepo = self.patcher_exam.start()
        self.MockLecRepo = self.patcher_lec.start()
        self.MockDeptRepo = self.patcher_dept.start()

        # Servisi başlat (Mock repository'leri kullanacak)
        self.service = SchedulerService()
        
        self.service.course_repo = self.MockCourseRepo.return_value
        self.service.classroom_repo = self.MockClassRepo.return_value
        self.service.exam_repo = self.MockExamRepo.return_value
        self.service.lecturer_repo = self.MockLecRepo.return_value

    def tearDown(self):
        """Her testten sonra patch'leri temizle"""
        patch.stopall()

    # 1. KAPASİTE KISITLAMASI TESTİ
    def test_kapasite_kisitlamasi(self):
        print("\nTest 1: Kapasite Kısıtlaması Kontrolü...")
        
        # 60 kişilik dersi 40 kişilik sınıfa atamaya çalışma durumu
        mock_course = Course(id=1, name="Büyük Ders", student_count=60, exam_duration=60)
        mock_classroom = Classroom(id=1, name="Küçük Sınıf", capacity=40)
        
        self.service.course_repo.get_by_id.return_value = mock_course
        self.service.classroom_repo.get_by_id.return_value = mock_classroom
        self.service.exam_repo.get_by_course_id.return_value = []

        result = self.service.validate_manual_schedule(
            course_id=1, classroom_id=1, 
            exam_date="2025-01-06", start_time="10:00"
        )
        
        self.assertFalse(result['valid'])
        error_msg = f"Derslik kapasitesi yetersiz ({mock_classroom.capacity} < {mock_course.student_count})"
        self.assertIn(error_msg, result['errors'])
        print("   -> Başarılı: Kapasite yetersiz uyarısı alındı.")

    # 2. ÖĞRETİM ÜYESİ MÜSAİTLİK KISITLAMASI TESTİ
    def test_ogretim_uyesi_musaitlik(self):
        print("Test 2: Öğretim Üyesi Müsaitlik Kontrolü...")
        
        # Hoca sadece 'Salı' müsait, ama 'Pazartesi' (2025-01-06) günü sınav atanıyor gibi bir durum
        mock_lecturer = Lecturer(id=5, first_name="Ali", last_name="Veli", available_days=['Salı'])
        mock_course = Course(id=2, name="Fizik", lecturer_id=5, student_count=30, exam_duration=60)
        mock_classroom = Classroom(id=2, name="Derslik A", capacity=50)
        
        self.service.course_repo.get_by_id.return_value = mock_course
        self.service.classroom_repo.get_by_id.return_value = mock_classroom
        self.service.lecturer_repo.get_by_id.return_value = mock_lecturer
        
        result = self.service.validate_manual_schedule(
            course_id=2, classroom_id=2, 
            exam_date="2025-01-06", start_time="10:00"
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any("Pazartesi günü müsait değil" in err for err in result['errors']))
        print("   -> Başarılı: Hoca müsaitlik kısıtı çalıştı.")

    # 3. ZAMAN ÇAKIŞMA TESPİTİ (Öğrenci/Bölüm Çakışması)
    def test_zaman_cakisma_tespiti(self):
        print("Test 3: Zaman Çakışma Tespiti (Öğrenci)...")
        
        # Aynı bölüm ve sınıfın (Dept:1, Year:1) aynı saatte başka bir sınavı var
        mock_course = Course(id=3, department_id=1, year=1, student_count=30, exam_duration=60)
        mock_classroom = Classroom(id=3, capacity=50)
        
        conflicting_exam = ExamSchedule(
            course_id=99, start_time=time(10, 0), end_time=time(11, 0),
            exam_date=date(2025, 1, 7)
        )
        conflicting_exam.course_year = 1
        
        self.service.course_repo.get_by_id.return_value = mock_course
        self.service.classroom_repo.get_by_id.return_value = mock_classroom
        self.service.exam_repo.get_by_department_and_date.return_value = [conflicting_exam]
        
        result = self.service.validate_manual_schedule(
            course_id=3, classroom_id=3, 
            exam_date="2025-01-07", start_time="10:30" # 10:30, 10:00-11:00 aralığına denk gelir
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any("Çakışma tespit edildi" in err for err in result['errors']))
        print("   -> Başarılı: Zaman çakışması tespit edildi.")

    # 4. SINAV SÜRESİ
    def test_sinav_suresi_validasyonu(self):
        print("Test 4: Sınav Süresi/Format Validasyonu...")
        
        mock_course = Course(id=4, student_count=30, exam_duration=60)
        mock_classroom = Classroom(id=4, capacity=50)
        
        self.service.course_repo.get_by_id.return_value = mock_course
        self.service.classroom_repo.get_by_id.return_value = mock_classroom
        
        # Geçersiz Saat Formatı
        result = self.service.validate_manual_schedule(
            course_id=4, classroom_id=4, 
            exam_date="2025-01-08", start_time="25:00"
        )
        self.assertFalse(result['valid'])
        self.assertIn("Geçersiz başlangıç saati formatı (HH:MM olmalı)", result['errors'])
        
        # Süre Hesaplama ve Çakışma
        # Ders süresi 120 dk. 10:00'da başlarsa 12:00'de biter.
        # 11:30'da başka bir sınav varsa çakışma vermeli.
        mock_course_long = Course(id=5, student_count=30, exam_duration=120)
        self.service.course_repo.get_by_id.return_value = mock_course_long
        
        conflict_exam = ExamSchedule(
            course_id=98, start_time=time(11, 30), end_time=time(12, 30),
            exam_date=date(2025, 1, 8)
        )
        # Derslik bazlı çakışma kontrolü için classroom sorgusunu mock'luyoruz
        self.service.exam_repo.get_by_classroom_and_date.return_value = [conflict_exam]
        
        result_duration = self.service.validate_manual_schedule(
            course_id=5, classroom_id=4, 
            exam_date="2025-01-08", start_time="10:00"
        )
        
        # Eğer süre doğru hesaplandıysa (10:00-12:00), 11:30'daki sınavla çakışmalı
        self.assertFalse(result_duration['valid'])
        print("   -> Başarılı: Sınav süresi formatı ve süreye bağlı çakışma doğrulandı.")

    # 5. UYGUN OLMAYAN DERSLİK KONTROLÜ
    def test_uygun_olmayan_derslik(self):
        print("Test 5: Uygun Olmayan Derslik (Dolu Derslik) Kontrolü...")
        
        mock_course = Course(id=6, student_count=30, exam_duration=60)
        mock_classroom = Classroom(id=6, name="Lab-1", capacity=50)

        # O derslikte o saatte başka sınav var
        occupied_exam = ExamSchedule(
            course_id=97, classroom_id=6, 
            start_time=time(14, 0), end_time=time(16, 0),
            exam_date=date(2025, 1, 9)
        )
        
        self.service.course_repo.get_by_id.return_value = mock_course
        self.service.classroom_repo.get_by_id.return_value = mock_classroom
        self.service.exam_repo.get_by_classroom_and_date.return_value = [occupied_exam]
        
        # Test: Dolu saate (14:30) atama yapmaya çalış
        result = self.service.validate_manual_schedule(
            course_id=6, classroom_id=6, 
            exam_date="2025-01-9", start_time="14:30"
        )
        
        self.assertFalse(result['valid'])
        self.assertTrue(any("Derslik çakışması" in err or "Çakışma" in err for err in result['errors']))
        print("   -> Başarılı: Dersliğin o saatte uygun olmadığı (dolu olduğu) tespit edildi.")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExamScheduler)
    
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    output = stream.getvalue()
    print(output)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    failed = failures + errors
    
    if failed == 0:
        print(f"\n*** TUM TESTLER BASARILI! ({total_tests} test calistirildi) ***")
    else:
        print(f"\n*** {failed} TEST BASARISIZ! ({failures} failure, {errors} error) ***")
        
    sys.exit(0 if failed == 0 else 1)