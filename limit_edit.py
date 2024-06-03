from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtGui import QFont
from template import Template

class LimitEditorWindow(Template):
    limit_saved = pyqtSignal(str, str, name='limitSaved')

    def __init__(self, limit_data=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("PocketGuard - Limit Editor")
        self.old_category = limit_data[0] if limit_data else None
        self.old_limit = limit_data[1] if limit_data else "0"
        self.initContent()

    def initContent(self):
        content_layout = QVBoxLayout()

        if self.old_category: 
            header_label = QLabel("Edit Limit")
        else:
            header_label = QLabel("Add New Limit")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        content_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)
        form_layout.setContentsMargins(40, 0, 40, 0)

        self.name_input = QLineEdit()
        if self.old_category:
            self.name_input.setText(self.old_category)
        self.name_input.setPlaceholderText("Enter category name")
        self.name_input.setFixedHeight(30)
        self.name_input.setFixedWidth(400)
        self.name_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        form_layout.addWidget(QLabel("Category Name:"), 0, 0, Qt.AlignLeft)
        form_layout.addWidget(self.name_input, 0, 1, Qt.AlignRight)

        self.limit_input = QLineEdit()
        if self.old_limit:
            self.limit_input.setText(self.old_limit)
        self.limit_input.setPlaceholderText("Enter limit amount")
        self.limit_input.setFixedHeight(30)
        self.limit_input.setFixedWidth(400)
        self.limit_input.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        form_layout.addWidget(QLabel("Limit Amount:"), 1, 0, Qt.AlignLeft)
        form_layout.addWidget(self.limit_input, 1, 1, Qt.AlignRight)

        content_layout.addLayout(form_layout)

        save_button = QPushButton("Save")
        save_button.setFont(QFont("Arial", 16))
        save_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        save_button.clicked.connect(self.save_limit)
        content_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.addContent(content_layout)

    def save_limit(self):
        category_name = self.name_input.text()
        limit_amount = self.limit_input.text()
        if category_name and limit_amount:
            self.limit_saved.emit(category_name, limit_amount) 
            print(f"Saved limit: {category_name}, Amount: {limit_amount}")
            self.close()
