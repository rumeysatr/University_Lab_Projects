"""
Top (Ball) Varlık Sınıfı ve Hareket Mantığı
"""
import random
from config.settings import BALL_COLORS


class Ball:
    """Top varlığını temsil eden sınıf"""
    
    def __init__(self, canvas_id, radius, color, x, y):
        """
        Ball constructor
        
        Args:
            canvas_id: Canvas üzerindeki top'un ana id'si
            radius: Top'un yarıçapı
            color: Top'un rengi
            x: Başlangıç x konumu
            y: Başlangıç y konumu
        """
        self.id = canvas_id
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.vx = random.uniform(1.0, 3.0) * random.choice([-1, 1])
        self.vy = random.uniform(1.0, 3.0) * random.choice([-1, 1])
        
        # Efekt için ek canvas elementleri
        self.shadow_id = None
        self.gradient_ids = []
        self.highlight_id = None
        self.collision_effect_id = None
        self.is_colliding = False
        self.collision_timer = 0
    
    def to_dict(self):
        """Top'u dictionary formatına çevirir"""
        return {
            'id': self.id,
            'vx': self.vx,
            'vy': self.vy,
            'r': self.radius,
            'x': self.x,
            'y': self.y,
            'color': self.color
        }
    
    def create_shadow_effect(self, canvas):
        """Gölge efekti oluşturur"""
        shadow_offset = 3
        shadow_x1 = self.x - self.radius + shadow_offset
        shadow_y1 = self.y - self.radius + shadow_offset
        shadow_x2 = self.x + self.radius + shadow_offset
        shadow_y2 = self.y + self.radius + shadow_offset
        
        self.shadow_id = canvas.create_oval(
            shadow_x1, shadow_y1, shadow_x2, shadow_y2,
            fill='#333333',
            outline='',
            tags="shadow"
        )
        canvas.tag_lower(self.shadow_id)  # Gölgeyi arka plana gönder
    
    def create_gradient_layers(self, canvas):
        """Gradient efektleri için çoklu katmanlar oluşturur"""
        # Ana top katmanı (zaten var)
        # Gradient için daha koyu kenar katmanları
        gradient_steps = 3
        for i in range(gradient_steps):
            factor = 1 - (i * 0.15)  # Her katmanı biraz daha koyu yap
            adjusted_radius = self.radius - (i * 2)
            
            if adjusted_radius > 0:
                # Rengi koyulaştır
                darker_color = self._darken_color(self.color, factor)
                
                x1 = self.x - adjusted_radius
                y1 = self.y - adjusted_radius
                x2 = self.x + adjusted_radius
                y2 = self.y + adjusted_radius
                
                gradient_id = canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=darker_color,
                    outline='',
                    tags="gradient"
                )
                self.gradient_ids.append(gradient_id)
    
    def create_highlight_effect(self, canvas):
        """3D parlama efekti oluşturur"""
        # Parlaklık için üst sol köşede küçük bir oval
        highlight_radius = self.radius * 0.3
        highlight_x = self.x - self.radius * 0.3
        highlight_y = self.y - self.radius * 0.3
        
        self.highlight_id = canvas.create_oval(
            highlight_x - highlight_radius,
            highlight_y - highlight_radius,
            highlight_x + highlight_radius,
            highlight_y + highlight_radius,
            fill='white',
            outline='',
            tags="highlight",
            stipple='gray50'  # Yarı saydam efekt
        )
    
    def create_collision_effect(self, canvas):
        """Çarpışma efekti oluşturur"""
        if self.collision_effect_id:
            canvas.delete(self.collision_effect_id)
        
        # Parlama halkası efekti
        effect_radius = self.radius + 5
        self.collision_effect_id = canvas.create_oval(
            self.x - effect_radius,
            self.y - effect_radius,
            self.x + effect_radius,
            self.y + effect_radius,
            fill='',
            outline='white',
            width=3,
            tags="collision_effect"
        )
        self.is_colliding = True
        self.collision_timer = 10  # 10 frame boyunca göster
    
    def update_collision_effect(self, canvas):
        """Çarpışma efektini günceller"""
        if self.is_colliding and self.collision_timer > 0:
            self.collision_timer -= 1
            if self.collision_timer == 0:
                if self.collision_effect_id:
                    canvas.delete(self.collision_effect_id)
                    self.collision_effect_id = None
                self.is_colliding = False
    
    def _darken_color(self, hex_color, factor):
        """Hex rengini koyulaştırır"""
        # Hex'i RGB'ye çevir
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Koyulaştır
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # RGB'ye geri çevir
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def update_position(self, canvas, dx, dy):
        """Topun pozisyonunu ve tüm efektlerini günceller"""
        self.x += dx
        self.y += dy
        
        # Ana topu hareket ettir
        canvas.coords(
            self.id,
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius
        )
        
        # Gölgeyi hareket ettir
        if self.shadow_id:
            shadow_offset = 3
            canvas.coords(
                self.shadow_id,
                self.x - self.radius + shadow_offset, 
                self.y - self.radius + shadow_offset,
                self.x + self.radius + shadow_offset, 
                self.y + self.radius + shadow_offset
            )
        
        # Gradient katmanlarını hareket ettir
        for i, gradient_id in enumerate(self.gradient_ids):
            adjusted_radius = self.radius - (i * 2)
            if adjusted_radius > 0:
                canvas.coords(
                    gradient_id,
                    self.x - adjusted_radius, self.y - adjusted_radius,
                    self.x + adjusted_radius, self.y + adjusted_radius
                )
        
        # Parlama efektini hareket ettir
        if self.highlight_id:
            highlight_radius = self.radius * 0.3
            highlight_x = self.x - self.radius * 0.3
            highlight_y = self.y - self.radius * 0.3
            canvas.coords(
                self.highlight_id,
                highlight_x - highlight_radius,
                highlight_y - highlight_radius,
                highlight_x + highlight_radius,
                highlight_y + highlight_radius
            )
        
        # Çarpışma efektini güncelle
        if self.collision_effect_id:
            effect_radius = self.radius + 5
            canvas.coords(
                self.collision_effect_id,
                self.x - effect_radius,
                self.y - effect_radius,
                self.x + effect_radius,
                self.y + effect_radius
            )
        
        # Çarpışma efekt timer'ını güncelle
        self.update_collision_effect(canvas)
    
    @staticmethod
    def create_random_ball(canvas, radius, color, canvas_width, canvas_height):
        """
        Rastgele konumda modern efektlerle bir top oluşturur
        
        Args:
            canvas: Tkinter Canvas nesnesi
            radius: Top yarıçapı
            color: Top rengi (eğer None ise paletten seçilir)
            canvas_width: Canvas genişliği
            canvas_height: Canvas yüksekliği
            
        Returns:
            Ball: Yeni oluşturulan top nesnesi
        """
        # Renk belirle
        if color is None or color in ['red', 'blue', 'yellow']:
            color = random.choice(BALL_COLORS)
        
        x = random.randint(radius + 10, canvas_width - radius - 10)
        y = random.randint(radius + 10, canvas_height - radius - 10)
        
        x1, y1 = x - radius, y - radius
        x2, y2 = x + radius, y + radius
        
        # Ana topu oluştur
        ball_id = canvas.create_oval(
            x1, y1, x2, y2, 
            fill=color, 
            tags="top", 
            outline=''
        )
        
        # Ball nesnesini oluştur
        ball = Ball(ball_id, radius, color, x, y)
        
        # Efektleri ekle
        ball.create_shadow_effect(canvas)
        ball.create_gradient_layers(canvas)
        ball.create_highlight_effect(canvas)
        
        # Z-order'ı ayarla (gölge en altta, parlama en üstte)
        if ball.shadow_id:
            canvas.tag_lower(ball.shadow_id)
        for gradient_id in ball.gradient_ids:
            canvas.tag_lower(gradient_id, ball.id)
        if ball.highlight_id:
            canvas.tag_raise(ball.highlight_id)
        
        return ball