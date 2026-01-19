# 🎓 Üniversite Sınav Programı Sistemi

Üniversite sınav programlarını **otomatik olarak planlayan** ve yöneten bir masaüstü uygulamasıdır. Sistem, fakülteler, bölümler, derslikler, öğretim üyeleri, öğrenciler ve dersler arasındaki ilişkileri yönetir ve **çakışmasız** bir sınav programı oluşturur.

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Veritabanı Şeması](#-veritabanı-şeması)
- [API Referansı](#-api-referansı)
- [Test](#-test)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## ✨ Özellikler

### 🔑 Temel Özellikler
- **Otomatik Sınav Programı Oluşturma** - Greedy + Backtracking algoritması ile optimize edilmiş planlama
- **Öğrenci Bazlı Çakışma Kontrolü** - Gerçek öğrenci listeleri üzerinden kesişim kontrolü
- **Derslik Birleştirme** - Yeterli kapasite yoksa birden fazla derslik otomatik birleştirme
- **Derslik Yakınlık Grafiği** - Birleştirme için optimize edilmiş derslik seçimi
- **Öğretim Üyesi Müsaitlik Kontrolü** - Haftanın günlerine göre müsaitlik takibi

### 👥 Kullanıcı Rolleri
| Rol | Yetkiler |
|-----|----------|
| **Admin** | Tüm işlemler: CRUD, raporlama, kullanıcı yönetimi |
| **Bölüm Yetkilisi** | Kendi bölümü için CRUD ve raporlama |
| **Öğretim Üyesi** | Sınav programı görüntüleme |
| **Öğrenci** | Kendi sınav programını görüntüleme |

### 📊 Raporlama
- **PDF Export** - Sınav programlarını PDF formatında dışa aktarma
- **Excel Export** - Detaylı raporlar için Excel çıktısı
- **Öğrenci Raporları** - Kişiselleştirilmiş sınav programları
- **Ders Raporları** - Ders bazlı sınav programları

### 🔒 Güvenlik
- **Bcrypt Şifreleme** - Güvenli parola hash'leme
- **Ortam Değişkenleri** - `.env` ile hassas bilgi yönetimi
- **Merkezi Loglama** - Renkli konsol + dosya loglama sistemi

---

## 🛠 Teknoloji Yığını

| Katman | Teknoloji | Sürüm |
|--------|-----------|-------|
| **Veritabanı** | PostgreSQL | 14+ |
| **GUI** | Tkinter | - |
| **Veritabanı Driver** | psycopg | 3.2+ |
| **Excel İşlemleri** | openpyxl, xlrd | 3.1+, 2.0+ |
| **PDF Oluşturma** | reportlab | 4.0+ |
| **Güvenlik** | bcrypt | 4.1+ |
| **Test** | pytest | 7.4+ |
| **Dil** | Python | 3.8+ (3.13 test edilmiş) |

---

## 🚀 Kurulum

### Ön Gereksinimler
- Python 3.8 veya üzeri
- PostgreSQL 14 veya üzeri
- pip (Python paket yöneticisi)

### Adım 1: Projeyi Klonlayın
```bash
git clone <repository-url>
cd yazilimLab03
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: Ortam Değişkenlerini Ayarlayın
```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sinav_sistemi
DB_USER=your_username
DB_PASSWORD=your_password
```

### Adım 5: Veritabanını Kurun
```bash
python database/core/setup_db.py
```

### Adım 6: Uygulamayı Başlatın
```bash
python src/main.py
```

---

## 📖 Kullanım

### Öğrenci Verisi İçe Aktarma
```python
from src.services.student_import_service import StudentImportService

service = StudentImportService()

result = service.import_from_excel(
    "exceller/SınıfListesi[BLM111].xls",
    course_id=1,
    semester="2024-2025 Güz"
)

results = service.import_from_excel_directory(
    "exceller/",
    semester="2024-2025 Güz"
)
```

### Derslik Yakınlık Grafiği
```python
from src.utils.classroom_proximity_loader import get_proximity_loader

loader = get_proximity_loader()

neighbors = loader.get_neighbors("M101")

closest = loader.get_closest_classrooms(
    "M101",
    available_list,
    limit=5
)
```

### Sınav Programı Oluşturma
```python
from src.services.scheduler_service import SchedulerService

scheduler = SchedulerService()
result = scheduler.generate_schedule(
    start_date="2025-01-20",
    end_date="2025-02-07",
    exam_type="final"
)
```

---

## 📁 Proje Yapısı

```
yazilimLab03/
├── 📁 database/                    # Veritabanı katmanı
│   ├── 📁 core/                    # Bağlantı ve kurulum
│   │   ├── connection.py           # Veritabanı bağlantı havuzu
│   │   ├── setup_db.py             # Şema oluşturma
│   │   └── recreate_db.py          # Veritabanı sıfırlama
│   ├── 📁 exceller/                # Sistem Excel dosyaları
│   │   ├── DerslikYakinlik.xlsx    # Derslik yakınlık matrisi
│   │   └── kostu_sinav_kapasiteleri.xlsx
│   └── 📁 scripts/                 # Yardımcı scriptler
│       ├── analyze_all_excel.py    # Excel analiz aracı
│       ├── create_excel_files.py   # Excel oluşturma
│       └── verify_import.py        # Veri doğrulama
│
├── 📁 docs/                        # Dokümantasyon
│   ├── 00-genel-ozet.md            # Proje genel bakış
│   ├── 01-database-katmani.md      # Veritabanı dokümantasyonu
│   ├── 02-models-katmani.md        # Model katmanı
│   ├── 03-repositories-katmani.md  # Repository katmanı
│   ├── 04-services-katmani.md      # Servis katmanı
│   ├── 05-controllers-views-katmani.md
│   ├── 06-utils-config-katmani.md
│   ├── 07-scripts-migrations.md
│   ├── 08-baslangic-rehberi.md
│   ├── 09-excel-integration.md
│   ├── 10-security.md
│   └── ...                         # Diğer dokümantasyon
│
├── 📁 exceller/                    # Öğrenci listesi Excel dosyaları
│   ├── AlgoritmaTasarımıveAnalizi[BLM331].xls
│   ├── BilgisayarMühendisliğineGiriş[BLM111].xls
│   └── ...                         # 13 ders dosyası
│
├── 📁 src/                         # Kaynak kod
│   ├── 📁 config/                  # Yapılandırma
│   │   └── database.py             # DB bağlantı yapılandırması
│   │
│   ├── 📁 models/                  # Veri modelleri (dataclass)
│   │   ├── faculty.py              # Fakülte modeli
│   │   ├── department.py           # Bölüm modeli
│   │   ├── classroom.py            # Derslik modeli
│   │   ├── lecturer.py             # Öğretim üyesi modeli
│   │   ├── course.py               # Ders modeli
│   │   ├── student.py              # Öğrenci modeli
│   │   ├── exam_schedule.py        # Sınav programı modeli
│   │   └── user.py                 # Kullanıcı modeli
│   │
│   ├── 📁 repositories/            # Veritabanı erişim katmanı
│   │   ├── base_repository.py      # Generic CRUD operasyonları
│   │   ├── faculty_repository.py
│   │   ├── department_repository.py
│   │   ├── classroom_repository.py
│   │   ├── lecturer_repository.py
│   │   ├── course_repository.py
│   │   ├── student_repository.py
│   │   ├── exam_schedule_repository.py
│   │   └── user_repository.py
│   │
│   ├── 📁 services/                # İş mantığı katmanı
│   │   ├── auth_service.py         # Kimlik doğrulama
│   │   ├── faculty_service.py
│   │   ├── department_service.py
│   │   ├── classroom_service.py
│   │   ├── lecturer_service.py
│   │   ├── course_service.py
│   │   ├── exam_schedule_service.py
│   │   ├── scheduler_service.py    # Otomatik planlama algoritması
│   │   └── student_import_service.py
│   │
│   ├── 📁 controllers/             # View-Service köprüsü
│   │   ├── auth_controller.py
│   │   ├── dashboard_controller.py
│   │   └── export_controller.py
│   │
│   ├── 📁 views/                   # Tkinter arayüz bileşenleri
│   │   ├── 📁 components/          # Ortak UI bileşenleri
│   │   │   ├── sidebar.py          # Sol menü
│   │   │   ├── data_table.py       # Veri tablosu
│   │   │   └── form_dialog.py      # Form dialog
│   │   ├── login_view.py           # Giriş ekranı
│   │   ├── dashboard_view.py       # Ana sayfa
│   │   ├── faculty_view.py         # Fakülte yönetimi
│   │   ├── department_view.py      # Bölüm yönetimi
│   │   ├── classroom_view.py       # Derslik yönetimi
│   │   ├── lecturer_view.py        # Öğretim üyesi yönetimi
│   │   ├── course_view.py          # Ders yönetimi
│   │   ├── exam_schedule_view.py   # Sınav programı
│   │   ├── import_view.py          # Veri içe aktarma
│   │   ├── reports_view.py         # Raporlar
│   │   └── student_schedule_view.py
│   │
│   ├── 📁 utils/                   # Yardımcı fonksiyonlar
│   │   ├── classroom_proximity_loader.py  # Derslik yakınlık grafiği
│   │   ├── exam_capacity_importer.py      # Kapasite içe aktarma
│   │   ├── excel_builder.py               # Excel oluşturucu
│   │   ├── excel_generator.py             # Excel rapor oluşturucu
│   │   ├── pdf_generator.py               # PDF oluşturucu
│   │   ├── student_importer.py            # Öğrenci içe aktarma
│   │   ├── logging_config.py              # Loglama yapılandırması
│   │   └── validators.py                  # Doğrulama fonksiyonları
│   │
│   └── main.py                     # Uygulama giriş noktası
│
├── 📁 logs/                        # Log dosyaları
├── .env                            # Ortam değişkenleri (git'e eklenmez)
├── .env.example                    # Örnek ortam değişkenleri
├── .gitignore
├── requirements.txt                # Python bağımlılıkları
├── tests.py                        # Test paketi
└── README.md                       # Bu dosya
```

---

## 🗄 Veritabanı Şeması

### Ana Tablolar

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  faculties   │     │  departments │     │  classrooms  │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ id           │◄────│ faculty_id   │     │ id           │
│ name         │     │ id           │     │ faculty_id   │──►
│ code         │     │ name         │     │ name         │
│ dean_name    │     │ code         │     │ capacity     │
│ is_active    │     │ head_name    │     │ room_type    │
└──────────────┘     │ is_active    │     │ block        │
                     └──────────────┘     │ is_suitable  │
                            │             └──────────────┘
                            │
                            ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  lecturers   │     │   courses    │     │   students   │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ id           │     │ id           │     │ id           │
│ department_id│◄────│ department_id│     │ department_id│◄──
│ first_name   │     │ lecturer_id  │──►  │ student_number│
│ last_name    │     │ code         │     │ first_name   │
│ title        │     │ name         │     │ last_name    │
│ available_days│    │ student_count│     │ year         │
└──────────────┘     │ exam_duration│     │ is_active    │
                     └──────────────┘     └──────────────┘
                            │                    │
                            │                    │
                            ▼                    ▼
                     ┌──────────────┐     ┌────────────────┐
                     │exam_schedule │     │student_courses │
                     ├──────────────┤     ├────────────────┤
                     │ id           │     │ id             │
                     │ course_id    │◄────│ course_id      │
                     │ classroom_id │     │ student_id     │──►
                     │ exam_date    │     │ semester       │
                     │ start_time   │     │ is_active      │
                     │ end_time     │     └────────────────┘
                     │ status       │
                     └──────────────┘
```

### Önemli İlişkiler
- `students` ↔ `courses`: `student_courses` tablosu ile N:N ilişki
- `exam_schedule` → `courses`: Her sınav bir derse ait
- `exam_schedule` → `classrooms`: Her sınav bir derslikte yapılır
- `unique_classroom_time`: Aynı derslik + tarih + saat kombinasyonu tekrar edemez

---

## 🔌 API Referansı

### Repository Katmanı (BaseRepository)

```python
# Temel CRUD operasyonları
repository.get_all()                    # Tüm kayıtları getir
repository.get_by_id(id)                # ID ile getir
repository.create(entity)               # Yeni kayıt oluştur
repository.update(entity)               # Kayıt güncelle
repository.delete(id)                   # Kayıt sil

# Transaction yönetimi
with repository.transaction() as tx:
    repository.create(entity1)
    repository.create(entity2)
    tx.commit()

# Batch operasyonları
repository._execute_batch(query, values_list)
```

### Service Katmanı

```python
# Kimlik Doğrulama
auth_service.login(username, password)  # → (success, message)
auth_service.logout()
auth_service.has_permission(permission)

# Sınav Planlama
scheduler_service.generate_schedule(start_date, end_date, exam_type)
scheduler_service.check_conflicts(course_id, date, time)

# Öğrenci Import
import_service.import_from_excel(file_path, course_id, semester)
import_service.import_from_excel_directory(directory, semester)
```

### Controller Katmanı

```python
# Dashboard Controller
dashboard_controller.get_student_schedule(student_id)
dashboard_controller.filter_schedule_by_user(user_info)
dashboard_controller.get_upcoming_exams(limit=5)

# Export Controller
export_controller.export_to_pdf(schedule, output_path)
export_controller.export_to_excel(schedule, output_path)
```

---

## 🧪 Test

### Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
python -m pytest tests.py -v

# Belirli bir test sınıfını çalıştır
pytest tests.py::TestUserModel -v

# Belirli bir testi çalıştır
pytest tests.py::TestDashboardController::test_get_student_schedule_exists -v

# Kapsam raporu ile
pytest tests.py --cov=src --cov-report=html
```

### Test Kategorileri
- **TestUserModel** - Kullanıcı modeli ve bcrypt testleri
- **TestProximityLoader** - Derslik yakınlık grafiği testleri
- **TestStudentImporter** - Öğrenci import testleri
- **TestExcelBuilder** - Excel oluşturma testleri
- **TestDashboardController** - Dashboard controller testleri

---

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Kod Standartları
- PEP 8 uyumlu Python kodu
- Type hints kullanımı
- Docstring'ler ile fonksiyon dokümantasyonu
- Test coverage %80+

---
