import tkinter as tk

from changeAs import changeAs
from print_letters import PrintLettersPage
from print_split import PrintSplit
from re_assemble import ReAssemblePage
from rev_print import RevPrint
from find_speed import FindSpeed
from total_vow import TotalVow

class MainMenu:
    root_x = 0
    root_y = 0
    def __init__(self, root):
        self.root = root
        self.root.title("TEXT MANIPULATION PROGRAM")
        self.root.geometry("810x650+100+150")
        self.root.resizable(False, False)
        self.root.config(background="navy")

        self.label = tk.Label(
            root,
            text="MENU",
            fg="white",
            background="navy",
            font=("Georgia", 40, "underline", "bold")
        )
        self.label.place(x= 300, y= 25)
        
        self.root.text = tk.Message(root, text="pick a program whatever you want to do", fg="light grey", width=2000, font=("Arial", 14, "bold", "italic"), background="navy")
        self.root.text.place(x = 210, y=100)
        
        # Butonlarý oluþtur
        self.button1 = tk.Button(root, text='print letters\none below\nthe other', fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white", 
                width=12, height=7, command=self.open_button1_page)
        self.button1.place(x = 40, y =175)

        self.button2 = tk.Button(root, text='print reverse of\ntext and\nwords',
                fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white",
                width=12, height=7, command=self.open_button2_page)
        self.button2.place(x = 240, y =175)

        self.button3 = tk.Button(root,  text="change all\nof 'a' in\n text to 'A'",
                fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white", 
                width=12, height=7, command=self.open_button3_page)
        self.button3.place(x = 440, y =175)

        self.button4 = tk.Button(root, text='print split',
                fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white", 
                width=12, height=7, command=self.open_button4_page)
        self.button4.place(x = 640, y =175)
        
        self.button5 = tk.Button(root, text='re\nassemble\nof words',
                fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white", 
                width=12, height=7, command=self.open_button5_page)
        self.button5.place(x = 40, y =400)
        
        self.button6 = tk.Button(root, text='total\nnumber\nof vowels',
                fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white", 
                width=12, height=7, command=self.open_button6_page)
        self.button6.place(x = 240, y =400)
        
        self.button7 = tk.Button(root, text='calculate\ntyping\nspeed',
                fg="navy",font =("Montserrat", 12, "bold"), activebackground="navy", activeforeground="white", 
                width=12, height=7, command=self.open_button7_page)
        self.button7.place(x = 440, y =400)
        
        exit_button = tk.Button(root, text="EXIT", fg="white", font=("Montserrat", 12, "bold"), background="red",
                     activebackground="white", activeforeground="red", width=8, height=5, command=root.quit)
        exit_button.place(x = 655, y=420)
    
    def open_button1_page(self):
        # Ana menüyü gizle
        self.root.withdraw()
        # Button 1 sayfasýný aç
        self.button1_page = PrintLettersPage(self.root, self.root_x, self.root_y)

    def open_button2_page(self):
        self.root.withdraw()
        self.button2_page = RevPrint(self.root, self.root_x, self.root_y)

    def open_button3_page(self):
        self.root.withdraw()
        self.button3_page = changeAs(self.root, self.root_x, self.root_y)

    def open_button4_page(self):
        self.root.withdraw()
        self.button4_page = PrintSplit(self.root, self.root_x, self.root_y)

    def open_button5_page(self):
        self.root.withdraw()
        self.button5_page = ReAssemblePage(self.root, self.root_x, self.root_y)

    def open_button6_page(self):
        self.root.withdraw()
        self.button6_page = TotalVow(self.root, self.root_x, self.root_y)

    def open_button7_page(self):
        self.root.withdraw()
        self.button7_page = FindSpeed(self.root, self.root_x, self.root_y)

# Ana pencereyi olu�tur ve s�n�f� ba�lat

root = tk.Tk()
page = MainMenu(root)
root.mainloop()