from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QStackedWidget, QLabel, 
                             QDialog, QLineEdit, QComboBox, QDateEdit, QTextEdit, 
                             QMessageBox, QListWidgetItem, QMenu, QHeaderView)
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QIcon, QAction
import os
from views.ui_utils import FluentStyle, WindowEffect
from views.calendar_view import CalendarView
from views.analytics_view import AnalyticsView
from views.about_view import AboutDialog
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
        # Store internal values separately or rely on index, for simplicity we use keys that map to translation keys
        # But here we need to display translated text.
        # We will populate these in update_texts to handle language switch if needed, 
        # but for a modal dialog, it re-creates usually. 
        # Let's populate initially with current lang.
        self.priority_input.addItems([lang_service.get(f"priority_{p}") for p in ["Low", "Medium", "High", "Critical"]])
        layout.addWidget(self.priority_input)
        
        self.category_input = QComboBox()
        self.category_input.addItems([lang_service.get(f"cat_{c}") for c in ["Work", "Personal", "Study", "Other"]])
        layout.addWidget(self.category_input)
        
        self.save_btn = QPushButton()
        self.save_btn.setStyleSheet("background-color: #0078D4; padding: 10px; font-weight: bold;")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)
        
        self.update_texts()

    def get_data(self):
        # We need to map back the translated priority/category to internal English values
        # Or simpler: Just stick to index since the order is fixed.
        priorities = ["Low", "Medium", "High", "Critical"]
        categories = ["Work", "Personal", "Study", "Other"]
        
        return {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "priority": priorities[self.priority_input.currentIndex()],
            "category": categories[self.category_input.currentIndex()]
        }

    def update_texts(self):
        self.setWindowTitle(lang_service.get("new_task"))
        self.title_input.setPlaceholderText(lang_service.get("task_title_placeholder"))
        self.desc_input.setPlaceholderText(lang_service.get("task_desc_placeholder"))
        self.save_btn.setText(lang_service.get("save_task"))


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
        # Menu Bar
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {FluentStyle.BACKGROUND_DARK};
                color: {FluentStyle.TEXT_DARK};
                border-bottom: 1px solid {FluentStyle.BORDER_DARK};
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
            }}
            QMenuBar::item:selected {{
                background-color: {FluentStyle.SURFACE_DARK};
            }}
            QMenu {{
                background-color: {FluentStyle.SURFACE_DARK};
                border: 1px solid {FluentStyle.BORDER_DARK};
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 24px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {FluentStyle.HOVER_DARK};
            }}
        """)
        
        self.help_menu = self.menu_bar.addMenu(lang_service.get("menu_help"))
        self.about_action = QAction(lang_service.get("menu_about"), self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

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
        
        # Task List (Table)
        self.task_list_widget = QTableWidget()
        self.task_list_widget.setColumnCount(3)
        self.task_list_widget.setHorizontalHeaderLabels([lang_service.get("priority"), lang_service.get("my_tasks"), lang_service.get("due_date")])
        self.task_list_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.task_list_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_list_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.task_list_widget.setStyleSheet(f"""
            QTableWidget {{
                background-color: {FluentStyle.SURFACE_DARK};
                gridline-color: #3E3E3E;
                border: none;
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {FluentStyle.SURFACE_DARK};
                color: {FluentStyle.TEXT_DARK};
                border: none;
                font-weight: bold;
                padding: 5px;
            }}
        """)
        
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
        
        # Update Menu
        self.help_menu.setTitle(lang_service.get("menu_help"))
        self.about_action.setText(lang_service.get("menu_about"))

        # Update Table Headers
        self.task_list_widget.setHorizontalHeaderLabels([lang_service.get("priority"), lang_service.get("my_tasks"), lang_service.get("due_date")])

        # Refresh widgets if needed
        self.calendar_page.retranslate_ui()
        self.analytics_page.retranslate_ui()
        self.load_tasks()


    def load_tasks(self):
        self.task_list_widget.setRowCount(0)
        tasks = self.task_controller.get_user_tasks(self.user.id)
        search_term = self.search_input.text().lower()
        
        current_lang = lang_service.get_current_code()
        
        for task in tasks:
            if search_term in task.title.lower():
                row = self.task_list_widget.rowCount()
                self.task_list_widget.insertRow(row)
                
                # Priority
                priority_key = f"priority_{task.priority}"
                priority_text = lang_service.get(priority_key, default=task.priority)
                item_priority = QTableWidgetItem(priority_text)
                self.task_list_widget.setItem(row, 0, item_priority)
                
                # Title
                item_title = QTableWidgetItem(task.title)
                item_title.setData(Qt.ItemDataRole.UserRole, task.id) # Store ID here
                self.task_list_widget.setItem(row, 1, item_title)
                
                # Date Formatting
                date_str = task.due_date
                try:
                    # Input is yyyy-MM-dd
                    parts = date_str.split("-")
                    if len(parts) == 3:
                         # Output dd.MM.yyyy
                        date_str = f"{parts[2]}.{parts[1]}.{parts[0]}"
                except:
                    pass
                    
                item_date = QTableWidgetItem(date_str)
                self.task_list_widget.setItem(row, 2, item_date)

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
                NotificationService.send_notification(
                    lang_service.get("notif_task_created_title"), 
                    lang_service.get("notif_task_created_msg", title=data['title'])
                )

    def show_context_menu(self, pos):
        item = self.task_list_widget.itemAt(pos)
        if not item:
            return
            
        # Ensure we get the ID from column 1 (Title), regardless of clicked column
        row = self.task_list_widget.row(item)
        title_item = self.task_list_widget.item(row, 1)
        if not title_item:
            return
            
        menu = QMenu()
        delete_action = QAction(lang_service.get("delete_task"), self)
        delete_action.triggered.connect(lambda: self.delete_task_item(title_item))
        menu.addAction(delete_action)
        
        complete_action = QAction(lang_service.get("mark_completed"), self)
        complete_action.triggered.connect(lambda: self.complete_task_item(title_item))
        menu.addAction(complete_action)
        
        menu.exec(self.task_list_widget.mapToGlobal(pos))

    def delete_task_item(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(self, lang_service.get("confirm_delete_title"), lang_service.get("confirm_delete_msg"))
        if confirm == QMessageBox.StandardButton.Yes:
            self.task_controller.delete_task(task_id)
            self.load_tasks()
            self.analytics_page.refresh_stats()

    def complete_task_item(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        self.task_controller.update_task(task_id, status="Completed")
        self.load_tasks()
        self.analytics_page.refresh_stats()

    def trigger_sync(self):
        self.sync_controller.perform_sync()
        QMessageBox.information(self, lang_service.get("sync"), lang_service.get("sync_completed"))
        
    def export_csv(self):
        from services.export_service import ExportService
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(self, lang_service.get("export_info"), "", "CSV Files (*.csv)")
        if path:
            tasks = self.task_controller.get_user_tasks(self.user.id)
            success, msg = ExportService.export_to_csv(tasks, path)
            QMessageBox.information(self, lang_service.get("export_info"), msg)
            if success:
                try:
                    os.startfile(path)
                except Exception:
                    pass

    def export_pdf(self):
        from services.export_service import ExportService
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(self, lang_service.get("export_info"), "", "PDF Files (*.pdf)")
        if path:
            tasks = self.task_controller.get_user_tasks(self.user.id)
            success, msg = ExportService.export_to_pdf(tasks, path)
            QMessageBox.information(self, lang_service.get("export_info"), msg)
            if success:
                try:
                    os.startfile(path)
                except Exception:
                    pass
            
    def closeEvent(self, event):
        self.sync_controller.stop_sync()
        event.accept()

    def show_about(self):
        dlg = AboutDialog(self)
        dlg.exec()
