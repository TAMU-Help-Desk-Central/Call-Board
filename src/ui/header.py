from email import header
import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from PyQt5 import QtSvg

class HeaderLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        logo = QtSvg.QSvgWidget("images/TAMULogo.svg")
        scaleFactor = 2.5
        logo.setFixedSize(int(197.91*scaleFactor), int(48.05*scaleFactor))
        self.addWidget(logo)
        self.addWidget(QWidget())
        self.addWidget(QLabel("4:00PM"))

class Header(QWidget):
    def __init__(self):
        super().__init__()
        with open("src/style-sheets/header.qss", 'r') as f:
            self.setStyleSheet(f.read())

        headerLayout = HeaderLayout()
        self.setLayout(headerLayout)