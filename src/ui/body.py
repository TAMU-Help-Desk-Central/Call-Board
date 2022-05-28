from datetime import datetime
from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using
from ui import queueAndPosData, snowData, stateData

class Body(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)

        # Initialize the three primary components
        self.agentState = stateData.AgentState()
        self.queuePosData = queueAndPosData.QueueAndPositionState()
        self.serviceNowData = snowData.ServiceNowData()

        # Attach the three primary components
        self.addLayout(self.agentState, stretch=5)
        self.addLayout(self.queuePosData, stretch=3)
        self.addLayout(self.serviceNowData, stretch=2)
    
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