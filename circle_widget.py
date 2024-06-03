from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont

class CircleWidget(QWidget):
    def __init__(self, color, amount=0, size=150, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.amount = amount
        self.setFixedSize(size, size) 

        self.amount_label = QLabel(f"${self.amount:.2f}", self)
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.amount_label.setFont(QFont("Arial", 16))
        self.amount_label.setStyleSheet("color: black;")  

        layout = QVBoxLayout(self)
        layout.addWidget(self.amount_label)
        layout.setAlignment(Qt.AlignCenter)

    def setAmount(self, amount):
        self.amount = amount
        self.amount_label.setText(str(self.amount))
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(0, 0, self.width(), self.height())