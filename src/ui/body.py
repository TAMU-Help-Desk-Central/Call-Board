import sys
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class AgentState(QTableWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize columns
        self.setColumnCount(2)  
        self.setHorizontalHeaderLabels(["Technician", "Duration"])

        # Set column widths
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        # Initialize rows
        self.rowCount = 4
        self.fillRows()

        # Disable focusing cells (unless clicked... don't click on the cells)
        self.setFocusPolicy(0)
        self.setSelectionBehavior(0)
    
    def fillRows(self):
        # Set the row count
        self.setRowCount(self.rowCount)

        # Set the data for each row (placeholder for now)
        for i in range(self.rowCount):
            rowHeaderItem = QTableWidgetItem("   ")  # Sets the thickness of the header
            rowHeaderItem.setBackground(QtGui.QColor(0, 255, 0))  # Colors the header to the ready state
            self.setVerticalHeaderItem(i, rowHeaderItem)
            self.setItem(i, 0, QTableWidgetItem("Braeden S."))  # Set the technician name
            self.setItem(i, 1, QTableWidgetItem(str(6 - i) + ":00"))  # Set the time in state

class Body(QHBoxLayout):
    def __init__(self):
        super().__init__()

        midLabel = QLabel("Middle Section")
        self.addWidget(AgentState())
        self.addWidget(midLabel)