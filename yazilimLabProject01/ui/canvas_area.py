"""
Canvas Alanı ve Animasyon Yönetimi
"""
import tkinter as tk
from config.settings import KANVAS_GENISLIK, KANVAS_YUKSEKLIK, CANVAS_COLORS


class CanvasArea:
    """Canvas alanını yöneten sınıf"""
    
    
    def __init__(self, master):
        """
        CanvasArea constructor
        
        Args:
            master: Tkinter parent widget
        """
        self.master = master
        
        # Modern görünüm için Frame container
        self.container_frame = tk.Frame(master, bg=CANVAS_COLORS['dark_gray'])
        self.container_frame.pack(pady=10, padx=10)
        
        # Canvas (Çizim Alanı) - modern renk paleti ile
        self.canvas = tk.Canvas(self.container_frame,
                                width=KANVAS_GENISLIK,
                                height=KANVAS_YUKSEKLIK,
                                bg=CANVAS_COLORS['whitesmoke'],
                                highlightthickness=2,
                                highlightbackground=CANVAS_COLORS['dark_gray'],
                                borderwidth=0)
        self.canvas.pack(padx=2, pady=2)
        
        # Grid desenini çiz
        self._draw_grid_pattern()
    
    def get_canvas(self):
        """Canvas nesnesini döndürür"""
        return self.canvas
    
    def get_dimensions(self):
        """
        Canvas boyutlarını döndürür
        
        Returns:
            tuple: (genişlik, yükseklik)
        """
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Canvas henüz render olmadıysa default değerleri döndür
        if canvas_width == 1 or canvas_height == 1:
            self.master.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
        
        return canvas_width, canvas_height
    
    def clear_balls(self):
        """Canvas'taki tüm topları ve efektlerini temizler"""
        self.canvas.delete("top")
        self.canvas.delete("shadow")         # Gölge etiketini sil
        self.canvas.delete("gradient")       # Gradient etiketini sil
        self.canvas.delete("highlight")      # Parlama etiketini sil
        self.canvas.delete("collision_effect") # Çarpışma efektlerini de sil
    
    def move_ball(self, ball_id, dx, dy):
        """
        Top'u belirtilen miktarda hareket ettirir
        
        Args:
            ball_id: Canvas üzerindeki top id'si
            dx: X ekseninde hareket miktarı
            dy: Y ekseninde hareket miktarı
        """
        self.canvas.move(ball_id, dx, dy)
    
    def get_ball_coords(self, ball_id):
        """
        Top'un koordinatlarını döndürür
        
        Args:
            ball_id: Canvas üzerindeki top id'si
            
        Returns:
            tuple: (x1, y1, x2, y2) koordinatları
        """
        return self.canvas.coords(ball_id)
    
    def _draw_grid_pattern(self):
        """Canvas'a modern grid deseni çizer"""
        grid_size = 20  # Grid hücre boyutu
        
        # Mevcut temayı kontrol et
        try:
            current_theme = self.master.style.theme_use()
            is_dark_theme = current_theme in ["superhero", "darkly", "cyborg"]
        except:
            is_dark_theme = False
        
        # Temaya göre grid rengi belirle
        if is_dark_theme:
            # Dark theme için saydam grid rengi
            grid_color = "#404040"  # Daha koyu ve saydam gri
        else:
            grid_color = CANVAS_COLORS['light_gray']
        
        # Dikey çizgiler
        for x in range(0, KANVAS_GENISLIK + 1, grid_size):
            self.canvas.create_line(x, 0, x, KANVAS_YUKSEKLIK,
                                   fill=grid_color,
                                   width=1,
                                   tags="grid")
        
        # Yatay çizgiler
        for y in range(0, KANVAS_YUKSEKLIK + 1, grid_size):
            self.canvas.create_line(0, y, KANVAS_GENISLIK, y,
                                   fill=grid_color,
                                   width=1,
                                   tags="grid")
        
        # Grid desenini arka planda tut
        self.canvas.tag_lower("grid")