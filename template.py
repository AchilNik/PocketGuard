from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QSizePolicy, QMenu, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QFont

class Template(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 1200)
        self.setWindowTitle("PocketGuard")
        self.setWindowIcon(QIcon("images/Screenshot 2024-05-14 213211.png"))
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.setSpacing(0)

        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("images/menu_icon.png"))
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setStyleSheet("background: transparent; border: none;")
        self.menu_button.clicked.connect(self.showMenu)

        app_name = QLabel("PocketGuard")
        app_name.setFont(QFont("Arial", 50, QFont.Bold))
        app_name.setAlignment(Qt.AlignCenter)
        
        self.top_bar_layout.addWidget(self.menu_button, alignment=Qt.AlignLeft)
        self.top_bar_layout.addStretch(1)
        self.top_bar_layout.addWidget(app_name, alignment=Qt.AlignCenter)
        self.top_bar_layout.addStretch(1)

        top_bar_widget = QWidget()
        top_bar_widget.setLayout(self.top_bar_layout)
        top_bar_widget.setStyleSheet("background-color: #800080;")

        top_bar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar_widget.setFixedHeight(80)

        self.main_layout.addWidget(top_bar_widget)
        self.setStyleSheet("""
            QMainWindow { background-color: #FFC0CB; }
            QWidget#top_bar_widget { background-color: #800080; }
            QLabel { font-size: 24px; color: black; }
            QLabel#app_name { font-size: 40px; font-weight: bold; color: black; }
            QPushButton { font-size: 35px; border-radius: 10px; background-color: gray; color: white; }  # Changed background color to gray
            QLineEdit { border-radius: 10px; background-color: #00FFFF; color: black; }
        """)

    def addContent(self, layout):
        self.main_layout.insertLayout(1, layout)


    def initMenu(self):
        self.menu = QMenu()
        self.menu.setStyleSheet("QMenu { background-color: #800080; }")
        self.menu.addAction('Main Screen', lambda: self.change_screen('main'))
        self.menu.addAction('Limits', lambda: self.change_screen('limits'))
        self.menu.addAction('Group Expenses', lambda: self.change_screen('group_expenses'))
        self.menu.addAction('Fixed Expenses', lambda: self.change_screen('fixed_expenses'))
        self.menu.addAction('Customizable Categories', lambda: self.change_screen('customizable_categories'))
        self.menu.addAction('Data Export', lambda: self.change_screen('data_export'))
        self.menu.addAction('Statistics', lambda: self.change_screen('statistics'))
        

    def change_screen(self, screen_type):
        if screen_type == 'main':
            from main_window import MainWindow
            self.setCentralWidget(MainWindow())
        elif screen_type == 'limits':
            from limits import LimitsWindow
            self.setCentralWidget(LimitsWindow())
        elif screen_type == 'group_expenses':
            from we_expenses import WeExpenses
            self.setCentralWidget(WeExpenses())
        elif screen_type == 'fixed_expenses':
            from fixed_expenses import FixedExpensesWindow
            self.setCentralWidget(FixedExpensesWindow())
        elif screen_type == 'customizable_categories':
            from customizable_categories import CustomizableCategoriesWindow
            self.setCentralWidget(CustomizableCategoriesWindow())
        elif screen_type == 'data_export':
            from data_export import DataExportWindow
            self.setCentralWidget(DataExportWindow())
        elif screen_type == 'statistics':
            from statistics_screen import StatisticsWindow
            self.setCentralWidget(StatisticsWindow())
        

    def showMenu(self):
        self.menu.exec_(self.mapToGlobal(QPoint(self.menu_button.x(), self.menu_button.y() + self.menu_button.height())))
