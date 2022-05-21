import datetime
from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from ui import queueAndPosData, snowData

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
        self.rowCount = 0
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
            self.setItem(i, 0, QTableWidgetItem("x"))  # Set the technician name
            self.setItem(i, 1, QTableWidgetItem("x" + ":00"))  # Set the time in state

class Body(QHBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize the three primary components
        self.agentState = AgentState()
        self.queuePosData = queueAndPosData.QueueAndPositionState()
        self.serviceNowData = snowData.ServiceNowData()

        # Attach the three primary components
        self.addWidget(self.agentState)
        self.addLayout(self.queuePosData)
        self.addLayout(self.serviceNowData)
    
    def updatePhones(self, count:int, longestStartTime:datetime):
        # Just call lower-level method to update the phones queue
        self.queuePosData.updatePhones(count, longestStartTime)

    def updateBomgar(self, count:int, longestStartTime:datetime):
        # Just call lower-level method to update the bomgar queue
        self.queuePosData.updateBomgar(count, longestStartTime)

    def updatePositions(self, employees:dict[str, str]):
        # Just call lower-level method to update the positions
        self.queuePosData.updatePositions(employees)

    def updateIncidents(self, over4:int, over2:int, under2:int, onHold:int, triage:int):
        # Call the lower-level method which will update the queue data
        self.serviceNowData.updateIncidents(over4, over2, under2, onHold, triage)

    def updateActiveIncidents(self, over4:int, over2:int, under2:int):
        # Call the lower-level method that updates active incident counts
        self.serviceNowData.updateActiveIncidents(over4, over2, under2)

    def updateOnHold(self, onHold:int):
        # Call the lower-level method that updates on hold incidents
        self.serviceNowData.updateOnHold(onHold)

    def updateTriage(self, triage:int):
        # Call the lower-level method that updates triage calls
        self.serviceNowData.updateTriage(triage)