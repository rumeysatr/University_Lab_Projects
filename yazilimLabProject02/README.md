# 🎓 Üniversite Sınav Programı Yönetim Sistemi

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational%20Use-green.svg)](LICENSE)

Üniversite sınavlarının otomatik planlanması ve yönetimi için geliştirilmiş Python/Tkinter tabanlı masaüstü uygulaması.

## 🚀 Özellikler

- 👥 **Rol Bazlı Erişim**: Admin, Bölüm Yetkilisi, Hoca ve Öğrenci rolleri
- 🤖 **Otomatik Sınav Planlama**: Çakışma kontrolü ile akıllı zamanlama algoritması
- 🏢 **Kaynak Yönetimi**: Fakülte, bölüm, derslik, öğretim üyesi ve ders yönetimi
- 📊 **Raporlama**: Excel formatında sınav programı dışa aktarımı

## 📋 Gereksinimler

- Python 3.10+
- PostgreSQL 12+

## ⚡ Hızlı Kurulum

```bash
# 1. Repository'i klonlayın
git clone <repository-url>
cd yazilimLab02

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Veritabanı yapılandırmasını yapın
cp .env.example .env
# .env dosyasını veritabanı bilgilerinizle düzenleyin

# 4. Veritabanını kurun
python database/setup_db.py

# 5. Test verilerini ekleyin (opsiyonel)
python database/db_seeder.py

# 6. Uygulamayı çalıştırın
python src/main.py
```

## 🔐 Giriş Bilgileri

| Rol | Kullanıcı Adı | Şifre |
|-----|---------------|-------|
| Admin | admin | admin123 |
| Bölüm Yetkilisi | fatma.celik | 123456 |
| Hoca | ahmet.yilmaz | 123456 |
| Öğrenci | ogrenci.bm1 | 123456 |
...

## 📁 Proje Yapısı

```
yazilimLab02/
├── 📂 database/        # Veritabanı script'leri ve migrations
├── 📂 src/            # Ana uygulama kodu
│   ├── 📂 config/     # Veritabanı ve uygulama yapılandırması
│   ├── 📂 models/     # Veri modelleri
│   ├── 📂 repositories/ # Veritabanı erişim katmanı
│   ├── 📂 services/   # İş mantığı katmanı
│   ├── 📂 controllers/ # Controller katmanı
│   ├── 📂 views/      # Tkinter arayüz bileşenleri
│   └── 📂 utils/      # Yardımcı modüller
└── 📄 requirements.txt # Python bağımlılıkları
```

## 🎯 Kullanım

1. **Admin**: Sistem genel ayarları, kullanıcı yönetimi
2. **Bölüm Yetkilisi**: Bölüm derslerini ve sınavlarını yönetir
3. **Hoca**: Bölümündeki sınavları götüntüler
4. **Öğrenci**: Sınav programını görüntüler

## 📝 Geliştirme

Bu proje **Yazılım Laboratuvarı I** dersi kapsamında eğitim amaçlı geliştirilmiştir (2025).



