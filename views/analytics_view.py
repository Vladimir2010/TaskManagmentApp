from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
from views.ui_utils import FluentStyle
from services.language_service import lang_service

class AnalyticsView(QWidget):
    def __init__(self, task_controller, user_id):
        super().__init__()
        self.task_controller = task_controller
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title)
        
        # Pie Chart
        self.series = QPieSeries()
        self.refresh_stats()
        
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Task Status Distribution")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Theme Customization
        self.chart.setBackgroundBrush(QColor(FluentStyle.BACKGROUND_DARK))
        self.chart.setTitleBrush(QColor(FluentStyle.TEXT_DARK))
        self.chart.legend().setLabelColor(QColor(FluentStyle.TEXT_DARK))
        
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        layout.addWidget(chart_view)

    def refresh_stats(self):
        self.series.clear()
        stats = self.task_controller.get_statistics(self.user_id)
        
        completed = stats.get('completed', 0)
        pending = stats.get('pending', 0)
        
        if completed + pending == 0:
            slice_ = self.series.append(lang_service.get("no_tasks"), 1)
            slice_.setColor(QColor("#555555"))
            return

        slice_c = self.series.append(lang_service.get("status_completed"), completed)
        slice_c.setColor(QColor("#107C10")) # Green
        slice_c.setLabelVisible(True)
        
        slice_p = self.series.append(lang_service.get("status_pending"), pending)
        slice_p.setColor(QColor("#C50F1F")) # Red
        slice_p.setLabelVisible(True)

    def retranslate_ui(self):
        self.title.setText(lang_service.get("analytics_title"))
        self.refresh_stats()

