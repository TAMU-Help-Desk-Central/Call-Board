import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from ui import body, footer, header

class MainWindowLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # Initialize the primary components of the window
        headerWidget = header.Header()
        self.bodyWidget = body.Body()
        footerLayout = footer.Footer()

        # Attach components
        self.addWidget(headerWidget)
        self.addWidget(self.bodyWidget)
        self.addLayout(footerLayout)
    
    def getBody(self) -> body.Body:
        return self.bodyWidget

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set windows title and size
        self.setWindowTitle("Call Board")
        self.resize(1920, 1080) # TODO: Set to fullscreen before deployment

        # Set up and add the main layout for the window
        mainWindowLayout = MainWindowLayout()
        self.setLayout(mainWindowLayout) # TODO: Change to QBorderLayout

if __name__ == '__main__':
    # Create and initialize the application
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    # Create and initialize the window
    window = Window()

    # Show the window
    window.show()

    # Allow the app to continue running
    sys.exit(app.exec_())