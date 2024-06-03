from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout
from PyQt5.QtGui import QFont
from template import Template

class CategoryEditorWindow(Template):
    category_saved = pyqtSignal(str, str, name='categorySaved') 

    def __init__(self, category_data=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("PocketGuard - Category Editor")
        self.old_category = category_data[0] if category_data else None
        self.old_provider = category_data[1] if category_data else "Provider 1"
        self.initContent()

    def initContent(self):
        content_layout = QVBoxLayout()

        if self.old_category:
            header_label = QLabel("Edit Category")
        else:
            header_label = QLabel("Add New Category")
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

        self.provider_combo = QComboBox()
        self.provider_combo.addItem("Provider 1")
        self.provider_combo.addItem("Provider 2")
        self.provider_combo.addItem("Provider 3")
        if self.old_provider:
            index = self.provider_combo.findText(self.old_provider)
            if index >= 0:
                self.provider_combo.setCurrentIndex(index)
        self.provider_combo.setFixedHeight(30)
        self.provider_combo.setFixedWidth(400)
        self.provider_combo.setStyleSheet("border-radius: 10px; background-color: #00FFFF; color: black;")
        form_layout.addWidget(QLabel("Shop/Provider:"), 1, 0, Qt.AlignLeft)
        form_layout.addWidget(self.provider_combo, 1, 1, Qt.AlignRight)

        content_layout.addLayout(form_layout)

        save_button = QPushButton("Save")
        save_button.setFont(QFont("Arial", 16))
        save_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        save_button.clicked.connect(self.save_category)
        content_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.addContent(content_layout)

    def save_category(self):
        category_name = self.name_input.text()
        provider = self.provider_combo.currentText()
        if category_name:
            self.category_saved.emit(category_name, provider) 
            print(f"Saved category: {category_name}, Provider: {provider}")
            self.close()
        else:
            self.show_popup("Error", "Please enter a category name.")

