import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from ui import body, footer, header

class MainWindowLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        header = header.Header()
        body = body.Body()
        footer = footer.Footer()

        self.addLayout(header)
        self.addLayout(body)
        self.addLayout(footer)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.resize(1920, 1080)

        mainWindowLayout = MainWindowLayout()
        self.setLayout(mainWindowLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = Window()
    window.show()
    sys.exit(app.exec_())