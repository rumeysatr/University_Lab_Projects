import tkinter as tk
from tkinter import Text

class ReAssemblePage:
    def __init__(self, master, root_x, root_y):
        self.master = master
        self.top = tk.Toplevel(master)

        # Yeni pencereyi ana pencerenin üzerine a�acak �ekilde konumland�r
        self.top.title("RE ASSEMBLE")
        self.top.resizable(False, False)
        self.top.geometry("810x650+100+150")

        # Sayfa baslığı
        self.label = tk.Label(
            self.top,
            text= "RE ASSEMBLE OF WORDS",
            fg = "white",
            background="navy",
            font=("Georgia", 20, "underline", "bold")
        )
        self.label.place(x= 217, y= 25)
        
        self.top.config(background="navy")
        self.text = tk.Message(self.top, text="You can write a sentence or text", fg="light grey", width=2000, font=("Arial", 14, "bold", "italic"), background="navy")
        self.text.place(x = 250, y=90)
        
        self.inputtxt = Text(self.top, height=10, width=35, bg="white")
        self.inputtxt.place(x = 265, y = 150)

        self.Output = Text(self.top, height=10, width=25, bg="light cyan")
        self.Output.place(x = 300, y = 400)

        # 'Answer' butonu
        self.Display = tk.Button(self.top, height=2, width=20, text="Answer", command=self.display_text)
        self.Display.place(x= 330, y = 330)

        # Ana menüye dön butonu
        self.simple_button = tk.Button(self.top, width=20, text="Back to the Main Menu", command=self.return_to_main_menu)
        self.simple_button.place(x = 330, y = 590)

    def re_assemble(self, text):
        ntext = text.replace(" ", "")
        return ntext

    def display_text(self):
        # Giri� metnini al ve ters �evirerek ��k��a ekle
        input_text = self.inputtxt.get("1.0", "end-1c")
        reversed_text = self.re_assemble(input_text)
        self.Output.delete("1.0", "end")
        self.Output.insert("end", reversed_text)

    def return_to_main_menu(self):
        # �st pencereyi kapat�r ve ana pencereyi yeniden g�sterir
        self.top.destroy()
        self.master.deiconify()