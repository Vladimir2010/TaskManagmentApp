from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QLabel, QListWidget
from PyQt6.QtCore import QDate, Qt
from views.ui_utils import FluentStyle

class CalendarView(QWidget):
    def __init__(self, task_controller, user_id):
        super().__init__()
        self.task_controller = task_controller
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Task Calendar")
        title.setFont(FluentStyle.title_font()) 
        # Fallback if I forgot to add font helper, but I'll stick to styles defined
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet(f"""
            QCalendarWidget QWidget {{ 
                background-color: {FluentStyle.SURFACE_DARK}; 
                color: white; 
            }}
            QCalendarWidget QMenu {{
                background-color: {FluentStyle.SURFACE_DARK};
                color: white;
            }}
            QCalendarWidget QSpinBox {{
                color: white;
                background-color: {FluentStyle.SURFACE_DARK};
            }}
        """)
        self.calendar.clicked.connect(self.show_tasks_for_date)
        layout.addWidget(self.calendar)
        
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(f"background-color: {FluentStyle.SURFACE_DARK}; border-radius: 5px;")
        layout.addWidget(self.task_list)

    def show_tasks_for_date(self, date):
        self.task_list.clear()
        selected_date_str = date.toString("yyyy-MM-dd")
        tasks = self.task_controller.get_user_tasks(self.user_id)
        
        for task in tasks:
            if task.due_date == selected_date_str:
                self.task_list.addItem(f"{task.priority} - {task.title}")
