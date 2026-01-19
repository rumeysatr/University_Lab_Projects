"""
Exam Schedule View - Sınav Programı Görünümü
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime, timedelta
from src.views.base_crud_view import BaseCrudView


class ExamScheduleView(BaseCrudView):    
    title = "📅 Sınav Programı"
    columns = [
        ('id', 'ID', 50),
        ('exam_date', 'Tarih', 100),
        ('time', 'Saat', 100),
        ('course_code', 'Ders Kodu', 100),
        ('course_name', 'Ders Adı', 180),
        ('lecturer_name', 'Öğretim Üyesi', 150),
        ('classrooms', 'Derslikler', 180),
        ('student_count', 'Öğrenci', 70),
        ('status', 'Durum', 100),
    ]
    
    def __init__(self, parent, dashboard):
        self.user_role = dashboard.get_user_role()
        self.user_department_id = dashboard.get_user_department_id()
        
        self.view_only = self.user_role in ['hoca', 'ogrenci']
        
        super().__init__(parent, dashboard)
        
        self._setup_role_based_buttons()
    
    def _create_header(self):
        header_frame = tk.Frame(self, bg='#ecf0f1')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        if self.view_only:
            title_text = "📅 Sınav Programı (Görüntüleme)"
        elif self.user_role == 'bolum_yetkilisi':
            title_text = "📅 Sınav Programı (Bölüm Yönetimi)"
        else:
            title_text = "📅 Sınav Programı Yönetimi"
        
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=('Segoe UI', 20, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(side='left')
        
        self.btn_frame = tk.Frame(header_frame, bg='#ecf0f1')
        self.btn_frame.pack(side='right')
        
        if not self.view_only:
            self.add_btn = tk.Button(
                self.btn_frame,
                text='➕ Ekle',
                font=('Segoe UI', 10),
                bg='#27ae60',
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=self._on_add
            )
            self.add_btn.pack(side='left', padx=5)
            self._add_button_hover(self.add_btn, '#27ae60', '#2ecc71')
            
            self.edit_btn = tk.Button(
                self.btn_frame,
                text='✏️ Düzenle',
                font=('Segoe UI', 10),
                bg='#3498db',
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=self._on_edit
            )
            self.edit_btn.pack(side='left', padx=5)
            self._add_button_hover(self.edit_btn, '#3498db', '#5dade2')
            
            self.delete_btn = tk.Button(
                self.btn_frame,
                text='🗑️ Sil',
                font=('Segoe UI', 10),
                bg='#e74c3c',
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=self._on_delete
            )
            self.delete_btn.pack(side='left', padx=5)
            self._add_button_hover(self.delete_btn, '#e74c3c', '#ec7063')
        
        self.excel_btn = tk.Button(
            self.btn_frame,
            text='Excel İndir',
            font=('Segoe UI', 10),
            bg='#16a085',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self._on_export_excel
        )
        self.excel_btn.pack(side='left', padx=5)
        self._add_button_hover(self.excel_btn, '#16a085', '#1abc9c')
        
        self.refresh_btn = tk.Button(
            self.btn_frame,
            text='🔄 Yenile',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.load_data
        )
        self.refresh_btn.pack(side='left', padx=5)
        self._add_button_hover(self.refresh_btn, '#95a5a6', '#bdc3c7')
    
    def _setup_role_based_buttons(self):
        if self.view_only:
            return
        
        if self.user_role == 'admin':
            bulk_delete_btn = tk.Button(
                self.btn_frame,
                text='🗑️ Toplu Sil',
                font=('Segoe UI', 10),
                bg='#c0392b',
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=self._on_bulk_delete
            )
            bulk_delete_btn.pack(side='left', padx=5)
            self._add_button_hover(bulk_delete_btn, '#c0392b', '#e74c3c')
            
            auto_btn = tk.Button(
                self.btn_frame,
                text='Otomatik Dağıt',
                font=('Segoe UI', 10),
                bg='#9b59b6',
                fg='white',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2',
                command=self._on_auto_schedule
            )
            auto_btn.pack(side='left', padx=5)
            self._add_button_hover(auto_btn, '#9b59b6', '#a569bd')
        
        if self.user_role == 'admin':
            self.data_table.tree.configure(selectmode='extended')
    
    def _on_double_click(self, item):
        if item and not self.view_only:
            self._on_edit()

    def _format_classrooms(self, exam):
        classroom_value = getattr(exam, 'classrooms', None)
        if classroom_value is None:
            classroom_value = getattr(exam, 'classroom_names', None)
        if classroom_value is None:
            classroom_value = getattr(exam, 'classroom_name', None)
        if classroom_value is None:
            classroom_value = getattr(exam, 'classroom', None)

        if isinstance(classroom_value, (list, tuple)):
            names = []
            for item in classroom_value:
                if isinstance(item, dict):
                    name = item.get('name') or item.get('classroom_name')
                else:
                    name = getattr(item, 'name', None) if not isinstance(item, str) else item
                if name:
                    names.append(str(name))
            return ' + '.join(names) if names else '-'

        if isinstance(classroom_value, str):
            return classroom_value if classroom_value.strip() else '-'

        if getattr(exam, 'classroom_name', None):
            return exam.classroom_name
        if getattr(exam, 'faculty_name', None) and getattr(exam, 'classroom_name', None):
            return exam.classroom_name
        return '-'
    
    def get_form_fields(self):
        courses = self.controller.get_all_courses()
        
        if self.user_role == 'bolum_yetkilisi' and self.user_department_id:
            courses = [c for c in courses if c.department_id == self.user_department_id]
        
        course_options = [
            (c.id, f"{c.code} - {c.name} ({c.student_count or 0} öğrenci, {c.exam_duration or 60} dk)")
            for c in courses
            if getattr(c, 'has_exam', True) and c.exam_duration and c.exam_duration > 0
        ]
        
        classrooms = self.controller.get_exam_suitable_classrooms()
        if not classrooms:
            classrooms = self.controller.get_all_classrooms()
        classroom_options = [
            (c.id, f"{c.faculty_name or 'Belirsiz'} - {c.name} (Kapasite: {c.capacity})")
            for c in classrooms
        ]
        
        status_options = [
            ('planned', 'Planlandı'),
            ('confirmed', 'Onaylandı'),
            ('completed', 'Tamamlandı'),
            ('cancelled', 'İptal Edildi')
        ]
        
        exam_type_options = [
            ('midterm', 'Vize'),
            ('final', 'Final'),
            ('makeup', 'Bütünleme'),
            ('quiz', 'Quiz')
        ]
        
        return [
            {
                'name': 'course_id',
                'label': 'Ders',
                'type': 'combo',
                'options': course_options,
                'required': True
            },
            {
                'name': 'classroom_ids',
                'label': 'Derslik(ler)',
                'type': 'multi_combo',
                'options': classroom_options,
                'required': True,
                'height': 6
            },
            {
                'name': 'exam_date',
                'label': 'Sınav Tarihi',
                'type': 'date',
                'required': True
            },
            {
                'name': 'start_time',
                'label': 'Başlangıç Saati',
                'type': 'time',
                'required': True
            },
            {
                'name': 'end_time',
                'label': 'Bitiş Saati',
                'type': 'time',
                'required': True
            },
            {
                'name': 'exam_type',
                'label': 'Sınav Türü',
                'type': 'combo',
                'options': exam_type_options,
                'required': True
            },
            {
                'name': 'status',
                'label': 'Durum',
                'type': 'combo',
                'options': status_options,
                'default': 'planned',
                'required': True
            },
            {
                'name': 'notes',
                'label': 'Notlar',
                'type': 'text',
                'required': False
            }
        ]
    
    def load_data(self, search_term=''):
        """
        Kullanıcı rolüne göre sınav verilerini yükler.
        - Hoca: Kendi derslerinin sınavları
        - Öğrenci: Aldığı derslerin sınavları
        - Bölüm Yetkilisi: Kendi bölümünün sınavları
        - Admin: Tüm sınavlar
        """
        # Kullanıcı bilgilerini al
        user_info = self.dashboard.app.auth_controller.get_current_user()
        
        if self.user_role == 'ogrenci' and user_info:
            # Öğrenci için kişiselleştirilmiş liste
            exams_dict = self.controller.filter_schedule_by_user(user_info)
            # Dict listesini ExamSchedule nesnelerine benzer bir yapıya çevir
            exams = self._convert_dict_to_exam_objects(exams_dict)
        elif self.user_role == 'hoca' and user_info:
            # Hoca için kişiselleştirilmiş liste
            exams_dict = self.controller.filter_schedule_by_user(user_info)
            exams = self._convert_dict_to_exam_objects(exams_dict)
        else:
            # Admin ve Bölüm Yetkilisi için mevcut mantık
            exams = self.controller.get_all_exams()
            
            if self.user_role == 'bolum_yetkilisi' and self.user_department_id:
                all_courses = self.controller.get_all_courses()
                dept_course_ids = [c.id for c in all_courses if c.department_id == self.user_department_id]
                exams = [e for e in exams if e.course_id in dept_course_ids]
        
        status_map = {
            'planned': 'Planlandı',
            'confirmed': 'Onaylandı',
            'completed': 'Tamamlandı',
            'cancelled': 'İptal Edildi'
        }
        
        data = []
        for exam in exams:
            classrooms_display = self._format_classrooms(exam)
            row = {
                'id': exam.id,
                'exam_date': str(exam.exam_date),
                'time': f"{exam.start_time} - {exam.end_time}",
                'start_time': str(exam.start_time),
                'end_time': str(exam.end_time),
                'course_id': exam.course_id,
                'course_code': exam.course_code or '-',
                'course_name': exam.course_name or '-',
                'lecturer_name': exam.lecturer_name or '-',
                'classroom_id': exam.classroom_id,
                'classroom_ids': [exam.classroom_id], 
                'classrooms': classrooms_display,
                'student_count': exam.student_count,
                'exam_type': exam.exam_type,
                'status': status_map.get(exam.status, exam.status),
                'notes': exam.notes or ''
            }
            
            if search_term:
                searchable = f"{row['course_code']} {row['course_name']} {row['lecturer_name']} {row['classrooms']} {row['exam_date']}".lower()
                if search_term not in searchable:
                    continue
            
            data.append(row)
        
        self.data_table.load_data(data)
    
    def _convert_dict_to_exam_objects(self, exams_dict):
        """
        Dict formatındaki sınav listesini ExamSchedule benzeri nesnelere çevirir.
        filter_schedule_by_user'dan gelen dict verileri işlemek için kullanılır.
        """
        class SimpleExam:
            """Basit bir sınav sınıfı - ExamSchedule özelliklerini taşır"""
            def __init__(self, data):
                self.id = data.get('id')
                self.exam_date = data.get('date')
                self.start_time = data.get('start_time', data.get('time', ''))
                self.end_time = data.get('end_time', '')
                self.course_id = data.get('course_id')
                self.course_code = data.get('course_code')
                self.course_name = data.get('course_name')
                self.lecturer_name = data.get('lecturer_name', data.get('lecturer', ''))
                self.classroom_id = None
                self.classroom_name = data.get('classroom_name', data.get('classroom', ''))
                self.student_count = data.get('student_count', 0)
                self.exam_type = data.get('exam_type', 'final')
                self.status = data.get('status', 'planned')
                self.notes = ''
        
        return [SimpleExam(exam) for exam in exams_dict]
    
    def validate_form(self, data):
        if not data.get('course_id'):
            return False, "Ders seçimi zorunludur."
        
        classroom_ids = data.get('classroom_ids', [])
        if not classroom_ids or len(classroom_ids) == 0:
            return False, "En az bir derslik seçimi zorunludur."
        
        if not data.get('exam_date'):
            return False, "Sınav tarihi zorunludur."
        if not data.get('start_time'):
            return False, "Başlangıç saati zorunludur."
        if not data.get('end_time'):
            return False, "Bitiş saati zorunludur."
        
        try:
            exam_date = datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
            if exam_date < date.today():
                return False, "Sınav tarihi geçmiş bir tarih olamaz."
        except ValueError:
            return False, "Geçersiz tarih formatı. YYYY-MM-DD formatında girin."
        
        try:
            start = datetime.strptime(data['start_time'], '%H:%M').time()
            end = datetime.strptime(data['end_time'], '%H:%M').time()
            if start >= end:
                return False, "Bitiş saati başlangıç saatinden sonra olmalıdır."
        except ValueError:
            return False, "Geçersiz saat formatı. HH:MM formatında girin."
        
        try:
            exam_date = datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
            if exam_date.weekday() >= 5:  # 5=Cumartesi, 6=Pazar
                return False, "Sınav tarihi hafta içi bir gün olmalıdır."
        except ValueError:
            pass
        
        return True, ""
    
    def create_item(self, data):
        classroom_ids = data.get('classroom_ids', [])
        
        if len(classroom_ids) == 0:
            return {'success': False, 'message': 'En az bir derslik seçilmelidir.'}
        
        result = self.controller.create_exam({
            'course_id': data['course_id'],
            'classroom_ids': classroom_ids,  # Çoklu derslik listesi
            'exam_date': data['exam_date'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'exam_type': data['exam_type'],
            'status': data.get('status', 'planned'),
            'notes': data.get('notes', '')
        })
        
        return result
    
    def update_item(self, id, data):
        classroom_ids = data.get('classroom_ids', [])
        if isinstance(classroom_ids, list) and len(classroom_ids) > 0:
            classroom_id = classroom_ids[0]
        else:
            classroom_id = data.get('classroom_id')
        
        return self.controller.update_exam(id, {
            'course_id': data['course_id'],
            'classroom_id': classroom_id,
            'exam_date': data['exam_date'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'exam_type': data['exam_type'],
            'status': data.get('status', 'planned'),
            'notes': data.get('notes', '')
        })
    
    def delete_item(self, id):
        return self.controller.delete_exam(id)
    
    def _on_bulk_delete(self):
        if self.user_role != 'admin':
            messagebox.showwarning('Uyarı', 'Bu işlem için yetkiniz yok.')
            return
        
        selected_ids = self.data_table.get_selected_ids()
        
        if not selected_ids:
            messagebox.showwarning(
                'Uyarı',
                'Lütfen silmek için en az bir kayıt seçin.\n\n'
                'İpucu: Ctrl tuşuna basılı tutarak birden fazla satır seçebilirsiniz.'
            )
            return
        
        count = len(selected_ids)
        confirm = messagebox.askyesno(
            'Toplu Silme Onayı',
            f'{count} adet sınavı silmek istediğinize emin misiniz?\n\n'
            'Bu işlem geri alınamaz!'
        )
        
        if not confirm:
            return
        
        success_count = 0
        failed_count = 0
        
        for exam_id in selected_ids:
            try:
                result = self.controller.delete_exam(exam_id)
                if result and result.get('success'):
                    success_count += 1
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1
        
        if failed_count == 0:
            messagebox.showinfo('Başarılı', f'{success_count} sınav başarıyla silindi.')
        else:
            messagebox.showwarning(
                'Kısmi Başarı',
                f'{success_count} sınav silindi, {failed_count} sınav silinemedi.'
            )
        
        self.load_data()
    
    def _on_auto_schedule(self):
        if self.user_role != 'admin':
            messagebox.showwarning('Uyarı', 'Bu işlem için yetkiniz yok.')
            return
        
        dialog = AutoScheduleDialog(self, self.controller)
        dialog.grab_set()

    def _on_export_pdf(self):
        file_path = filedialog.asksaveasfilename(
            title='PDF Kaydet',
            defaultextension='.pdf',
            filetypes=[
                ('PDF Dosyaları', '*.pdf'),
                ('Tüm Dosyalar', '*.*')
            ]
        )
        if not file_path:
            return
        
        try:
            # TODO: implement in ExamScheduleController: export_schedule_pdf(filepath: str) -> dict/None
            result = self.controller.export_schedule_pdf(file_path)
        except AttributeError:
            messagebox.showerror('Hata', 'PDF dışa aktarma için controller yöntemi bulunamadı.')
            return
        except Exception as exc:
            messagebox.showerror('Hata', f'Hata oluştu: {str(exc)}')
            return
        
        if isinstance(result, dict) and not result.get('success', True):
            messagebox.showerror('Hata', result.get('message', 'PDF oluşturulamadı.'))
            return
        
        messagebox.showinfo('Başarılı', 'PDF başarıyla kaydedildi.')

    def _on_export_excel(self):
        file_path = filedialog.asksaveasfilename(
            title='Excel Kaydet',
            defaultextension='.xlsx',
            filetypes=[
                ('Excel Dosyaları', '*.xlsx'),
                ('CSV Dosyaları', '*.csv'),
                ('Tüm Dosyalar', '*.*')
            ]
        )
        if not file_path:
            return
        
        try:
            # TODO: implement in ExamScheduleController: export_schedule_excel(filepath: str) -> dict/None
            result = self.controller.export_schedule_excel(file_path)
        except AttributeError:
            messagebox.showerror('Hata', 'Excel dışa aktarma için controller yöntemi bulunamadı.')
            return
        except Exception as exc:
            messagebox.showerror('Hata', f'Hata oluştu: {str(exc)}')
            return
        
        if isinstance(result, dict) and not result.get('success', True):
            messagebox.showerror('Hata', result.get('message', 'Excel oluşturulamadı.'))
            return
        
        messagebox.showinfo('Başarılı', 'Excel başarıyla kaydedildi.')


class AutoScheduleDialog(tk.Toplevel):    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        self.title('🤖 Otomatik Sınav Planlaması')
        self.geometry('500x450')
        self.resizable(False, False)
        self.configure(bg='#ecf0f1')
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 450) // 2
        self.geometry(f'+{x}+{y}')
        
        self._create_widgets()
    
    def _create_widgets(self):
        title = tk.Label(
            self,
            text='Otomatik Sınav Programı Oluşturma',
            font=('Segoe UI', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title.pack(pady=(20, 10))
        
        form_frame = tk.Frame(self, bg='#ecf0f1')
        form_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(form_frame, text='Başlangıç Tarihi:', font=('Segoe UI', 10), bg='#ecf0f1').pack(anchor='w')
        self.start_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        start_entry = tk.Entry(form_frame, textvariable=self.start_date_var, font=('Segoe UI', 11))
        start_entry.pack(fill='x', pady=(0, 10), ipady=5)
        
        tk.Label(form_frame, text='Bitiş Tarihi:', font=('Segoe UI', 10), bg='#ecf0f1').pack(anchor='w')
        end_date = date.today() + timedelta(days=14)
        self.end_date_var = tk.StringVar(value=end_date.strftime('%Y-%m-%d'))
        end_entry = tk.Entry(form_frame, textvariable=self.end_date_var, font=('Segoe UI', 11))
        end_entry.pack(fill='x', pady=(0, 10), ipady=5)
        
        tk.Label(form_frame, text='Bölüm (Opsiyonel):', font=('Segoe UI', 10), bg='#ecf0f1').pack(anchor='w')
        departments = self.controller.get_all_departments()
        dept_options = ['Tümü'] + [d.name for d in departments if d.is_active]
        self.dept_var = tk.StringVar(value='Tümü')
        dept_combo = ttk.Combobox(form_frame, textvariable=self.dept_var, values=dept_options, state='readonly')
        dept_combo.pack(fill='x', pady=(0, 10), ipady=3)
        self.departments = departments
        
        tk.Label(form_frame, text='Sınav Türü:', font=('Segoe UI', 10), bg='#ecf0f1').pack(anchor='w')
        exam_types = ['Final', 'Vize', 'Bütünleme']
        self.exam_type_var = tk.StringVar(value='Final')
        type_combo = ttk.Combobox(form_frame, textvariable=self.exam_type_var, values=exam_types, state='readonly')
        type_combo.pack(fill='x', pady=(0, 10), ipady=3)
        
        btn_frame = tk.Frame(self, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        generate_btn = tk.Button(
            btn_frame,
            text='🚀 Oluştur',
            font=('Segoe UI', 11),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self._generate
        )
        generate_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text='❌ İptal',
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.destroy
        )
        cancel_btn.pack(side='left', padx=5)
    
    def _generate(self):
        try:
            start_date = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date_var.get(), '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror('Hata', 'Geçersiz tarih formatı. YYYY-MM-DD kullanın.')
            return
        
        if start_date >= end_date:
            messagebox.showerror('Hata', 'Bitiş tarihi başlangıç tarihinden sonra olmalıdır.')
            return
        
        department_id = None
        dept_name = self.dept_var.get()
        if dept_name != 'Tümü':
            for d in self.departments:
                if d.name == dept_name:
                    department_id = d.id
                    break
        
        exam_type_map = {'Final': 'final', 'Vize': 'midterm', 'Bütünleme': 'makeup'}
        exam_type = exam_type_map.get(self.exam_type_var.get(), 'final')
        
        try:
            result = self.controller.generate_auto_schedule(
                start_date, end_date, department_id, exam_type
            )
            
            if isinstance(result, dict):
                success = result.get('success', False)
                message = result.get('message', '')
                failed_count = result.get('failed_count')
                if failed_count is None:
                    failed_count = result.get('unscheduled_count')
                failed_courses = result.get('failed_courses', [])

                if success:
                    if failed_count is None:
                        info_message = 'Sınavlar dağıtıldı!'
                    else:
                        info_message = f'Sınavlar dağıtıldı! {failed_count} sınav yerleşemedi.'
                    messagebox.showinfo('Başarılı', info_message)

                    if failed_count:
                        failed_info = self._format_failed_courses(failed_courses)
                        messagebox.showwarning(
                            'Kısmi Başarı',
                            f'{message}\n\nPlanlanamayan Dersler:\n{failed_info}'
                        )

                    self.parent.load_data()
                    self.destroy()
                else:
                    failed_info = self._format_failed_courses(failed_courses)
                    messagebox.showerror(
                        'Planlama Başarısız',
                        f'{message}\n\nPlanlanamayan Dersler:\n{failed_info}'
                    )
            else:
                if result and result[0]:
                    info_text = 'Sınavlar dağıtıldı!'
                    if len(result) > 1 and result[1]:
                        info_text = f"{info_text}\n{result[1]}"
                    messagebox.showinfo('Başarılı', info_text)
                    self.parent.load_data()
                    self.destroy()
                else:
                    messagebox.showwarning(
                        'Uyarı',
                        result[1] if result else 'Program oluşturulamadı.'
                    )
        except Exception as e:
            messagebox.showerror('Hata', f'Program oluşturulurken hata: {str(e)}')
    
    def _format_failed_courses(self, failed_courses: list) -> str:
        if not failed_courses:
            return "Bilgi yok"
        
        lines = []
        for i, course in enumerate(failed_courses[:10], 1):
            # course dict veya benzeri bir yapı olabilir, string de olabilir
            if isinstance(course, dict):
                code = course.get('code', '?')
                name = course.get('name', '?')
                reason = course.get('reason', 'Bilinmeyen neden')
            elif isinstance(course, str):
                code = course
                name = '?'
                reason = 'Bilinmeyen neden'
            else:
                # Course nesnesi veya diğer tipler
                code = getattr(course, 'code', '?')
                name = getattr(course, 'name', '?')
                reason = getattr(course, 'reason', 'Bilinmeyen neden')
            
            if not code or code == '?':
                code = str(i)
            if not name or name == '?':
                name = 'Bilinmeyen Ders'
            if not reason:
                reason = 'Bilinmeyen neden'
            
            lines.append(f"{i}. {code} - {name}\n   Neden: {reason}")
        
        if len(failed_courses) > 10:
            lines.append(f"\n... ve {len(failed_courses) - 10} ders daha")
        
        return '\n'.join(lines)
