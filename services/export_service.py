import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class ExportService:
    @staticmethod
    def export_to_csv(tasks, filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Title", "Description", "Due Date", "Priority", "Status"])
                for task in tasks:
                    writer.writerow([task.id, task.title, task.description, task.due_date, task.priority, task.status])
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
            c.drawString(50, y, "Task Report")
            y -= 30
            c.setFont(font_name, 12)
            
            for task in tasks:
                # Ensure text is properly encoded/decoded if needed, but python strings are unicode
                line = f"[{task.priority}] {task.title} - Due: {task.due_date} ({task.status})"
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
