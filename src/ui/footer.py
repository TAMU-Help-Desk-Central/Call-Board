import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class FooterLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.addWidget(QLabel("Haha Dad Joke"))
        self.addStretch()
        self.addWidget(QLabel("Weather Last Updated: 4:00PM"))

class Footer(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("padding: 10px")

        footerLayout = FooterLayout()
        self.setLayout(footerLayout)