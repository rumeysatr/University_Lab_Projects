import tkinter as tk
from tkinter import Text
from datetime import datetime
import re

class FindSpeed:
    def __init__(self, master, root_x, root_y):
        self.master = master
        self.top = tk.Toplevel(master)
        
        self.start_time = None

        # Yeni pencereyi ana pencerenin �zerine a�acak �ekilde konumland�r
        self.top.title("FIND SPEED")
        self.top.resizable(False, False)
        self.top.geometry("810x650+100+150")

        # Sayfa ba�l���
        self.label = tk.Label(
            self.top,
            text="FIND SPEED",
            fg="white",
            background="navy",
            font=("Georgia", 20, "underline", "bold")
        )
        self.label.place(x= 313, y= 25)
        
        self.top.config(background="navy")
        self.text = tk.Message(self.top, text="You can write a sentence or text", fg="light grey", width=2000, font=("Arial", 14, "bold", "italic"), background="navy")
        self.text.place(x = 250, y=90)
        
        self.inputtxt = Text(self.top, height=10, width=35, bg="white")
        self.inputtxt.place(x = 265, y = 150)
        self.inputtxt.bind("<FocusIn>", self.start_timing)  # Tıklandığında zamanı başlat

        self.Output = Text(self.top, height=7, width=40, bg="light cyan")
        self.Output.place(x = 250, y = 400)

        # 'Answer' butonu
        self.Display = tk.Button(self.top, height=2, width=20, text="Answer", command=self.display_text)
        self.Display.place(x= 330, y = 330)

        # Ana menüye dön butonu
        self.simple_button = tk.Button(self.top, width=20, text="Back to the Main Menu", command=self.return_to_main_menu)
        self.simple_button.place(x = 330, y = 590)
        
    def start_timing(self, event):
        """Girdi kutusu focus aldığında zamanlayıcıyı başlatır."""
        self.start_time = datetime.now()
        self.dtimestamp = self.start_time.timestamp()
    
    def find_speed(self, text):
        """Yazma hızını saniye başına harf ve süre cinsinden hesaplar."""
        if not self.start_time:
            return "Error"

        end_time = datetime.now()
        dtimestamp1 = end_time.timestamp()

        # Metindeki harf sayısını bul (boşlukları hariç tutarak)
        letter_count = len(re.findall(r'\w', text))  # Boşlukları çıkarır
        self.words = (letter_count)/(dtimestamp1 - self.dtimestamp)
        # Sonuç metnini oluştur
        result = (
            f"Your score: {dtimestamp1 - self.dtimestamp:.7f} seconds.\n"
            f"{self.words:.1f} letters per second."
        )

        return result


    def display_text(self):
        """Yazma hızı ve süreyi gösterir."""
        input_text = self.inputtxt.get("1.0", "end-1c")  # Girdi kutusundan metni al
        result = self.find_speed(input_text)
        self.Output.delete("1.0", "end")  # Çıktı kutusunu temizle
        self.Output.insert("end", result)  # Sonucu çıktı kutusuna yazdır


    def return_to_main_menu(self):
        # �st pencereyi kapat�r ve ana pencereyi yeniden g�sterir
        self.top.destroy()
        self.master.deiconify()