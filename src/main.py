import sys
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from ui import body, footer, header
import pidfile

class MainWindowLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize the primary components of the window
        headerLayout = header.Header()
        self.bodyLayout = body.Body()
        footerLayout = footer.Footer()

        # Attach components
        self.addLayout(headerLayout)
        self.addLayout(self.bodyLayout)
        self.addLayout(footerLayout)
    
    def getBody(self) -> body.Body:
        return self.bodyLayout

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set windows title and size
        self.setWindowTitle("Call Board")
        self.resize(1920, 1080) # TODO: Set to fullscreen before deployment

        # Set up and add the main layout for the window
        mainWindowLayout = MainWindowLayout()
        self.setLayout(mainWindowLayout) # TODO: Change to QBorderLayout

print('Starting process')
try:
    with pidfile.PIDFile():
        print('Process started')
        if __name__ == "__main__":
            # Create and initialize the application
            app = QApplication(sys.argv)
            app.setStyle(QStyleFactory.create('Fusion'))

            # Create and initialize the window
            window = Window()

            # Show the window
            window.show()

            # Allow the app to continue running
            sys.exit(app.exec_())
except pidfile.AlreadyRunningError:
    print('Already running.')