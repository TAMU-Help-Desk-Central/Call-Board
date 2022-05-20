import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from PyQt5 import QtGui

class Header(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("Texas A&M"))
        logo = QLabel("Texas A&M")
        logo.setPixmap(QtGui.QPixmap("images/TAMULogoShaheer.svg"))
        self.addWidget(logo)
        self.addWidget(QLabel("4:00PM"))