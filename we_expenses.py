from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox)
from PyQt5.QtGui import QFont
from template import Template
from custom_popup_window import CustomPopupWindow

class WeExpenses(Template):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - We Expenses")
        self.person_count = 3
        self.inputs = []
        self.initContent()
        self.initMenu()

    def initContent(self):
        content_layout = QVBoxLayout()

        create_new_group_label = QLabel("Create New Group")
        create_new_group_label.setFont(QFont("Arial", 20, QFont.Bold))
        content_layout.addWidget(create_new_group_label, alignment=Qt.AlignCenter)

        self.form_layout = QGridLayout()
        self.form_layout.setHorizontalSpacing(10)
        self.form_layout.setVerticalSpacing(10)
        self.form_layout.setContentsMargins(40, 0, 40, 0)

        self.add_form_row(0,"Group Name:", "Enter group name")
        self.add_form_row(1,"Add Total Amount:", "Enter total amount")
        self.add_form_row(2,"Add friend 1:", "Enter friend's name")
        self.add_form_row(3,"Add friend 2:", "Enter friend's name")
        self.add_form_row(4,"Add friend 3:", "Enter friend's name")

        content_layout.addLayout(self.form_layout)

        add_person_button = QPushButton("Add another person")
        add_person_button.setFont(QFont("Arial", 16))
        add_person_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        add_person_button.clicked.connect(self.add_person_row)
        content_layout.addWidget(add_person_button, alignment=Qt.AlignCenter)

        complete_button = QPushButton("Complete")
        complete_button.setFont(QFont("Arial", 16))
        complete_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        complete_button.clicked.connect(self.show_popup)
        content_layout.addWidget(complete_button, alignment=Qt.AlignCenter)


        self.addContent(content_layout)

    def add_form_row(self, row, label_text, placeholder_text=""):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 16))
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setFixedHeight(30)
        input_field.setFixedWidth(400)
        input_field.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        self.form_layout.addWidget(label, row, 0, Qt.AlignLeft)
        self.form_layout.addWidget(input_field, row, 1, Qt.AlignRight)
        self.inputs.append((label_text, input_field))

    def add_person_row(self):
        self.person_count += 1
        self.add_form_row(self.form_layout.rowCount(), f"Add friend {self.person_count}:", "Enter friend's name")
                      
    def show_popup(self):
        summary = ""
        for label_text, input_field in self.inputs:
            summary += f"{label_text} {input_field.text()}\n"
        
        self.popup_window = CustomPopupWindow(summary)
        self.popup_window.show()
