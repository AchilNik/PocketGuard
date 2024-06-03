import os
import json
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QDateEdit, QGridLayout)
from PyQt5.QtGui import QFont
from template import Template

TRANSACTION_FILE = 'transactions.json'

class DataExportWindow(Template):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Data Export")
        self.initContent()
        self.initMenu()

    def initContent(self):
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)

        create_new_file_label = QLabel("Create New File")
        create_new_file_label.setFont(QFont("Arial", 20, QFont.Bold))
        content_layout.addWidget(create_new_file_label, alignment=Qt.AlignCenter)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)
        form_layout.setContentsMargins(40, 0, 40, 0)

        def add_form_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 16))
            form_layout.addWidget(label, row, 0, Qt.AlignLeft)
            form_layout.addWidget(widget, row, 1, Qt.AlignRight)

        start_date_edit = QDateEdit()
        start_date_edit.setDate(QDate.currentDate())
        start_date_edit.setFixedHeight(30)
        start_date_edit.setFixedWidth(400)
        start_date_edit.setCalendarPopup(True)
        start_date_edit.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(0, "Start Date:", start_date_edit)

        end_date_edit = QDateEdit()
        end_date_edit.setDate(QDate.currentDate())
        end_date_edit.setFixedHeight(30)
        end_date_edit.setFixedWidth(400)
        end_date_edit.setCalendarPopup(True)
        end_date_edit.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(1, "End Date:", end_date_edit)

        file_type_combo = QComboBox()
        file_type_combo.addItem("txt")
        file_type_combo.addItem("csv")
        file_type_combo.setFixedHeight(30)
        file_type_combo.setFixedWidth(400)
        file_type_combo.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(2, "Choose File type:", file_type_combo)

        content_layout.addLayout(form_layout)

        export_data_button = QPushButton("Export Data")
        export_data_button.setFont(QFont("Arial", 16))
        export_data_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        export_data_button.clicked.connect(lambda: self.export_data(start_date_edit.date(), end_date_edit.date(), file_type_combo.currentText()))
        content_layout.addWidget(export_data_button, alignment=Qt.AlignCenter)

        self.addContent(content_layout)

    def export_data(self, start_date, end_date, file_type):
        if not os.path.exists(TRANSACTION_FILE):
            print("No transactions to export.")
            return

        with open(TRANSACTION_FILE, 'r') as file:
            transactions = json.load(file)

        start_date = start_date.toString("yyyy-MM-dd")
        end_date = end_date.toString("yyyy-MM-dd")

        filtered_transactions = [
            t for t in transactions
            if start_date <= t['date'] <= end_date
        ]

        if file_type == 'txt':
            self.export_to_txt(filtered_transactions)
        elif file_type == 'csv':
            self.export_to_csv(filtered_transactions)
        elif file_type == 'pdf':
            self.export_to_pdf(filtered_transactions)

    def export_to_txt(self, transactions):
        with open('data_export.txt', 'w') as file:
            for t in transactions:
                file.write(f"Date: {t['date']}, Type: {t['type']}, Amount: {t['amount']}, Category: {t['category']}, Description: {t['description']}\n")
        print("Exported to data_export.txt")

    def export_to_csv(self, transactions):
        import csv
        with open('data_export.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Type', 'Amount', 'Category', 'Description'])
            for t in transactions:
                writer.writerow([t['date'], t['type'], t['amount'], t['category'], t['description']])
        print("Exported to data_export.csv")
