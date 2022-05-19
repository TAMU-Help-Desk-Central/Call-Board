import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Header(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(QLabel("Texas A&M"))
        self.addWidget(QLabel("4:00PM"))