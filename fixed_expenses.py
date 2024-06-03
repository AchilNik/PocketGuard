from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QDateEdit)
from PyQt5.QtGui import QFont
from template import Template
from custom_popup_window import CustomPopupWindow 

class FixedExpensesWindow(Template):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Fixed Expenses")
        self.inputs = {}
        self.initContent()
        self.initMenu()

    def initContent(self):
        content_layout = QVBoxLayout()

        create_new_expense_label = QLabel("Create New Fixed Expense")
        create_new_expense_label.setFont(QFont("Arial", 20, QFont.Bold))
        content_layout.addWidget(create_new_expense_label, alignment=Qt.AlignCenter)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10) 
        form_layout.setVerticalSpacing(10) 
        form_layout.setContentsMargins(40, 0, 40, 0)

        def add_form_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 16))
            form_layout.addWidget(label, row, 0, Qt.AlignLeft)
            form_layout.addWidget(widget, row, 1, Qt.AlignRight)
            self.inputs[label_text] = widget

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter expense name")
        name_input.setFixedHeight(30)
        name_input.setFixedWidth(400)
        name_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;") 
        add_form_row(1, "Expense Name:", name_input)

        amount_input = QLineEdit()
        amount_input.setPlaceholderText("Enter amount")
        amount_input.setFixedHeight(30)
        amount_input.setFixedWidth(400)
        amount_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;") 
        add_form_row(2, "Add Amount:", amount_input)

        category_combo = QComboBox()
        category_combo.addItem("Leisure")
        category_combo.addItem("Cash")
        category_combo.addItem("Health")
        category_combo.addItem("Home")
        category_combo.addItem("Shopping")
        category_combo.addItem("Transport")
        category_combo.setFixedHeight(30)
        category_combo.setFixedWidth(400)
        category_combo.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(3, "Choose Category:", category_combo)

        amount_input = QLineEdit()
        amount_input.setPlaceholderText("Enter frequency")
        amount_input.setFixedHeight(30)
        amount_input.setFixedWidth(400)
        amount_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;") 
        add_form_row(4, "Add Frequency of charge:", amount_input)
        
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate())
        date_input.setFixedHeight(50)
        date_input.setFixedWidth(400)
        date_input.setCalendarPopup(True)
        date_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        add_form_row(5, "Add Date of charge", widget=date_input)

        content_layout.addLayout(form_layout)

        add_expense_button = QPushButton("Add expense")
        add_expense_button.setFont(QFont("Arial", 16))
        add_expense_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        add_expense_button.clicked.connect(self.show_popup)
        content_layout.addWidget(add_expense_button, alignment=Qt.AlignCenter)

        self.addContent(content_layout)


    def show_popup(self):
        summary = "Summary of Fixed Expense:\n"
        for label_text, widget in self.inputs.items():
            if isinstance(widget, QDateEdit):
                summary += f"{label_text}: {widget.date().toString(Qt.ISODate)}\n"
            elif isinstance(widget, QComboBox):
                summary += f"{label_text}: {widget.currentText()}\n"
            else:
                summary += f"{label_text}: {widget.text()}\n"
        
        self.popup_window = CustomPopupWindow(summary)
        self.popup_window.show()

