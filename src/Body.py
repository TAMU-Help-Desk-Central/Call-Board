import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Body(QHBoxLayout):
    def __init__(self):
        super().__init__()

        spacer = QWidget()
        spacer.setFixedSize(0, 800) # not a perfect solution
        midLabel = QLabel("Middle Section")
        self.addWidget(spacer)
        self.addWidget(midLabel)