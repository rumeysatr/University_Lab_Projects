# Top Animasyonu Uygulaması

Tkinter tabanlı modern bir top animasyonu uygulaması. Fizik simülasyonu, çarpışma tespiti ve görsel efektler içeren interaktif bir GUI uygulaması.

## 📋 İçerik

- [Özellikler](#-özellikler)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Kullanılan Kütüphaneler](#-kullanılan-kütüphaneler)
- [Konfigürasyon](#-konfigürasyon)

## ✨ Özellikler

### 🎮 Temel Fonksiyonlar
- **Dinamik Top Animasyonu**: Farklı boyutlarda ve renklerde toplar oluşturma
- **Fizik Simülasyonu**: Gerçekçi hareket ve çarpışma fiziği
- **Çarpışma Tespiti**: Toplar arası ve kenar çarpışmaları
- **Görsel Efektler**: Gölge, gradient, parlama ve çarpışma efektleri

### 🎨 Kullanıcı Arayüzü
- **Modern Tasarım**: ttkbootstrap ile Bootstrap temaları
- **Tema Desteği**: Dark ve Light tema geçişi
- **İkonlu Butonlar**: PIL ile oluşturulmuş özel ikonlar
- **İnteraktif Renk Seçimi**: Yuvarlak renk butonları
- **Hız Kontrolü**: Animasyon hızını artırma/azaltma

### 🔧 Teknik Özellikler
- **Modüler Mimari**: Ayrı modüller (models, ui, config)
- **OOP Tasarım**: Nesne yönelimli programlama
- **Konfigürasyon Yönetimi**: Merkezi ayar dosyası
- **Grid Deseni**: Modern canvas arka planı

## 🚀 Gereksinimler

### Python Sürümü
- Python 3.7 veya üzeri

### Gerekli Kütüphaneler
```bash
pip install ttkbootstrap
pip install Pillow
```

## 🎯 Kullanım

### Uygulamayı Başlatma
```bash
python app.py
```

### Kullanım Adımları

1. **Başlat**: "BAŞLAT" butonuna tıklayarak animasyonu başlatın
2. **Boyut Seçimi**: İstediğiniz boyut butonuna tıklayarak top ekleyin
3. **Renk Seçimi**: Renk paletinden istediğiniz rengi seçin
4. **Hız Kontrolü**: "Hızlandır" butonu ile animasyon hızını artırın
5. **Tema Değiştir**: "Tema" butonu ile dark/light mod arasında geçiş yapın
6. **Sıfırla**: "SIFIRLA" butonu ile tüm topları temizleyin

### Kontroller
- **BAŞLAT**: Animasyonu başlatır
- **DURDUR**: Animasyonu durdurur
- **SIFIRLA**: Canvas'ı temizler ve ayarları sıfırlar
- **Hızlandır**: Animasyon hızını artırır
- **Tema**: Dark/Light tema geçişi yapar

## 📁 Proje Yapısı

```
yazilimLab01/
├── app.py                 # Ana uygulama sınıfı ve başlangıç noktası
├── README.md             # Proje dokümantasyonu
├── config/               # Konfigürasyon dosyaları
│   ├── __init__.py
│   └── settings.py       # Uygulama ayarları
├── models/               # Veri modelleri
│   ├── __init__.py
│   └── ball.py          # Top sınıfı ve fizik mantığı
├── ui/                   # Kullanıcı arayüzü bileşenleri
│   ├── __init__.py
│   ├── canvas_area.py   # Canvas alanı yönetimi
│   └── control_panel.py # Kontrol paneli UI
└── icons/                # İkon dosyaları
    ├── create_icons.py   # İkon oluşturma scripti
    ├── play.png
    ├── stop.png
    ├── reset.png
    ├── speed.png
    └── theme.png
```

### Yapısal İyileştirmeler
- **Kod Basitleştirme**: Uzun metodlar daha küçük, anlaşılır fonksiyonlara ayrıldı
- **Modüler Tasarım**: UI bileşenleri mantıksal parçalara bölündü
- **Tek Başlangıç Noktası**: Sadece `app.py` kullanımı
- **Temiz Kod**: Gereksiz test dosyaları kaldırıldı

## 📚 Kullanılan Kütüphaneler

### Ana Kütüphaneler
- **tkinter**: Python standart GUI kütüphanesi
- **ttkbootstrap**: Modern Bootstrap temaları için Tkinter eklentisi
- **PIL (Pillow)**: Görüntü işleme ve ikon oluşturma için

### Standart Kütüphaneler
- **random**: Rastgele konum ve hız değerleri için
- **os**: Dosya sistemi işlemleri için
- **math**: Matematiksel hesaplamalar için

### Kütüphane Görevleri
```python
# GUI ve Tema
import tkinter as tk
import ttkbootstrap as tb

# Görüntü İşleme
from PIL import Image, ImageTk

# Rastgelelik
import random
```

## ⚙️ Konfigürasyon

### Ayarlar Dosyası ([`config/settings.py`](config/settings.py))

#### Canvas Ayarları
```python
KANVAS_GENISLIK = 450    # Canvas genişliği (piksel)
KANVAS_YUKSEKLIK = 400   # Canvas yüksekliği (piksel)
```

#### Animasyon Hız Ayarları
```python
INITIAL_DELAY = 30       # Başlangıç gecikmesi (milisaniye)
SPEED_UP_DECREMENT = 5   # Hız artırım miktarı
MIN_DELAY = 1           # Minimum gecikme
```

#### Top Konfigürasyonları
```python
TOP_KONFIGURASYONLARI = [
    (10, 'Kirmizi'),  # Küçük top
    (20, 'Mavi'),     # Orta top  
    (30, 'Sari')      # Büyük top
]
```

#### Kontrol Butonları
```python
KONTROL_KONFIGURASYONLARI = [
    ("START", 'red', 'hareketi_baslat'),
    ("STOP", 'blue', 'hareketi_durdur'),
    ("RESET", 'yellow', 'sifirla')
]
```
## 🎨 Görsel Efektler

### Top Efektleri
- **Gölge Efekti**: 3D derinlik hissi
- **Gradient Katmanları**: Modern görünüm
- **Parlama Efekti**: Işık yansıması
- **Çarpışma Efekti**: Beyaz halka animasyonu

### Canvas Efektleri
- **Grid Deseni**: Modern arka plan
- **Tema Desteği**: Dark/Light mod
- **Kenar Çarpışması**: Sınır tespiti

## 🔄 Animasyon Döngüsü

Uygulamanın animasyon döngüsü şu adımları içerir:

1. **Pozisyon Güncelleme**: Topların konumlarını güncelle
2. **Kenar Çarpışma Kontrolü**: Canvas sınırlarını kontrol et
3. **Toplar Arası Çarpışma**: Toplar arası mesafeyi hesapla
4. **Efekt Güncelleme**: Görsel efektleri yenile
5. **Tekrarla**: Belirlenen gecikme ile döngüyü tekrarla

## 🐛 Hata Ayıklama

### Yaygın Sorunlar

#### İkonların Gözükmemesi
```bash
# İkonları yeniden oluştur
python icons/create_icons.py
```

#### Tema Değişmiyor
- ttkbootstrap kurulu olduğundan emin olun
- Python sürümünün uyumlu olduğunu kontrol edin

#### Performans Sorunları
- Çok fazla top eklenmemesi önerilir
- Hız ayarlarının aşırı düşük yapılmaması gerekir

## 📄 Lisans

Bu proje [LICENSE](LICENSE) dosyasında belirtilen lisans altında dağıtılmaktadır.
