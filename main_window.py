import os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QFont
from template import Template
from circle_widget import CircleWidget
from transactions import TransactionsWindow

TRANSACTION_FILE = 'transactions.json'

class MainWindow(Template):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Main Window")
        self.initMenu()

        self.cash_amount = 0.0
        self.card_amount = 0.0

        self.load_amounts()
        
        self.initContent()

    def initContent(self):
        content_layout = QVBoxLayout()

        middle_layout = QHBoxLayout()

        balance_layout = QVBoxLayout()

        balance_label = QLabel("Total Balance")
        balance_label.setFont(QFont("Arial", 24)) 

        self.circle_balance = CircleWidget("#FF6347", self.cash_amount + self.card_amount)
        balance_layout.addWidget(balance_label, alignment=Qt.AlignCenter)
        balance_layout.addWidget(self.circle_balance, alignment=Qt.AlignCenter)
        balance_layout.addSpacing(20)

        middle_layout.addLayout(balance_layout)

        cash_layout = QVBoxLayout()
        self.circle_cash = CircleWidget("#FF6347", self.cash_amount)
        cash_label = QLabel("Cash")
        cash_label.setFont(QFont("Arial", 24)) 
        cash_layout.addWidget(cash_label, alignment=Qt.AlignCenter)
        cash_layout.addWidget(self.circle_cash, alignment=Qt.AlignCenter)
        cash_layout.addSpacing(20) 

        card_layout = QVBoxLayout()
        self.circle_card = CircleWidget("#FF6347", self.card_amount)
        card_label = QLabel("Card")
        card_label.setFont(QFont("Arial", 24)) 
        card_layout.addWidget(card_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.circle_card, alignment=Qt.AlignCenter)
        
        cash_card_layout = QVBoxLayout()
        cash_card_layout.addLayout(cash_layout)
        cash_card_layout.addLayout(card_layout)

        middle_layout.addLayout(cash_card_layout)

        content_layout.addLayout(middle_layout)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10) 

        def add_form_row(label_text, placeholder_text="", widget=None):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10) 
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 16))
            if widget is None:
                input_field = QLineEdit()
                input_field.setPlaceholderText(placeholder_text)
                input_field.setFixedHeight(50) 
                input_field.setFixedWidth(400) 
                input_field.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;") 
                row_layout.addWidget(label)
                row_layout.addWidget(input_field)
                return input_field
            else:
                row_layout.addWidget(label)
                row_layout.addWidget(widget)
            row_layout.addStretch() 
            form_layout.addLayout(row_layout)

        self.cash_input = add_form_row("Add Cash Amount:", "Enter cash amount")
        self.card_input = add_form_row("Add Card Amount:", "Enter card amount")

        add_to_wallet_button = QPushButton("New Transaction")
        add_to_wallet_button.setFont(QFont("Arial", 16))
        add_to_wallet_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        add_to_wallet_button.clicked.connect(self.open_transactions_window)
        form_layout.addWidget(add_to_wallet_button, alignment=Qt.AlignCenter)

        content_layout.addLayout(form_layout)

        self.addContent(content_layout)

    def open_transactions_window(self):
        self.transactions_window = TransactionsWindow()
        self.transactions_window.transaction_added.connect(self.handle_transaction)
        self.transactions_window.show()

    def handle_transaction(self, transaction_type, amount, date, category, description):
        self.update_amounts(transaction_type, amount)
        self.save_transaction(transaction_type, amount, date, category, description)

    def add_to_wallet(self):
        try:
            cash_amount = float(self.cash_input.text())
            card_amount = float(self.card_input.text())
            self.cash_amount += cash_amount
            self.card_amount += card_amount
            self.update_balances()
            self.save_amounts() 
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def update_amounts(self, transaction_type, amount):
        if transaction_type == "Cash":
            self.cash_amount += amount
        elif transaction_type == "Card":
            self.card_amount += amount
        self.update_balances()
        self.save_amounts()

    def update_balances(self):
        self.circle_balance.setAmount(self.cash_amount + self.card_amount)
        self.circle_cash.setAmount(self.cash_amount)
        self.circle_card.setAmount(self.card_amount)

    def save_amounts(self):
        data = {
            'cash_amount': self.cash_amount,
            'card_amount': self.card_amount
        }
        with open('amounts.json', 'w') as file:
            json.dump(data, file)

    def load_amounts(self):
        if os.path.exists('amounts.json'):
            with open('amounts.json', 'r') as file:
                data = json.load(file)
                self.cash_amount = data.get('cash_amount', 0.0)
                self.card_amount = data.get('card_amount', 0.0)

    def save_transaction(self, transaction_type, amount, date, category, description):
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'date': date,
            'category': category,
            'description': description
        }
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, 'r') as file:
                transactions = json.load(file)
        else:
            transactions = []

        transactions.append(transaction)

        with open(TRANSACTION_FILE, 'w') as file:
            json.dump(transactions, file)

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
