"""
Kontrol Paneli UI Bileşeni
"""
import tkinter as tk
import ttkbootstrap as tb
from PIL import Image, ImageTk
from config.settings import (
    TOP_KONFIGURASYONLARI,
    KONTROL_KONFIGURASYONLARI,
    SELECTION_COLOR_ACTIVE,
    PANEL_COLORS,
    MODERN_COLORS
)


class ControlPanel:
    """Kontrol paneli UI bileşenini yöneten sınıf"""
    
    
    def __init__(self, master, app_instance):
        """
        ControlPanel constructor
        
        Args:
            master: Tkinter parent widget
            app_instance: Ana uygulama instance'ı (callback'ler için)
        """
        self.master = master
        self.app = app_instance
        
        # Kontrol Çerçevesi - Modern arka plan
        self.kontrol_cercevesi = tk.Frame(master, bg=PANEL_COLORS['bg'], relief=tk.RAISED, bd=1)
        self.kontrol_cercevesi.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.color_sq_refs = {}  # Renk kare widget referansları
        self.btn_refs = {}  # Kontrol buton referansları
        self.hiz_gostergesi = None  # Hız göstergesi referansı
        self.icons = {}  # İkon referansları
        
        self._ikonlari_yukle()
        self._arayuz_olustur()
    
    def _ikonlari_yukle(self):
        """Buton ikonlarını yükler"""
        try:
            # İkonları yükle ve boyutlandır
            icon_size = (16, 16)
            
            self.icons['play'] = ImageTk.PhotoImage(
                Image.open('icons/play.png').resize(icon_size, Image.Resampling.LANCZOS)
            )
            self.icons['stop'] = ImageTk.PhotoImage(
                Image.open('icons/stop.png').resize(icon_size, Image.Resampling.LANCZOS)
            )
            self.icons['reset'] = ImageTk.PhotoImage(
                Image.open('icons/reset.png').resize(icon_size, Image.Resampling.LANCZOS)
            )
            self.icons['speed'] = ImageTk.PhotoImage(
                Image.open('icons/speed.png').resize(icon_size, Image.Resampling.LANCZOS)
            )
            self.icons['theme'] = ImageTk.PhotoImage(
                Image.open('icons/theme.png').resize(icon_size, Image.Resampling.LANCZOS)
            )
        except Exception as e:
            print(f"İkonlar yüklenirken hata: {e}")
            self.icons = {}
    
    def _arayuz_olustur(self):
        """Kontrol arayüzünü oluşturur (Yuvarlak Renk Butonları, Türkçe Metinler)."""
        
        # Ana grid çerçevesi ve konfigürasyon
        main_frame = self._ana_cerceve_olustur()
        
        # Boyut seçimi bölümü
        self._boyut_secimi_olustur(main_frame)
        
        # Renk seçimi bölümü
        self._renk_secimi_olustur(main_frame)
        
        # Aksiyon butonları bölümü
        self._aksiyon_butonlari_olustur(main_frame)
        
        # Hız kontrolü bölümü
        self._hiz_kontrolu_olustur(main_frame)
        
        # Tema değiştirme bölümü
        self._tema_degistirme_olustur(main_frame)
    
    def _ana_cerceve_olustur(self):
        """Ana grid çerçevesini oluşturur ve konfigürasyonunu yapar."""
        main_frame = tk.Frame(self.kontrol_cercevesi, bg=PANEL_COLORS['bg'])
        main_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # Grid konfigürasyonu
        self.kontrol_cercevesi.grid_rowconfigure(0, weight=1)
        self.kontrol_cercevesi.grid_columnconfigure(0, weight=1)
        
        return main_frame
    
    def _boyut_secimi_olustur(self, main_frame):
        """Boyut seçimi bölümünü oluşturur."""
        boyut_baslik = tb.Label(main_frame, text="Boyut:", font=("Segoe UI", 12, "bold"), bootstyle="primary")
        boyut_baslik.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        
        # Boyut butonları
        for i, (r, _) in enumerate(TOP_KONFIGURASYONLARI):
            col = i
            size_text = f"Boyut {r}"
            size_btn = tb.Button(main_frame,
                                text=size_text,
                                bootstyle="primary-outline",
                                width=12,
                                command=lambda yaricap=r: self.app.top_ekle(yaricap))
            size_btn.grid(row=1, column=col, padx=10, pady=5, sticky="ew")
    
    def _renk_secimi_olustur(self, main_frame):
        """Renk seçimi bölümünü oluşturur."""
        renk_baslik = tb.Label(main_frame, text="Renkler:", font=("Segoe UI", 12, "bold"), bootstyle="primary")
        renk_baslik.grid(row=2, column=0, columnspan=3, pady=(20, 10), sticky="w")
        
        # Renk butonları için frame
        renk_frame = tk.Frame(main_frame, bg=PANEL_COLORS['bg'])
        renk_frame.grid(row=3, column=0, columnspan=3, pady=5, sticky="ew")
        
        # Yuvarlak renk butonları oluştur
        for i, renk in enumerate(MODERN_COLORS):
            col = i
            
            # Yuvarlak renk butonu için Canvas
            color_canvas = tk.Canvas(renk_frame, width=40, height=40, bg=PANEL_COLORS['bg'], highlightthickness=0)
            color_canvas.grid(row=0, column=col, padx=10, pady=5)
            
            # Yuvarlak daire çiz
            color_canvas.create_oval(5, 5, 35, 35, fill=renk, outline="", tags="color_circle")
            
            # Tıklama olayı ekle
            color_canvas.bind("<Button-1>", lambda e, r=renk: self.app.renk_sec(r))
            
            # Hover efekti için
            color_canvas.bind("<Enter>", lambda e, canvas=color_canvas: canvas.configure(cursor="hand2"))
            color_canvas.bind("<Leave>", lambda e, canvas=color_canvas: canvas.configure(cursor=""))
            
            self.color_sq_refs[renk] = color_canvas
    
    def _aksiyon_butonlari_olustur(self, main_frame):
        """Aksiyon butonları bölümünü oluşturur."""
        # Türkçe metinler
        turkce_metinler = {
            "START": "BAŞLAT",
            "STOP": "DURDUR",
            "RESET": "SIFIRLA"
        }
        
        # Bootstrap stilini belirle
        bootstyle_map = {
            "START": "success",
            "STOP": "danger",
            "RESET": "warning"
        }
        
        # İkonu belirle
        icon_map = {
            "START": self.icons.get('play'),
            "STOP": self.icons.get('stop'),
            "RESET": self.icons.get('reset')
        }
        
        # Aksiyon butonları için döngü
        for i, config in enumerate(KONTROL_KONFIGURASYONLARI):
            col = i
            btn_text = config[0]
            btn_func_name = config[2]
            
            bootstyle = bootstyle_map.get(btn_text, "primary")
            icon = icon_map.get(btn_text)
            turkce_text = turkce_metinler.get(btn_text, btn_text)
            
            if icon:
                button_text = f" {turkce_text}"
                action_btn = tb.Button(main_frame,
                                      text=button_text,
                                      image=icon,
                                      compound=tk.LEFT,
                                      bootstyle=bootstyle,
                                      width=12,
                                      command=lambda f=btn_func_name: getattr(self.app, f)())
            else:
                action_btn = tb.Button(main_frame,
                                      text=turkce_text,
                                      bootstyle=bootstyle,
                                      width=12,
                                      command=lambda f=btn_func_name: getattr(self.app, f)())
            
            action_btn.grid(row=4, column=col, padx=10, pady=5, sticky="ew")
            self.btn_refs[btn_text] = action_btn
    
    def _hiz_kontrolu_olustur(self, main_frame):
        """Hız göstergesi ve hızlandır butonunu oluşturur."""
        # Hız göstergesi frame'i
        speed_frame = tk.Frame(main_frame, bg=PANEL_COLORS['bg'])
        speed_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        # Hız göstergesi Label
        self.hiz_gostergesi = tb.Label(speed_frame,
                                      text="Hız: 1.0x",
                                      bootstyle="info",
                                      font=("Segoe UI", 10, "bold"))
        self.hiz_gostergesi.pack(side=tk.LEFT, padx=(0, 10))
        
        # Hızlandır butonu
        speed_icon = self.icons.get('speed')
        if speed_icon:
            self.speed_btn = tb.Button(speed_frame,
                                      text=" Hızlandır",
                                      image=speed_icon,
                                      compound=tk.LEFT,
                                      bootstyle="info",
                                      width=25)
        else:
            self.speed_btn = tb.Button(speed_frame,
                                      text="Hızlandır",
                                      bootstyle="info",
                                      width=25)
        
        self.speed_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.speed_btn.configure(command=self.app.hizlandir)
    
    def _tema_degistirme_olustur(self, main_frame):
        """Tema değiştirme butonunu oluşturur."""
        # Tema butonu frame'i
        theme_frame = tk.Frame(main_frame, bg=PANEL_COLORS['bg'])
        theme_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        # Tema değiştirme butonu
        theme_icon = self.icons.get('theme')
        if theme_icon:
            self.theme_btn = tb.Button(theme_frame,
                                  text=" Tema",
                                  image=theme_icon,
                                  compound=tk.LEFT,
                                  bootstyle="secondary",
                                  width=25,
                                  command=self.app.tema_degistir)
        else:
            self.theme_btn = tb.Button(theme_frame,
                                  text="Tema",
                                  bootstyle="secondary",
                                  width=25,
                                  command=self.app.tema_degistir)
        
        self.theme_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    
    
    def guncelle_secim_goster(self, secilen_renk):
        """Seçili renk butonunu görsel olarak vurgular."""
        for renk, canvas_widget in self.color_sq_refs.items():
            if renk == secilen_renk:
                # Seçili renk için kalın çerçeve ekle
                canvas_widget.delete("selection")
                canvas_widget.create_oval(3, 3, 37, 37, outline="white", width=3, tags="selection")
            else:
                # Seçili olmayan renk için çerçeveyi kaldır
                canvas_widget.delete("selection")
    
    def guncelle_hiz_gostergesi(self, hiz_seviyesi):
        """Hız göstergesini günceller."""
        if self.hiz_gostergesi:
            self.hiz_gostergesi.config(text=f"Speed: {hiz_seviyesi}x")
    
    def guncelle_tema_butonu(self, mevcut_tema):
        """Tema butonunu günceller."""
        if hasattr(self, 'theme_btn'):
            # Tema adına göre buton metnini güncelle
            tema_adi = "Dark" if mevcut_tema == "superhero" else "Light"
            self.theme_btn.config(text=f" {tema_adi}")