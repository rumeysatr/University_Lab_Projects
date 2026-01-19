"""
Classroom View - Derslik Yönetimi Görünümü
Derslik CRUD işlemlerini yönetir
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_crud_view import BaseCrudView


class ClassroomView(BaseCrudView):    
    title = "🚪 Derslik Yönetimi"
    columns = [
        ('id', 'ID', 50),
        ('name', 'Derslik Adı', 150),
        ('faculty_name', 'Fakülte', 200),
        ('capacity', 'Kapasite', 80),
        ('has_computer', 'Bilgisayar', 80),
        ('is_suitable', 'Sınav Uygun', 80),
    ]
    
    def __init__(self, parent, controller):
        self.faculties = []
        self.filter_suitable_only = tk.BooleanVar(value=False)
        super().__init__(parent, controller)
    
    def _create_search_bar(self):
        search_frame = tk.Frame(self, bg='#ecf0f1')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        search_label = tk.Label(
            search_frame,
            text='🔍',
            font=('Segoe UI', 12),
            bg='#ecf0f1'
        )
        search_label.pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search)
        
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            width=40,
            bd=1,
            relief='solid'
        )
        self.search_entry.pack(side='left', padx=10, ipady=5)
        
        clear_btn = tk.Button(
            search_frame,
            text='✖',
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            bd=0,
            cursor='hand2',
            command=lambda: self.search_var.set('')
        )
        clear_btn.pack(side='left')
        
        filter_frame = tk.Frame(self, bg='#ecf0f1')
        filter_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        separator = ttk.Separator(filter_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
        
        filter_inner_frame = tk.Frame(filter_frame, bg='#ecf0f1')
        filter_inner_frame.pack(fill='x')
        
        filter_label = tk.Label(
            filter_inner_frame,
            text='🔍 Filtreleme:',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        filter_label.pack(side='left', padx=(0, 10))
        
        self.suitable_checkbox = tk.Checkbutton(
            filter_inner_frame,
            text="Sadece Sınav Yapılabilecek Derslikleri Göster",
            variable=self.filter_suitable_only,
            command=self._on_filter_change,
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            activebackground='#ecf0f1',
            fg='#2c3e50',
            selectcolor='#ffffff'
        )
        self.suitable_checkbox.pack(side='left', padx=10)
    
    def _on_filter_change(self):
        self.load_data(self.search_var.get().lower() if hasattr(self, 'search_var') else '')
    
    def get_form_fields(self):
        self.faculties = self.controller.get_all_faculties()
        faculty_options = [(f.id, f.name) for f in self.faculties]
        
        return [
            {
                'name': 'name',
                'label': 'Derslik Adı',
                'type': 'entry',
                'required': True
            },
            {
                'name': 'faculty_id',
                'label': 'Fakülte',
                'type': 'combo',
                'options': faculty_options,
                'required': True
            },
            {
                'name': 'capacity',
                'label': 'Kapasite (Öğrenci)',
                'type': 'spinbox',
                'min': 1,
                'max': 500,
                'default': 30,
                'required': True
            },
            {
                'name': 'has_computer',
                'label': 'Bilgisayar Var',
                'type': 'checkbox',
                'default': True
            },
            {
                'name': 'is_suitable',
                'label': 'Sınav Yapılabilir',
                'type': 'checkbox',
                'default': True
            }
        ]
    
    def load_data(self, search_term=''):
        if self.filter_suitable_only.get():
            classrooms = self.controller.get_exam_suitable_classrooms()
        else:
            classrooms = self.controller.get_all_classrooms()
        
        data = []
        for classroom in classrooms:
            row = {
                'id': classroom.id,
                'name': classroom.name,
                'faculty_name': classroom.faculty_name if classroom.faculty_name else 'Belirsiz',
                'capacity': classroom.capacity,
                'has_computer': '✓' if classroom.has_computer else '✗',
                'is_suitable': '✓' if classroom.is_suitable else '✗'
            }
            
            if search_term:
                searchable = f"{row['name']} {row['faculty_name']}".lower()
                if search_term not in searchable:
                    continue
            
            data.append(row)
        
        self.data_table.load_data(data)
    
    def validate_form(self, data):
        if not data.get('name'):
            return False, "Derslik adı zorunludur."
        if not data.get('faculty_id'):
            return False, "Fakülte seçimi zorunludur."
        
        capacity = data.get('capacity', 0)
        
        if capacity < 1:
            return False, "Kapasite en az 1 olmalıdır."
        
        return True, ""
    
    def create_item(self, data):
        return self.controller.create_classroom({
            'name': data['name'],
            'faculty_id': data['faculty_id'],
            'capacity': data['capacity'],
            'has_computer': data.get('has_computer', False),
            'is_suitable': data.get('is_suitable', True)
        })
    
    def update_item(self, id, data):
        return self.controller.update_classroom(id, {
            'name': data['name'],
            'faculty_id': data['faculty_id'],
            'capacity': data['capacity'],
            'has_computer': data.get('has_computer', False),
            'is_suitable': data.get('is_suitable', True)
        })
    
    def delete_item(self, id):
        return self.controller.delete_classroom(id)
    
    def get_edit_data(self, item_id):
        classrooms = self.controller.get_all_classrooms()
        for classroom in classrooms:
            if classroom.id == item_id:
                return {
                    'name': classroom.name,
                    'faculty_id': classroom.faculty_id,
                    'capacity': classroom.capacity,
                    'has_computer': classroom.has_computer,
                    'is_suitable': classroom.is_suitable
                }
        return None
