import os
import json
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDateEdit, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont
from template import Template

TRANSACTION_FILE = 'transactions.json'

class StatisticsWindow(Template):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Statistics")
        self.transactions = self.load_transactions()
        self.filtered_transactions = self.transactions
        self.initContent()
        self.initMenu()

    def load_transactions(self):
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, 'r') as file:
                transactions = json.load(file)
        else:
            transactions = []
        return transactions

    def initContent(self):
        content_layout = QVBoxLayout()

        top_third_widget = QWidget()
        top_third_layout = QVBoxLayout(top_third_widget)
        top_third_layout.setContentsMargins(0, 30, 0, 0)

        date_row = QHBoxLayout()

        start_date_label = QLabel("Start Date:")
        start_date_label.setFont(QFont("Arial", 14))
        date_row.addWidget(start_date_label)

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        date_row.addWidget(self.start_date_edit)

        end_date_label = QLabel("End Date:")
        end_date_label.setFont(QFont("Arial", 14))
        date_row.addWidget(end_date_label)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        date_row.addWidget(self.end_date_edit)

        top_third_layout.addLayout(date_row)

        filter_button = QPushButton("Filter")
        filter_button.setFont(QFont("Arial", 14))
        filter_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        filter_button.clicked.connect(self.filter_transactions)
        top_third_layout.addWidget(filter_button, alignment=Qt.AlignCenter)

        content_layout.addWidget(top_third_widget)
        content_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        bottom_two_thirds_widget = QWidget()
        bottom_two_thirds_layout = QVBoxLayout(bottom_two_thirds_widget)

        bottom_two_thirds_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        stats_label = QLabel("Statistics")
        stats_label.setFont(QFont("Arial", 20, QFont.Bold))
        stats_label.setAlignment(Qt.AlignCenter)
        bottom_two_thirds_layout.addWidget(stats_label)

        bottom_two_thirds_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.stats_layout = QGridLayout()
        self.stats_layout.setHorizontalSpacing(20)
        self.stats_layout.setVerticalSpacing(10)
        self.stats_layout.setContentsMargins(40, 20, 40, 20)
        bottom_two_thirds_layout.addLayout(self.stats_layout)

        bottom_two_thirds_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        content_layout.addWidget(bottom_two_thirds_widget)

        self.addContent(content_layout)
        self.update_statistics()

    def filter_transactions(self):
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")

        self.filtered_transactions = [
            t for t in self.transactions
            if start_date <= t['date'] <= end_date
        ]
        self.update_statistics()

    def update_statistics(self):
        for i in reversed(range(self.stats_layout.count())):
            item = self.stats_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        total_amount_spent = sum(t['amount'] for t in self.filtered_transactions)
        categories = {}
        for t in self.filtered_transactions:
            if t['category'] in categories:
                categories[t['category']] += t['amount']
            else:
                categories[t['category']] = t['amount']

        total_label = QLabel(f"Total Amount Spent: ${total_amount_spent:.2f}")
        total_label.setFont(QFont("Arial", 16, QFont.Bold))
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setContentsMargins(0, 0, 0, 20)
        self.stats_layout.addWidget(total_label, 0, 0, 1, 2)

        row = 1
        for category, amount in categories.items():
            category_label = QLabel(f"{category}:")
            category_label.setFont(QFont("Arial", 14))
            category_label.setAlignment(Qt.AlignRight)
            amount_label = QLabel(f"${amount:.2f}")
            amount_label.setFont(QFont("Arial", 14))
            amount_label.setAlignment(Qt.AlignLeft)

            self.stats_layout.addWidget(category_label, row, 0, Qt.AlignRight)
            self.stats_layout.addWidget(amount_label, row, 1, Qt.AlignLeft)
            row += 1
