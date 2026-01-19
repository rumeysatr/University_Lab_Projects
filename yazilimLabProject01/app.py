import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox

from config.settings import INITIAL_DELAY, SPEED_UP_DECREMENT, MIN_DELAY
from models.ball import Ball
from ui.canvas_area import CanvasArea
from ui.control_panel import ControlPanel


class TopAnimasyonUygulamasi:
    
    def __init__(self, master):
        self.master = master
        master.title("Top Animasyonu")
        
        self.toplar = []
        self.animasyon_aktif = False
        self.hiz_gecikmesi = INITIAL_DELAY
        self.hiz_seviyesi = 1.0
        self.animasyon_after_id = None
        self.secilen_renk = "#3369a3"
        
        self.mevcut_tema = "superhero"
        self.tema_secenekleri = ["superhero", "litera"]
        
        self.canvas_area = CanvasArea(master)
        self.canvas = self.canvas_area.get_canvas()
        
        self.control_panel = ControlPanel(master, self)
        
        self.control_panel.guncelle_secim_goster(self.secilen_renk)
    
    
    def renk_sec(self, yeni_renk):
        self.secilen_renk = yeni_renk
        self.control_panel.guncelle_secim_goster(self.secilen_renk)
    
    def top_ekle(self, yaricap):        
        if not self.animasyon_aktif:
            messagebox.showinfo("Durum", "Lütfen önce BAŞLAT butonuna basarak animasyonu başlatın.")
            return
        
        renk = self.secilen_renk
        
        canvas_width, canvas_height = self.canvas_area.get_dimensions()
        
        ball = Ball.create_random_ball(
            self.canvas,
            yaricap,
            renk,
            canvas_width,
            canvas_height
        )
        
        self.toplar.append(ball)
    
    
    def _toplari_hareket_ettir(self):
        if not self.animasyon_aktif:
            return
        
        canvas_width, canvas_height = self.canvas_area.get_dimensions()
        
        self._top_pozisyonlarini_guncelle(canvas_width, canvas_height)
        
        self._check_ball_collisions()
        
        self._carpisma_efektlerini_guncelle()
        
        self.animasyon_after_id = self.master.after(self.hiz_gecikmesi, self._toplari_hareket_ettir)
    
    def _top_pozisyonlarini_guncelle(self, canvas_width, canvas_height):
        for top in self.toplar:
            top.update_position(self.canvas, top.vx, top.vy)
            
            self._kenar_carpismalarini_kontrol_et(top, canvas_width, canvas_height)
    
    def _kenar_carpismalarini_kontrol_et(self, top, canvas_width, canvas_height):
        x1 = top.x - top.radius
        x2 = top.x + top.radius
        y1 = top.y - top.radius
        y2 = top.y + top.radius
        
        collision_occurred = False
        
        if x1 <= 0 or x2 >= canvas_width:
            top.vx *= -1
            collision_occurred = True
            if x1 < 0:
                top.x = top.radius
            elif x2 > canvas_width:
                top.x = canvas_width - top.radius
        
        if y1 <= 0 or y2 >= canvas_height:
            top.vy *= -1
            collision_occurred = True
            if y1 < 0:
                top.y = top.radius
            elif y2 > canvas_height:
                top.y = canvas_height - top.radius
        
        if collision_occurred:
            top.create_collision_effect(self.canvas)
    
    def _carpisma_efektlerini_guncelle(self):
        for top in self.toplar:
            top.update_collision_effect(self.canvas)
    
    def _check_ball_collisions(self):
        for i in range(len(self.toplar)):
            for j in range(i + 1, len(self.toplar)):
                top1 = self.toplar[i]
                top2 = self.toplar[j]
                
                dx = top1.x - top2.x
                dy = top1.y - top2.y
                distance = (dx**2 + dy**2)**0.5
                
                if distance < top1.radius + top2.radius:
                    top1.create_collision_effect(self.canvas)
                    top2.create_collision_effect(self.canvas)
                    
                    top1.vx, top2.vx = top2.vx, top1.vx
                    top1.vy, top2.vy = top2.vy, top1.vy
                    
                    overlap = top1.radius + top2.radius - distance
                    if distance > 0:
                        dx_norm = dx / distance
                        dy_norm = dy / distance
                        
                        top1.x += dx_norm * overlap * 0.5
                        top1.y += dy_norm * overlap * 0.5
                        top2.x -= dx_norm * overlap * 0.5
                        top2.y -= dy_norm * overlap * 0.5
    
    
    def hareketi_baslat(self):
        if not self.animasyon_aktif:
            self.animasyon_aktif = True
            self.control_panel.btn_refs["START"].config(state=tk.DISABLED)
            self.control_panel.btn_refs["STOP"].config(state=tk.NORMAL)
            self._toplari_hareket_ettir()
    
    def hareketi_durdur(self):
        if self.animasyon_aktif:
            self.animasyon_aktif = False
            if self.animasyon_after_id:
                self.master.after_cancel(self.animasyon_after_id)
                self.animasyon_after_id = None
            
            self.control_panel.btn_refs["START"].config(state=tk.NORMAL)
            self.control_panel.btn_refs["STOP"].config(state=tk.DISABLED)
    
    def sifirla(self):
        self.hareketi_durdur()
        self.canvas_area.clear_balls()
        self.toplar = []
        self.hiz_gecikmesi = INITIAL_DELAY
        self.hiz_seviyesi = 1.0
        self.control_panel.guncelle_hiz_gostergesi(self.hiz_seviyesi)
        
        self.control_panel.btn_refs["START"].config(state=tk.NORMAL)
        self.control_panel.btn_refs["STOP"].config(state=tk.DISABLED)
    
    def hiz_seviyesini_hesapla(self):
        return round(INITIAL_DELAY / self.hiz_gecikmesi, 1)
    
    def hizlandir(self):
        yeni_gecikme = self.hiz_gecikmesi - SPEED_UP_DECREMENT
        
        if yeni_gecikme >= MIN_DELAY:
            self.hiz_gecikmesi = yeni_gecikme
        elif self.hiz_gecikmesi > MIN_DELAY:
            self.hiz_gecikmesi = MIN_DELAY
        
        self.hiz_seviyesi = self.hiz_seviyesini_hesapla()
        
        self.control_panel.guncelle_hiz_gostergesi(self.hiz_seviyesi)
    
    def tema_degistir(self):
        mevcut_index = self.tema_secenekleri.index(self.mevcut_tema)
        
        yeni_index = (mevcut_index + 1) % len(self.tema_secenekleri)
        yeni_tema = self.tema_secenekleri[yeni_index]
        
        self.mevcut_tema = yeni_tema
        
        self.master.style.theme_use(yeni_tema)
        
        self.control_panel.guncelle_tema_butonu(yeni_tema)


def main():
    root = tb.Window(themename="superhero")
    root.resizable(False, False)
    
    try:
        root.update()
    except tk.TclError:
        pass
    
    uygulama = TopAnimasyonUygulamasi(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()