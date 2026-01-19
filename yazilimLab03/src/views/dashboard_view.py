"""
Dashboard View - Ana Panel Görünümü
Sol menü ve içerik alanını yönetir
Rol bazlı içerik gösterimi sağlar
"""

import tkinter as tk
from tkinter import ttk
from src.views.components.sidebar import Sidebar
from src.controllers.dashboard_controller import DashboardController


class DashboardView(tk.Frame):    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app 
        self.controller = DashboardController(self)
        self.current_view = None
        
        self.user_info = self.app.auth_controller.get_current_user()
        self.user_role = self.user_info.get('role', 'ogrenci') if self.user_info else 'ogrenci'
        self.user_department_id = self.user_info.get('department_id') if self.user_info else None
        
        self._create_widgets()
        self._show_home()
    
    def _create_widgets(self):
        self.sidebar = Sidebar(self, on_menu_click=self._on_menu_click, user_role=self.user_role)
        self.sidebar.pack(side='left', fill='y')
        
        user_frame = tk.Frame(self.sidebar, bg='#1a252f')
        user_frame.pack(side='bottom', fill='x')
        
        if self.user_info:
            user_label = tk.Label(
                user_frame,
                text=f"👤 {self.user_info.get('username', '')}",
                font=('Segoe UI', 9),
                bg='#1a252f',
                fg='#bdc3c7'
            )
            user_label.pack(pady=5)
        
        logout_btn = tk.Button(
            user_frame,
            text='🚪 Çıkış',
            font=('Segoe UI', 10),
            bg='#c0392b',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2',
            command=self._logout
        )
        logout_btn.pack(pady=10)
        
        self.content_frame = tk.Frame(self, bg='#ecf0f1')
        self.content_frame.pack(side='right', fill='both', expand=True)
    
    def _on_menu_click(self, key, view_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_view = None
        
        if key == 'dashboard':
            self._show_home()
        elif key == 'faculties':
            if self.user_role == 'admin':
                from src.views.faculty_view import FacultyView
                self.current_view = FacultyView(self.content_frame, self)
        elif key == 'departments':
            if self.user_role == 'admin':
                from src.views.department_view import DepartmentView
                self.current_view = DepartmentView(self.content_frame, self)
        elif key == 'classrooms':
            if self.user_role in ['admin', 'bolum_yetkilisi']:
                from src.views.classroom_view import ClassroomView
                self.current_view = ClassroomView(self.content_frame, self)
        elif key == 'lecturers':
            if self.user_role in ['admin', 'bolum_yetkilisi']:
                from src.views.lecturer_view import LecturerView
                self.current_view = LecturerView(self.content_frame, self)
        elif key == 'courses':
            if self.user_role in ['admin', 'bolum_yetkilisi']:
                from src.views.course_view import CourseView
                self.current_view = CourseView(self.content_frame, self)
        elif key == 'import_view':
            if self.user_role in ['admin', 'bolum_yetkilisi']:
                from src.views.import_view import ImportView
                self.current_view = ImportView(self.content_frame, self)
        elif key == 'student_lists':
            if self.user_role in ['admin', 'bolum_yetkilisi']:
                from src.views.course_view import CourseView
                self.current_view = CourseView(self.content_frame, self)
        elif key == 'schedule':
            from src.views.exam_schedule_view import ExamScheduleView
            self.current_view = ExamScheduleView(self.content_frame, self)
        elif key == 'reports':
            if self.user_role == 'admin':
                from src.views.reports_view import ReportsView
                self.current_view = ReportsView(self.content_frame, self)
        
        if self.current_view:
            self.current_view.pack(fill='both', expand=True)
    
    def _show_home(self):
        if self.user_role == 'admin':
            self._show_admin_home()
        elif self.user_role == 'bolum_yetkilisi':
            self._show_bolum_yetkilisi_home()
        elif self.user_role == 'hoca':
            self._show_hoca_home()
        elif self.user_role == 'ogrenci':
            self._show_ogrenci_home()
        else:
            self._show_admin_home()
    
    def _show_admin_home(self):
        home_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        home_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        title = tk.Label(
            home_frame,
            text='📊 Sistem Özeti (Admin)',
            font=('Segoe UI', 24, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title.pack(anchor='w', pady=(0, 30))
        
        # Otomatik sınav programı oluşturma butonu
        actions_frame = tk.Frame(home_frame, bg='#ecf0f1')
        actions_frame.pack(fill='x', pady=(0, 20))
        
        auto_schedule_btn = tk.Button(
            actions_frame,
            text='🤖 Otomatik Sınav Programı Oluştur',
            font=('Segoe UI', 12, 'bold'),
            bg='#8e44ad',
            fg='white',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self._show_auto_schedule_dialog
        )
        auto_schedule_btn.pack(anchor='w')
        
        stats_frame = tk.Frame(home_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x')
        
        stats = [
            ('🏛️ Fakülteler', len(self.controller.get_all_faculties()), '#3498db'),
            ('📚 Bölümler', len(self.controller.get_all_departments()), '#9b59b6'),
            ('🚪 Derslikler', len(self.controller.get_all_classrooms()), '#1abc9c'),
            ('👨‍🏫 Öğretim Üyeleri', len(self.controller.get_all_lecturers()), '#e67e22'),
            ('📖 Dersler', len(self.controller.get_all_courses()), '#e74c3c'),
            ('📅 Planlanan Sınavlar', len(self.controller.get_all_exams()), '#2ecc71'),
        ]
        
        for i, (label, count, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, padx=20, pady=20)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            count_label = tk.Label(
                card, 
                text=str(count), 
                font=('Segoe UI', 36, 'bold'), 
                bg=color, 
                fg='white'
            )
            count_label.pack()
            
            text_label = tk.Label(
                card, 
                text=label, 
                font=('Segoe UI', 12), 
                bg=color, 
                fg='white'
            )
            text_label.pack()
        
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)
        
        self._show_upcoming_exams(home_frame)
    
    def _show_bolum_yetkilisi_home(self):
        home_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        home_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        department_name = "Bölümünüz"
        if self.user_department_id:
            departments = self.controller.get_all_departments()
            for dept in departments:
                if dept.id == self.user_department_id:
                    department_name = dept.name
                    break
        
        title = tk.Label(
            home_frame,
            text=f'📊 {department_name} - Bölüm Özeti',
            font=('Segoe UI', 24, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title.pack(anchor='w', pady=(0, 30))
        
        # Otomatik sınav programı oluşturma butonu
        actions_frame = tk.Frame(home_frame, bg='#ecf0f1')
        actions_frame.pack(fill='x', pady=(0, 20))
        
        auto_schedule_btn = tk.Button(
            actions_frame,
            text='🤖 Otomatik Sınav Programı Oluştur (Bölüm)',
            font=('Segoe UI', 12, 'bold'),
            bg='#8e44ad',
            fg='white',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=lambda: self._show_auto_schedule_dialog(department_id=self.user_department_id)
        )
        auto_schedule_btn.pack(anchor='w')
        
        stats_frame = tk.Frame(home_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x')
        
        all_lecturers = self.controller.get_all_lecturers()
        dept_lecturers = [l for l in all_lecturers if l.department_id == self.user_department_id]
        
        all_courses = self.controller.get_all_courses()
        dept_courses = [c for c in all_courses if c.department_id == self.user_department_id]
        
        all_exams = self.controller.get_all_exams()
        dept_course_ids = [c.id for c in dept_courses]
        dept_exams = [e for e in all_exams if e.course_id in dept_course_ids]
        
        stats = [
            ('👨‍🏫 Öğretim Üyeleri', len(dept_lecturers), '#e67e22'),
            ('📖 Dersler', len(dept_courses), '#e74c3c'),
            ('📅 Planlanan Sınavlar', len(dept_exams), '#2ecc71'),
        ]
        
        for i, (label, count, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, padx=20, pady=20)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            
            count_label = tk.Label(
                card, 
                text=str(count), 
                font=('Segoe UI', 36, 'bold'), 
                bg=color, 
                fg='white'
            )
            count_label.pack()
            
            text_label = tk.Label(
                card, 
                text=label, 
                font=('Segoe UI', 12), 
                bg=color, 
                fg='white'
            )
            text_label.pack()
        
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)
        
        info_label = tk.Label(
            home_frame,
            text='ℹ️ Bölüm yetkilisi olarak sadece kendi bölümünüze ait öğretim üyelerini, dersleri ve sınav programını yönetebilirsiniz.',
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            wraplength=600
        )
        info_label.pack(anchor='w', pady=(20, 0))
        
        self._show_upcoming_exams(home_frame, department_filter=self.user_department_id)
    
    def _show_hoca_home(self):
        """Hoca için ana sayfa - sadece kendi derslerinin sınav programını görüntüleme"""
        home_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        home_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        lecturer_name = self.user_info.get('full_name') or self.user_info.get('username') if self.user_info else "Hoca"
        
        title = tk.Label(
            home_frame,
            text=f'📅 Sınav Programınız - {lecturer_name}',
            font=('Segoe UI', 24, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title.pack(anchor='w', pady=(0, 30))
        
        info_label = tk.Label(
            home_frame,
            text='ℹ️ Öğretim üyesi olarak verdiğiniz derslerin sınav programını buradan görüntüleyebilirsiniz. Listede sadece kendi derslerinizin sınavları gösterilmektedir.',
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wraplength=600
        )
        info_label.pack(anchor='w', pady=(0, 20))
        
        # Kullanıcı bazlı filtreleme ile sınavları göster
        self._show_upcoming_exams(home_frame, use_user_filter=True)
    
    def _show_ogrenci_home(self):
        """Öğrenci için ana sayfa - sadece aldığı derslerin sınav programı görüntüleme"""
        home_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        home_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        student_name = self.user_info.get('full_name') or self.user_info.get('username') if self.user_info else "Öğrenci"
        
        title = tk.Label(
            home_frame,
            text=f'📅 Sınav Programınız - {student_name}',
            font=('Segoe UI', 24, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title.pack(anchor='w', pady=(0, 30))
        
        info_label = tk.Label(
            home_frame,
            text='ℹ️ Öğrenci olarak kayıtlı olduğunuz derslerin sınav programını buradan görüntüleyebilirsiniz. Listede sadece aldığınız derslerin sınavları gösterilmektedir.',
            font=('Segoe UI', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wraplength=600
        )
        info_label.pack(anchor='w', pady=(0, 20))
        
        # Kullanıcı bazlı filtreleme ile sınavları göster
        self._show_upcoming_exams(home_frame, use_user_filter=True)
    
    def _show_upcoming_exams(self, parent, department_filter=None, use_user_filter=False):
        """
        Kullanıcı bazlı sınav gösterimi.
        
        Args:
            parent: Ebeveyn widget
            department_filter: Bölüm filtresi (eski yöntem, backward compatibility)
            use_user_filter: Kullanıcı bazlı filtreleme kullan
        """
        upcoming_title = tk.Label(
            parent,
            text='📅 Yaklaşan Sınavlar',
            font=('Segoe UI', 18, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        upcoming_title.pack(anchor='w', pady=(30, 15))
        
        exams_frame = tk.Frame(parent, bg='white', bd=1, relief='solid')
        exams_frame.pack(fill='x')
        
        # Kullanıcı bazlı filtreleme
        if use_user_filter and self.user_info:
            upcoming = self.controller.filter_schedule_by_user(self.user_info)
        else:
            upcoming = self.controller.get_upcoming_exams(days=7)
            
            if department_filter:
                all_courses = self.controller.get_all_courses()
                dept_course_ids = [c.id for c in all_courses if c.department_id == department_filter]
                upcoming = [e for e in upcoming if e.get('course_id') in dept_course_ids]
        
        if not upcoming:
            no_exam_label = tk.Label(
                exams_frame,
                text='Yaklaşan sınav bulunmamaktadır.',
                font=('Segoe UI', 11),
                bg='white',
                fg='#7f8c8d',
                pady=20
            )
            no_exam_label.pack()
        else:
            for exam in upcoming[:5]:
                exam_row = tk.Frame(exams_frame, bg='white', pady=8, padx=15)
                exam_row.pack(fill='x', padx=1, pady=1)
                
                date_label = tk.Label(
                    exam_row,
                    text=f"📆 {exam['date']}",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg='#3498db',
                    width=12,
                    anchor='w'
                )
                date_label.pack(side='left')
                
                time_label = tk.Label(
                    exam_row,
                    text=f"⏰ {exam['time']}",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg='#e67e22',
                    width=10,
                    anchor='w'
                )
                time_label.pack(side='left')
                
                course_label = tk.Label(
                    exam_row,
                    text=f"{exam['course_code']} - {exam['course_name']}",
                    font=('Segoe UI', 10, 'bold'),
                    bg='white',
                    fg='#2c3e50',
                    anchor='w'
                )
                course_label.pack(side='left', fill='x', expand=True)
                
                room_label = tk.Label(
                    exam_row,
                    text=f"📍 {exam['classroom']}",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg='#7f8c8d'
                )
                room_label.pack(side='right')
    
    def _show_auto_schedule_dialog(self, department_id=None):
        """Otomatik sınav programı oluşturma dialog penceresi"""
        from datetime import date, timedelta
        from tkinter import simpledialog, messagebox
        
        # Dialog penceresi oluştur
        dialog = tk.Toplevel(self)
        dialog.title('Otomatik Sınav Programı Oluştur')
        dialog.geometry('450x350')
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self)
        dialog.grab_set()
        
        # Merkezleme
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Başlık
        title_label = tk.Label(
            dialog,
            text='🤖 Otomatik Sınav Programı Oluştur',
            font=('Segoe UI', 16, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(pady=(20, 10))
        
        info_label = tk.Label(
            dialog,
            text='Greedy + Backtracking algoritması ile sınav programı oluşturulacak.\n'
                 'Dersler, öğretim üyeleri ve derslikler çakışmayacak şekilde dağıtılır.',
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            justify='left'
        )
        info_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='#ecf0f1', padx=30)
        form_frame.pack(fill='x')
        
        # Başlangıç tarihi
        start_date_frame = tk.Frame(form_frame, bg='#ecf0f1')
        start_date_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            start_date_frame,
            text='Başlangıç Tarihi:',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            width=15,
            anchor='w'
        ).pack(side='left')
        
        today = date.today()
        start_date_var = tk.StringVar(value=today.strftime('%Y-%m-%d'))
        start_date_entry = tk.Entry(
            start_date_frame,
            textvariable=start_date_var,
            font=('Segoe UI', 10),
            width=15
        )
        start_date_entry.pack(side='left')
        
        # Bitiş tarihi
        end_date_frame = tk.Frame(form_frame, bg='#ecf0f1')
        end_date_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            end_date_frame,
            text='Bitiş Tarihi:',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            width=15,
            anchor='w'
        ).pack(side='left')
        
        two_weeks = today + timedelta(days=14)
        end_date_var = tk.StringVar(value=two_weeks.strftime('%Y-%m-%d'))
        end_date_entry = tk.Entry(
            end_date_frame,
            textvariable=end_date_var,
            font=('Segoe UI', 10),
            width=15
        )
        end_date_entry.pack(side='left')
        
        # Sınav tipi
        exam_type_frame = tk.Frame(form_frame, bg='#ecf0f1')
        exam_type_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            exam_type_frame,
            text='Sınav Tipi:',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            width=15,
            anchor='w'
        ).pack(side='left')
        
        exam_type_var = tk.StringVar(value='final')
        exam_type_combo = ttk.Combobox(
            exam_type_frame,
            textvariable=exam_type_var,
            values=['final', 'midterm', 'quiz', 'makeup'],
            state='readonly',
            width=12
        )
        exam_type_combo.pack(side='left')
        
        # Mevcut planları temizle
        clear_var = tk.BooleanVar(value=True)
        clear_check = tk.Checkbutton(
            form_frame,
            text='Mevcut planlanmış sınavları temizle',
            variable=clear_var,
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Segoe UI', 10),
            activebackground='#ecf0f1'
        )
        clear_check.pack(anchor='w', pady=(5, 15))
        
        # Buton frame
        button_frame = tk.Frame(dialog, bg='#ecf0f1')
        button_frame.pack(pady=(0, 20))
        
        def on_generate():
            start = start_date_var.get()
            end = end_date_var.get()
            exam_type = exam_type_var.get()
            clear = clear_var.get()
            
            if not start or not end:
                messagebox.showwarning('Uyarı', 'Lütfen başlangıç ve bitiş tarihi girin.')
                return
            
            try:
                result = self.controller.generate_auto_schedule(
                    start_date=start,
                    end_date=end,
                    department_id=department_id,
                    exam_type=exam_type
                )
                
                if clear and result.get('success'):
                    from src.repositories.exam_schedule_repository import ExamScheduleRepository
                    repo = ExamScheduleRepository()
                    repo.delete_planned()
                
                dialog.destroy()
                
                # Sonuç göster
                self._show_schedule_result(result)
                
            except Exception as e:
                messagebox.showerror('Hata', f'Sınav programı oluşturulurken hata: {str(e)}')
        
        generate_btn = tk.Button(
            button_frame,
            text='🚀 Oluştur',
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=on_generate
        )
        generate_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text='İptal',
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=dialog.destroy
        )
        cancel_btn.pack(side='left', padx=5)
    
    def _show_schedule_result(self, result):
        """Sınav programı oluşturma sonucunu gösterir"""
        from tkinter import scrolledtext
        
        dialog = tk.Toplevel(self)
        dialog.title('Sınav Programı Oluşturma Sonucu')
        dialog.geometry('600x500')
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self)
        dialog.grab_set()
        
        # Merkezleme
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Başlık
        if result.get('success'):
            title = '✅ Sınav Programı Başarıyla Oluşturuldu'
            color = '#27ae60'
        elif result.get('scheduled_count', 0) > 0:
            title = '⚠️ Sınav Programı Kısmen Oluşturuldu'
            color = '#f39c12'
        else:
            title = '❌ Sınav Programı Oluşturulamadı'
            color = '#e74c3c'
        
        title_label = tk.Label(
            dialog,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            bg='#ecf0f1',
            fg=color
        )
        title_label.pack(pady=(20, 10))
        
        # Özet
        summary_text = f"Planlanan: {result.get('scheduled_count', 0)}\n"
        summary_text += f"Başarısız: {result.get('failed_count', 0)}\n"
        
        stats = result.get('statistics', {})
        if stats:
            summary_text += f"\n📊 İstatistikler:\n"
            summary_text += f"  Kullanılan Gün: {stats.get('days_used', 0)}\n"
            summary_text += f"  Kullanılan Derslik: {stats.get('classrooms_used', 0)}\n"
            summary_text += f"  Ortalama Sınav/Gün: {stats.get('avg_exams_per_day', 0):.1f}\n"
        
        summary_label = tk.Label(
            dialog,
            text=summary_text,
            font=('Segoe UI', 11),
            bg='white',
            fg='#2c3e50',
            justify='left',
            padx=15,
            pady=10,
            relief='solid',
            bd=1
        )
        summary_label.pack(fill='x', padx=20, pady=(0, 15))
        
        # Mesaj
        message = result.get('message', '')
        if message:
            msg_label = tk.Label(
                dialog,
                text=message,
                font=('Segoe UI', 10),
                bg='#ecf0f1',
                fg='#2c3e50',
                wraplength=550,
                justify='left'
            )
            msg_label.pack(fill='x', padx=20, pady=(0, 10))
        
        # Başarısız dersler
        failed = result.get('failed_courses', [])
        if failed:
            tk.Label(
                dialog,
                text='❌ Planlanamayan Dersler:',
                font=('Segoe UI', 11, 'bold'),
                bg='#ecf0f1',
                fg='#e74c3c',
                anchor='w'
            ).pack(fill='x', padx=20, pady=(10, 5))
            
            failed_text = scrolledtext.ScrolledText(
                dialog,
                height=8,
                font=('Consolas', 9),
                bg='#fff5f5'
            )
            failed_text.pack(fill='both', expand=True, padx=20, pady=(0, 10))
            
            for course in failed:
                code = course.get('code', 'Bilinmiyor')
                name = course.get('name', '')
                reason = course.get('reason', 'Sebep belirtilmemiş')
                failed_text.insert('end', f"• {code} - {name}\n  Sebep: {reason}\n\n")
            
            failed_text.config(state='disabled')
        
        # Kapat butonu
        close_btn = tk.Button(
            dialog,
            text='Kapat',
            font=('Segoe UI', 11),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=dialog.destroy
        )
        close_btn.pack(pady=(10, 20))

    def _logout(self):
        self.app.auth_controller.logout()
        self.app.show_login()
    
    def refresh(self):
        self._on_menu_click('dashboard', 'DashboardView')
    
    def get_user_department_id(self):
        return self.user_department_id
    
    def get_user_role(self):
        return self.user_role
