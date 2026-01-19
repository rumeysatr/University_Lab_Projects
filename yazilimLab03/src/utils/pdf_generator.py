"""
PDF Rapor Oluşturucu - Sınav Programı ve raporları PDF olarak dışa aktarma
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """PDF rapor oluşturmak için yardımcı sınıf."""

    def __init__(self):
        self.title = "Sınav Programı"
        self.author = "Sınav Planlama Sistemi"

    def generate_exam_schedule_pdf(
        self,
        exams: List[Any],
        output_path: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> bool:
        """
        Sınav programını PDF olarak oluşturur.
        
        Args:
            exams: Sınav verisi listesi
            output_path: Çıktı dosya yolu (.pdf)
            start_date: Başlangıç tarihi
            end_date: Bitiş tarihi
            
        Returns:
            bool: Başarı durumu
        """
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            
            # Belge oluştur
            doc = SimpleDocTemplate(
                output_path,
                pagesize=landscape(A4),
                topMargin=0.5*inch,
                bottomMargin=0.5*inch,
                leftMargin=0.5*inch,
                rightMargin=0.5*inch,
                title=self.title,
                author=self.author
            )
            
            # Stil tanımla
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f4e78'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            elements = []
            
            # Başlık
            title_text = "SINAV PROGRAMI"
            if start_date and end_date:
                title_text += f" ({start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')})"
            
            elements.append(Paragraph(title_text, title_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Tablo başlıkları
            headers = [
                'Tarih',
                'Saat',
                'Ders Kodu',
                'Ders Adı',
                'Öğretim Üyesi',
                'Derslik',
                'Öğrenci',
                'Sınav Türü',
                'Durum'
            ]
            
            # Veriyi hazırla
            data = [headers]
            for exam in exams:
                row = [
                    self._get_value(exam, 'exam_date', ''),
                    f"{self._get_value(exam, 'start_time', '')} - {self._get_value(exam, 'end_time', '')}",
                    self._get_value(exam, 'course_code', ''),
                    self._truncate(self._get_value(exam, 'course_name', ''), 25),
                    self._truncate(self._get_value(exam, 'lecturer_name', ''), 20),
                    self._get_value(exam, 'classroom_name', ''),
                    str(self._get_value(exam, 'student_count', '')),
                    self._get_exam_type_label(self._get_value(exam, 'exam_type', '')),
                    self._get_status_label(self._get_value(exam, 'status', ''))
                ]
                data.append(row)
            
            # Tablo oluştur
            table = Table(data, colWidths=[0.9*inch, 1.1*inch, 0.9*inch, 1.8*inch, 1.5*inch, 0.8*inch, 0.6*inch, 0.8*inch, 0.8*inch])
            
            # Tablo stilini uygula
            table.setStyle(TableStyle([
                # Başlık satırı
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('PADDING', (0, 1), (-1, -1), 6),
            ]))
            
            elements.append(table)
            
            # Özet bilgi
            elements.append(Spacer(1, 0.2*inch))
            summary_style = ParagraphStyle(
                'Summary',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_LEFT
            )
            summary_text = f"Toplam Sınav: {len(exams)} | Oluşturma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            elements.append(Paragraph(summary_text, summary_style))
            
            # Belgeyi oluştur
            doc.build(elements)
            logger.info(f"PDF başarıyla oluşturuldu: {output_path}")
            return True
            
        except ImportError:
            logger.error("PDF oluşturma için reportlab kütüphanesi gereklidir")
            return False
        except Exception as e:
            logger.error(f"PDF oluşturulurken hata: {e}")
            return False

    def _get_value(self, item: Any, key: str, default: Any = '') -> Any:
        """Dict veya Object'ten değer al."""
        if isinstance(item, dict):
            return item.get(key, default)
        else:
            return getattr(item, key, default)

    def _truncate(self, text: str, length: int) -> str:
        """Metni belirli uzunluğa kısalt."""
        text = str(text)
        if len(text) > length:
            return text[:length-3] + "..."
        return text

    def _get_exam_type_label(self, exam_type: str) -> str:
        """Sınav türü etiketini döndür."""
        labels = {
            'midterm': 'Vize',
            'final': 'Final',
            'makeup': 'Bütünleme',
            'quiz': 'Quiz'
        }
        return labels.get(exam_type, exam_type or '')

    def _get_status_label(self, status: str) -> str:
        """Durum etiketini döndür."""
        labels = {
            'planned': 'Planlandı',
            'confirmed': 'Onaylandı',
            'cancelled': 'İptal Edildi'
        }
        return labels.get(status, status or '')


class SimplePDFGenerator:
    """reportlab olmadığı durumlarda alternatif PDF oluşturma."""

    @staticmethod
    def generate_exam_schedule_simple(
        exams: List[Any],
        output_path: str
    ) -> bool:
        """
        Basit metin tabanlı PDF oluştur (reportlab olmadan).
        """
        try:
            from fpdf import FPDF
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "SINAV PROGRAMI", ln=True, align='C')
            pdf.ln(5)
            
            # Başlıklar
            pdf.set_font("Arial", "B", 8)
            pdf.multi_cell(0, 5, "Tarih | Saat | Ders Kodu | Ders Adı | Öğretim Üyesi | Derslik | Öğrenci | Sınav Türü | Durum")
            pdf.ln(2)
            
            # Veriler
            pdf.set_font("Arial", "", 7)
            for exam in exams:
                line = f"{exam.get('exam_date', '')} | {exam.get('start_time', '')} - {exam.get('end_time', '')} | " \
                       f"{exam.get('course_code', '')} | {exam.get('course_name', '')[:15]} | " \
                       f"{exam.get('lecturer_name', '')[:15]} | {exam.get('classroom_name', '')} | " \
                       f"{exam.get('student_count', '')} | {exam.get('exam_type', '')} | {exam.get('status', '')}"
                pdf.multi_cell(0, 4, line)
            
            pdf.output(output_path)
            logger.info(f"Basit PDF oluşturuldu: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Basit PDF oluşturulurken hata: {e}")
            return False
