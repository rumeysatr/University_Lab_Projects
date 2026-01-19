import tkinter as tk
from tkinter import ttk


class Sidebar(tk.Frame):    
    MENU_ITEMS_BY_ROLE = {
        'admin': [
            ('dashboard', '🏠 Ana Sayfa', 'DashboardView'),
            ('faculties', '🏢 Fakülteler', 'FacultyView'),
            ('departments', '📚 Bölümler', 'DepartmentView'),
            ('classrooms', '🚪 Derslikler', 'ClassroomView'),
            ('lecturers', '👨‍🏫 Öğretim Üyeleri', 'LecturerView'),
            ('courses', '📖 Dersler', 'CourseView'),
            ('schedule', '📅 Sınav Programı', 'ExamScheduleView'),
            ('reports', '📊 Raporlar', 'ReportsView'),
        ],
        'bolum_yetkilisi': [
            ('dashboard', '🏠 Ana Sayfa', 'DashboardView'),
            ('lecturers', '👨‍🏫 Öğretim Üyeleri', 'LecturerView'),
            ('courses', '📖 Dersler', 'CourseView'),
            ('schedule', '📅 Sınav Programı', 'ExamScheduleView'),
        ],
        'hoca': [
            ('dashboard', '🏠 Ana Sayfa', 'DashboardView'),
            ('schedule', '📅 Sınav Programı', 'ExamScheduleView'),
        ],
        'ogrenci': [
            ('dashboard', '🏠 Ana Sayfa', 'DashboardView'),
            ('schedule', '📅 Sınav Programı', 'ExamScheduleView'),
        ],
    }
    
    def __init__(self, parent, on_menu_click=None, user_role='admin'):
        super().__init__(parent, bg='#2c3e50', width=220)
        self.pack_propagate(False)
        self.on_menu_click = on_menu_click
        self.user_role = user_role
        
        self.menu_items = self.MENU_ITEMS_BY_ROLE.get(user_role, self.MENU_ITEMS_BY_ROLE['ogrenci'])
        
        self._create_widgets()
    
    def _create_widgets(self):
        title_frame = tk.Frame(self, bg='#1a252f', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text='📋 Sınav Sistemi',
            font=('Segoe UI', 14, 'bold'),
            bg='#1a252f',
            fg='white'
        )
        title_label.pack(expand=True)
        
        role_names = {
            'admin': '👑 Admin',
            'bolum_yetkilisi': '🎓 Bölüm Yetkilisi',
            'hoca': '👨‍🏫 Öğretim Üyesi',
            'ogrenci': '👨‍🎓 Öğrenci'
        }
        role_display = role_names.get(self.user_role, self.user_role)
        
        role_frame = tk.Frame(self, bg='#34495e', height=30)
        role_frame.pack(fill='x')
        role_frame.pack_propagate(False)
        
        role_label = tk.Label(
            role_frame,
            text=role_display,
            font=('Segoe UI', 9),
            bg='#34495e',
            fg='#ecf0f1'
        )
        role_label.pack(expand=True)
        
        for key, text, view_name in self.menu_items:
            btn = tk.Button(
                self,
                text=text,
                font=('Segoe UI', 11),
                bg='#2c3e50',
                fg='white',
                activebackground='#34495e',
                activeforeground='white',
                bd=0,
                padx=20,
                pady=12,
                anchor='w',
                cursor='hand2',
                command=lambda k=key, v=view_name: self._on_click(k, v)
            )
            btn.pack(fill='x')
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#34495e'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#2c3e50'))
    
    def _on_click(self, key, view_name):
        if self.on_menu_click:
            self.on_menu_click(key, view_name)
