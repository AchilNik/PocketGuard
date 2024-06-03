import os
import json
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QDateEdit, QGridLayout)
from PyQt5.QtGui import QFont
from template import Template

TRANSACTION_FILE = 'transactions.json'

class TransactionsWindow(Template):
    transaction_added = pyqtSignal(str, float, str, str, str, name='transactionAdded')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Add Transaction")
        self.initContent()
        self.initMenu()

    def initContent(self):
        content_layout = QVBoxLayout()

        new_transaction = QLabel("New Transaction")
        new_transaction.setFont(QFont("Arial", 20, QFont.Bold))
        content_layout.addWidget(new_transaction, alignment=Qt.AlignCenter)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10) 
        form_layout.setVerticalSpacing(10) 
        form_layout.setContentsMargins(40, 0, 40, 0)

        def add_form_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 16))
            form_layout.addWidget(label, row, 0, Qt.AlignLeft)
            form_layout.addWidget(widget, row, 1, Qt.AlignRight)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setFixedHeight(30)
        self.amount_input.setFixedWidth(400)
        self.amount_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(0, "Amount:", self.amount_input)

        self.type_combo = QComboBox()
        self.type_combo.addItem("Cash")
        self.type_combo.addItem("Card")
        self.type_combo.setFixedHeight(30)
        self.type_combo.setFixedWidth(400)
        self.type_combo.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(1, "Type:", self.type_combo)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setFixedHeight(30)
        self.date_input.setFixedWidth(400)
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(2, "Date:", self.date_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter category")
        self.category_input.setFixedHeight(30)
        self.category_input.setFixedWidth(400)
        self.category_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(3, "Category:", self.category_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter description (optional)")
        self.description_input.setFixedHeight(30)
        self.description_input.setFixedWidth(400)
        self.description_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(4, "Description:", self.description_input)

        content_layout.addLayout(form_layout)

        add_transaction_button = QPushButton("Add Transaction")
        add_transaction_button.setFont(QFont("Arial", 16))
        add_transaction_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        add_transaction_button.clicked.connect(self.add_transaction)
        content_layout.addWidget(add_transaction_button, alignment=Qt.AlignCenter)

        self.addContent(content_layout)

    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            transaction_type = self.type_combo.currentText()
            date = self.date_input.date().toString("yyyy-MM-dd")
            category = self.category_input.text()
            description = self.description_input.text() if self.description_input.text() else "No description provided"
            self.transaction_added.emit(transaction_type, amount, date, category, description)
            self.close()
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

