import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Footer(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(QLabel("Haha Dad Joke"))
        self.addWidget(QLabel("Weather Last Updated: 4:00PM"))