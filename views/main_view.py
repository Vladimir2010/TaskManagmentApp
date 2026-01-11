from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QStackedWidget, QLabel, 
                             QDialog, QLineEdit, QComboBox, QDateEdit, QTextEdit, 
                             QMessageBox, QListWidgetItem, QMenu)
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QIcon, QAction
from views.ui_utils import FluentStyle, WindowEffect
from views.calendar_view import CalendarView
from views.analytics_view import AnalyticsView
from controllers.task_controller import TaskController
from controllers.sync_controller import SyncController
from services.notification_service import NotificationService

from services.language_service import lang_service

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.retranslate_ui()
        self.resize(400, 400)
        self.setStyleSheet(f"background-color: {FluentStyle.SURFACE_DARK}; color: white;")
        
        layout = QVBoxLayout(self)
        
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        
        self.desc_input = QTextEdit()
        layout.addWidget(self.desc_input)
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)
        
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High", "Critical"])
        layout.addWidget(self.priority_input)
        
        self.category_input = QComboBox()
        self.category_input.addItems(["Work", "Personal", "Study", "Other"])
        layout.addWidget(self.category_input)
        
        self.save_btn = QPushButton()
        self.save_btn.setStyleSheet("background-color: #0078D4; padding: 10px; font-weight: bold;")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)
        
        self.update_texts()

    def retranslate_ui(self):
        self.setWindowTitle(lang_service.get("new_task"))
    
    def update_texts(self):
        self.setWindowTitle(lang_service.get("new_task"))
        self.title_input.setPlaceholderText(lang_service.get("task_created")) # Using existing key or generic title
        self.desc_input.setPlaceholderText("Description")
        self.save_btn.setText("Save Task")


class MainView(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.task_controller = TaskController()
        self.sync_controller = SyncController(user.id)
        
        self.setWindowTitle(f"{lang_service.get('app_title')} - {user.username}")
        self.resize(1200, 800)
        
        # Apply Windows 11 Effects
        WindowEffect.apply_mica(int(self.winId()))
        
        self.init_ui()
        self.sync_controller.start_background_sync()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(f"background-color: {FluentStyle.SURFACE_DARK};")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        # User Info
        self.user_lbl = QLabel()
        self.user_lbl.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 20px;")
        sidebar_layout.addWidget(self.user_lbl)
        
        # Nav Buttons
        self.nav_dashboard = self.create_nav_btn("")
        self.nav_calendar = self.create_nav_btn("")
        self.nav_analytics = self.create_nav_btn("")
        
        sidebar_layout.addWidget(self.nav_dashboard)
        sidebar_layout.addWidget(self.nav_calendar)
        sidebar_layout.addWidget(self.nav_analytics)
        
        sidebar_layout.addStretch()
        
        # Language Switcher
        lang_layout = QHBoxLayout()
        lang_lbl = QLabel("Language:")
        lang_lbl.setStyleSheet("color: white;")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "bg"])
        self.lang_combo.setCurrentText(lang_service.get_current_code())
        self.lang_combo.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(lang_lbl)
        lang_layout.addWidget(self.lang_combo)
        sidebar_layout.addLayout(lang_layout)

        # Sync & Logout
        self.sync_btn = QPushButton("")
        self.sync_btn.clicked.connect(self.trigger_sync)
        sidebar_layout.addWidget(self.sync_btn)
        
        self.logout_btn = QPushButton("")
        self.logout_btn.setStyleSheet("background-color: #C50F1F; color: white;")
        self.logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(self.logout_btn)
        
        main_layout.addWidget(sidebar)
        
        # Content Area
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Pages UI
        self.dashboard_page = self.create_dashboard_page()
        self.calendar_page = CalendarView(self.task_controller, self.user.id)
        self.analytics_page = AnalyticsView(self.task_controller, self.user.id)
        
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.calendar_page)
        self.stack.addWidget(self.analytics_page)
        
        # Connect Nav
        self.nav_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.nav_calendar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.nav_analytics.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        
        self.retranslate_ui()

    def create_nav_btn(self, text):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton { text-align: left; padding: 10px; border: none; }
            QPushButton:hover { background-color: #3E3E3E; }
        """)
        return btn

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header_layout = QHBoxLayout()
        self.dashboard_title = QLabel()
        self.dashboard_title.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_layout.addWidget(self.dashboard_title)
        
        self.add_btn = QPushButton()
        self.add_btn.setFixedSize(120, 40)
        self.add_btn.setStyleSheet("background-color: #0078D4; border-radius: 5px; font-weight: bold;")
        self.add_btn.clicked.connect(self.open_add_task_dialog)
        header_layout.addWidget(self.add_btn)
        
        # Export Buttons
        export_csv_btn = QPushButton("CSV")
        export_csv_btn.setFixedSize(60, 40)
        export_csv_btn.clicked.connect(self.export_csv)
        header_layout.addWidget(export_csv_btn)

        export_pdf_btn = QPushButton("PDF")
        export_pdf_btn.setFixedSize(60, 40)
        export_pdf_btn.clicked.connect(self.export_pdf)
        header_layout.addWidget(export_pdf_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.load_tasks)
        filter_layout.addWidget(self.search_input)
        layout.addLayout(filter_layout)
        
        # Task List
        self.task_list_widget = QListWidget()
        self.task_list_widget.setStyleSheet(f"background-color: {FluentStyle.SURFACE_DARK}; border: none; border-radius: 8px;")
        self.task_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.task_list_widget)
        
        self.load_tasks()
        return page

    def change_language(self, lang_code):
        if lang_service.set_language(lang_code):
            self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(f"{lang_service.get('app_title')} - {self.user.username}")
        self.user_lbl.setText(lang_service.get('welcome', name=self.user.username))
        self.nav_dashboard.setText(lang_service.get('dashboard'))
        self.nav_calendar.setText(lang_service.get('calendar'))
        self.nav_analytics.setText(lang_service.get('analytics'))
        self.sync_btn.setText(lang_service.get('sync_now'))
        self.logout_btn.setText(lang_service.get('logout'))
        
        self.dashboard_title.setText(lang_service.get('my_tasks'))
        self.add_btn.setText(lang_service.get('new_task'))
        self.search_input.setPlaceholderText(lang_service.get('search_placeholder'))
        
        # Refresh widgets if needed


    def load_tasks(self):
        self.task_list_widget.clear()
        tasks = self.task_controller.get_user_tasks(self.user.id)
        search_term = self.search_input.text().lower()
        
        for task in tasks:
            if search_term in task.title.lower():
                item = QListWidgetItem(f"[{task.priority}] {task.title} - Due: {task.due_date}")
                item.setData(Qt.ItemDataRole.UserRole, task.id)
                self.task_list_widget.addItem(item)

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['title']:
                self.task_controller.create_task(
                    self.user.id,
                    data['title'],
                    data['description'],
                    data['due_date'],
                    data['priority'],
                    data['category']
                )
                self.load_tasks()
                self.analytics_page.refresh_stats()
                NotificationService.send_notification("Task Created", f"{data['title']} added successfully!")

    def show_context_menu(self, pos):
        item = self.task_list_widget.itemAt(pos)
        if not item:
            return
            
        menu = QMenu()
        delete_action = QAction("Delete Task", self)
        delete_action.triggered.connect(lambda: self.delete_task(item))
        menu.addAction(delete_action)
        
        complete_action = QAction("Mark Completed", self)
        complete_action.triggered.connect(lambda: self.complete_task(item))
        menu.addAction(complete_action)
        
        menu.exec(self.task_list_widget.mapToGlobal(pos))

    def delete_task(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this task?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.task_controller.delete_task(task_id)
            self.load_tasks()
            self.analytics_page.refresh_stats()

    def complete_task(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        self.task_controller.update_task(task_id, status="Completed")
        self.load_tasks()
        self.analytics_page.refresh_stats()

    def trigger_sync(self):
        self.sync_controller.perform_sync()
        QMessageBox.information(self, "Sync", "Synchronization completed!")
        
    def export_csv(self):
        from services.export_service import ExportService
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if path:
            tasks = self.task_controller.get_user_tasks(self.user.id)
            success, msg = ExportService.export_to_csv(tasks, path)
            QMessageBox.information(self, "Export", msg)

    def export_pdf(self):
        from services.export_service import ExportService
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF Files (*.pdf)")
        if path:
            tasks = self.task_controller.get_user_tasks(self.user.id)
            success, msg = ExportService.export_to_pdf(tasks, path)
            QMessageBox.information(self, "Export", msg)
            
    def closeEvent(self, event):
        self.sync_controller.stop_sync()
        event.accept()
