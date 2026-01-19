"""
Uygulama Konfigürasyon Sabitleri
"""

# Kanvas Ayarları
KANVAS_GENISLIK = 450
KANVAS_YUKSEKLIK = 400

# Animasyon Hız Ayarları
INITIAL_DELAY = 30
SPEED_UP_DECREMENT = 5
MIN_DELAY = 1

# Renk Ayarları
SELECTION_COLOR_ACTIVE = 'lightgreen'

# Top Renk Paleti
BALL_COLORS = [
    '#639ad3',  # mavi tonu
    '#ac8eab',  # pembe tonu
    '#a4aca1',  # yeşil tonu
    '#778899',  # slate gray
    '#B0C4DE'   # light steel blue
]

# Panel Renk Paleti
PANEL_COLORS = {
    'bg': '#F5F5F5',           # whitesmoke
    'button_normal': '#B0C4DE', # light steel blue
    'button_hover': '#778899',  # slate gray
    'button_active': '#A9A9A9', # dark gray
    'border': '#A9A9A9',        # dark gray
    'selection_highlight': '#B0C4DE' # light steel blue
}

# Kontrol Paneli Modern Renkler
MODERN_COLORS = [
    '#FF6B6B',  # kırmızı tonu
    '#4ECDC4',  # yeşil tonu
    '#45B7D1'   # mavi tonu
]

# Canvas Renk Paleti
CANVAS_COLORS = {
    'slate_gray': '#778899',
    'light_steel_blue': '#B0C4DE',
    'light_gray': '#D3D3D3',
    'whitesmoke': '#F5F5F5',
    'dark_gray': '#A9A9A9'
}

# Top Konfigürasyonları (Yarıçap, Renk Etiketi)
TOP_KONFIGURASYONLARI = [
    (10, 'Kirmizi'),  # Küçük
    (20, 'Mavi'),     # Orta
    (30, 'Sari')      # Büyük
]

# Kontrol Buton Konfigürasyonları (Metin, Arka Plan Rengi, Fonksiyon Adı)
KONTROL_KONFIGURASYONLARI = [
    ("START", 'red', 'hareketi_baslat'),
    ("STOP", 'blue', 'hareketi_durdur'),
    ("RESET", 'yellow', 'sifirla')
]