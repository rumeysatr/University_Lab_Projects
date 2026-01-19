import tkinter as tk
from tkinter import messagebox, filedialog


class ImportView(tk.Frame):
    title = '📥 Veri Yükleme'

    def __init__(self, parent, dashboard):
        super().__init__(parent, bg='#ecf0f1')
        self.dashboard = dashboard
        self.controller = dashboard.controller
        self.class_lists_folder = None
        self.proximity_file = None
        self.capacity_file = None

        self._create_widgets()

    def _create_widgets(self):
        header_frame = tk.Frame(self, bg='#ecf0f1')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text=self.title,
            font=('Segoe UI', 20, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(side='left')

        content_frame = tk.Frame(self, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        class_list_frame = tk.LabelFrame(
            content_frame,
            text='Sınıf Listeleri',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            padx=15,
            pady=10
        )
        class_list_frame.pack(fill='x', pady=(0, 15))

        class_list_label = tk.Label(
            class_list_frame,
            text='Sınıf Listeleri Klasörünü Seç',
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        class_list_label.pack(anchor='w')

        class_list_btn = tk.Button(
            class_list_frame,
            text='Klasör Seç',
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self._select_class_list_folder
        )
        class_list_btn.pack(anchor='w', pady=(8, 6))

        self.class_list_path_label = tk.Label(
            class_list_frame,
            text='Seçilmedi',
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.class_list_path_label.pack(anchor='w')

        proximity_frame = tk.LabelFrame(
            content_frame,
            text='Derslik Yakınlığı',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            padx=15,
            pady=10
        )
        proximity_frame.pack(fill='x', pady=(0, 15))

        proximity_label = tk.Label(
            proximity_frame,
            text='Derslik Yakınlık Dosyasını Seç',
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        proximity_label.pack(anchor='w')

        proximity_btn = tk.Button(
            proximity_frame,
            text='Dosya Seç',
            font=('Segoe UI', 10),
            bg='#16a085',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self._select_proximity_file
        )
        proximity_btn.pack(anchor='w', pady=(8, 6))

        self.proximity_path_label = tk.Label(
            proximity_frame,
            text='Seçilmedi',
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.proximity_path_label.pack(anchor='w')

        # Kapasite dosyası frame'i
        capacity_frame = tk.LabelFrame(
            content_frame,
            text='Sınav Kapasiteleri',
            font=('Segoe UI', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            padx=15,
            pady=10
        )
        capacity_frame.pack(fill='x', pady=(0, 15))

        capacity_label = tk.Label(
            capacity_frame,
            text='Derslik Kapasite Dosyasını Seç (kostu_sinav_kapasiteleri.xlsx)',
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        capacity_label.pack(anchor='w')

        capacity_btn = tk.Button(
            capacity_frame,
            text='Dosya Seç',
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self._select_capacity_file
        )
        capacity_btn.pack(anchor='w', pady=(8, 6))

        self.capacity_path_label = tk.Label(
            capacity_frame,
            text='Seçilmedi',
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.capacity_path_label.pack(anchor='w')

        action_frame = tk.Frame(content_frame, bg='#ecf0f1')
        action_frame.pack(fill='x', pady=(10, 0))

        upload_btn = tk.Button(
            action_frame,
            text='Yükle ve Kaydet',
            font=('Segoe UI', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self._on_upload
        )
        upload_btn.pack(anchor='e')

    def _select_class_list_folder(self):
        folder_path = filedialog.askdirectory(title='Sınıf Listeleri Klasörü Seç')
        if folder_path:
            self.class_lists_folder = folder_path
            self.class_list_path_label.config(text=folder_path)

    def _select_proximity_file(self):
        file_path = filedialog.askopenfilename(
            title='Derslik Yakınlık Dosyası Seç',
            filetypes=[
                ('Excel Dosyaları', '*.xlsx *.xls'),
                ('CSV Dosyaları', '*.csv'),
                ('Tüm Dosyalar', '*.*')
            ]
        )
        if file_path:
            self.proximity_file = file_path
            self.proximity_path_label.config(text=file_path)

    def _select_capacity_file(self):
        """Kapasite dosyasını seçer"""
        file_path = filedialog.askopenfilename(
            title='Sınav Kapasite Dosyasını Seç',
            filetypes=[
                ('Excel Dosyaları', '*.xlsx *.xls'),
                ('Tüm Dosyalar', '*.*')
            ]
        )
        if file_path:
            self.capacity_file = file_path
            self.capacity_path_label.config(text=file_path)

    def _on_upload(self):
        if not self.class_lists_folder:
            messagebox.showwarning('Uyarı', 'Lütfen sınıf listeleri klasörünü seçin.')
            return
        
        results = []
        
        # 1. Sınıf listelerini içe aktar
        try:
            class_list_result = self.controller.import_class_lists_folder(self.class_lists_folder)
            results.append(('Sınıf Listeleri', class_list_result))
        except AttributeError:
            messagebox.showerror('Hata', 'Sınıf listeleri yükleme yöntemi bulunamadı.')
            return
        except Exception as exc:
            messagebox.showerror('Hata', f'Sınıf listeleri yüklenemedi: {str(exc)}')
            return

        # 2. Derslik yakınlığını içe aktar (opsiyonel)
        if self.proximity_file:
            try:
                proximity_result = self.controller.import_classroom_proximity(self.proximity_file)
                results.append(('Derslik Yakınlığı', proximity_result))
            except Exception as exc:
                results.append(('Derslik Yakınlığı', {'success': False, 'message': f'Hata: {str(exc)}'}))
        
        # 3. Kapasite dosyasını içe aktar (opsiyonel)
        if self.capacity_file:
            try:
                capacity_result = self.controller.import_exam_capacity(self.capacity_file)
                results.append(('Sınav Kapasiteleri', capacity_result))
            except Exception as exc:
                results.append(('Sınav Kapasiteleri', {'success': False, 'message': f'Hata: {str(exc)}'}))
        
        # Sonuçları göster
        success_count = sum(1 for _, r in results if r.get('success', False))
        total_count = len(results)
        
        result_messages = []
        for name, result in results:
            status = "✓" if result.get('success', False) else "✗"
            result_messages.append(f"{status} {name}: {result.get('message', 'İşlem tamamlandı')}")
        
        summary = f"\n\n{success_count}/{total_count} işlem başarıyla tamamlandı.\n\n" + "\n".join(result_messages)
        
        if success_count == total_count:
            messagebox.showinfo('Başarılı', f'Tüm veriler başarıyla yüklendi.{summary}')
        else:
            messagebox.showwarning('Kısmi Başarı', f'Bazı işlemler başarısız oldu.{summary}')
