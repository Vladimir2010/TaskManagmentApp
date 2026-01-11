import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from services.language_service import lang_service

class ExportService:
    @staticmethod
    def export_to_csv(tasks, filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Translated Headers
                headers = [
                    lang_service.get("col_id"),
                    lang_service.get("col_title"),
                    lang_service.get("col_desc"),
                    lang_service.get("due_date"),
                    lang_service.get("priority"),
                    lang_service.get("col_status")
                ]
                writer.writerow(headers)
                
                for task in tasks:
                    # Translate Priority and Status
                    p_text = lang_service.get(f"priority_{task.priority}", default=task.priority)
                    # Status logic: Assuming task.status is "Pending" or "Completed"
                    # status_pending / status_completed keys exist? Let's check keys used in AnalyticsView
                    # Analytics used "status_pending" (lowercase p) but task.status might be "Pending"
                    s_key = f"status_{task.status.lower()}"
                    s_text = lang_service.get(s_key, default=task.status)
                    
                    writer.writerow([task.id, task.title, task.description, task.due_date, p_text, s_text])
            return True, "Exported successfully"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def export_to_pdf(tasks, filepath):
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            # Register a font that supports Cyrillic (Arial is standard on Windows)
            font_path = "C:\\Windows\\Fonts\\arial.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Arial', font_path))
                font_name = 'Arial'
                font_bold = 'Arial' # Using same for bold if bold file not found, or could just use regular
            else:
                font_name = 'Helvetica' # Fallback
                font_bold = 'Helvetica-Bold'

            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter
            y = height - 50
            
            c.setFont(font_bold, 16)
            c.drawString(50, y, lang_service.get("task_report"))
            y -= 30
            c.setFont(font_name, 12)
            
            for task in tasks:
                # Translate content
                p_text = lang_service.get(f"priority_{task.priority}", default=task.priority)
                s_key = f"status_{task.status.lower()}"
                s_text = lang_service.get(s_key, default=task.status)
                due_prefix = lang_service.get("due_prefix")
                
                # Format: [Priority] Title - Due: Date (Status)
                line = f"[{p_text}] {task.title} - {due_prefix}{task.due_date} ({s_text})"
                c.drawString(50, y, line)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont(font_name, 12)
            
            c.save()
            return True, "PDF Generated"
        except Exception as e:
            return False, str(e)
