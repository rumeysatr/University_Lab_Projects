import tkinter as tk
from tkinter import *

class PrintSplit:
    def __init__(self, master, root_x, root_y):
        self.master = master
        self.top = tk.Toplevel(master)

        # Yeni pencereyi ana pencereyi üzerine açacak şekilde konumlandır
        self.top.title("PRINT SPLIT")
        self.top.resizable(False, False)
        self.top.geometry("810x650+100+150")

        # Sayfa ba�l���
        self.label = tk.Label(
            self.top,
            text= "PRINT SPLIT",
            fg = "white",
            background="navy",
            font=("Georgia", 20, "underline", "bold")
        )
        self.label.place(x= 310, y= 25)
        
        self.top.config(background="navy")
        self.text = tk.Message(self.top, text="You can write a sentence or text", fg="light grey", width=2000, font=("Arial", 14, "bold", "italic"), background="navy")
        self.text.place(x = 250, y=90)
        
        self.inputtxt = Text(self.top, height=10, width=35, bg="white")
        self.inputtxt.place(x = 265, y = 150)

        self.Output = Text(self.top, height=10, width=25, bg="light cyan")
        self.Output.place(x = 300, y = 400)

        # Display butonu
        self.Display = tk.Button(self.top, height=2, width=20, text="Answer", command=self.display_text)
        self.Display.place(x= 330, y = 330)

        # Ana Men�ye d�n butonu
        self.simple_button = tk.Button(self.top, width=20, text="Back to the Main Menu", command=self.return_to_main_menu)
        self.simple_button.place(x = 330, y = 590)

    def print_split(self, text):
        words = text.split()
        return words

    def display_text(self):
        input_text = self.inputtxt.get("1.0", "end-1c")
        words = self.print_split(input_text)
        self.Output.delete("1.0", "end")
        formatedtext = str(words)
        self.Output.insert("end", formatedtext)

    def return_to_main_menu(self):
        self.top.destroy()
        self.master.deiconify()  # Ana men�y� tekrar g�ster