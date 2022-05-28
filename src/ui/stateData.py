from datetime import datetime
from xmlrpc.client import DateTime
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import * # will limit once I know what I'm using

def stateColor(state:str):
    stateColors = {
        "talking": "purple",
        "reserved": "gray",
        "ready": "green",
        "not ready": "red",
        "work": "yellow"
    }
    return stateColors.get(state, "white")

class AgentRowData(QHBoxLayout):
    def __init__(self, name:str, state:str, startTime:datetime):
        super().__init__()

        # Initialize variables
        self.agentName = name
        self.agentState = state
        self.stateStart = startTime

        # Set the initial state of the labels based on initial variables
        self.stateLabel = QLabel()
        self.stateLabel.setStyleSheet("background-color: " + stateColor(state))
        self.nameLabel = QLabel(name)
        self.timeLabel = QLabel("0:00")

        # Update the time
        self.updateTimer()

        # Add all of the widgets to the layout
        self.addWidget(self.stateLabel, stretch=1)
        self.addWidget(self.nameLabel, stretch=20)
        self.addWidget(self.timeLabel, stretch=5)

    def updateTimer(self):
        # Convert the start time of the state into a timedelta
        timeInState = datetime.now() - self.stateStart

        # Display the timedelta of the state's time
        minutes = timeInState.seconds // 60
        seconds = timeInState.seconds % 60
        self.timeLabel.setText("{:d}:{:02d}".format(minutes, seconds))

    def getStateTime(self):
        return datetime.now() - self.stateStart

class AgentState(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize a layout for the header of the table
        self.headerLayout = QHBoxLayout()
        
        # Add the labels for each section of the header
        self.headerLayout.addWidget(QLabel(""), stretch=1)
        self.headerLayout.addWidget(QLabel("Name"), stretch=20)
        self.headerLayout.addWidget(QLabel("Time"), stretch=5)
        self.addWidget(QLabel("Time"))
        
        # Initialize the lists of the technicians' rows
        self.talkingList = QVBoxLayout()
        self.reservedList = QVBoxLayout()
        self.readyList = QVBoxLayout()
        self.notReadyList = QVBoxLayout()
        self.workList = QVBoxLayout()
        self.otherList = QVBoxLayout()  # For any technician who's state does not fit into the about categories

        # Create a dictionary of these lists
        self.agentLists = {
            "talking": self.talkingList,
            "reserved": self.reservedList,
            "ready": self.readyList,
            "not ready": self.notReadyList,
            "work": self.workList
            # Other is omitted and will be used as a default
        }

        # Add the header to the layout
        self.addLayout(self.headerLayout)

        # Add each of the subdivisions to the layout
        self.addLayout(self.talkingList)
        self.addLayout(self.reservedList)
        self.addLayout(self.readyList)
        self.addLayout(self.notReadyList)
        self.addLayout(self.workList)
        self.addLayout(self.otherList)

        # Make the layout stop when it is over
        self.addStretch()

        # Initialize a timer to keep track of the waiting time
        timer = QtCore.QTimer(self)

        # Attach the timer update method to the timer
        timer.timeout.connect(self.updateTimes)

        # Update the timer every second
        timer.start(3000)  # TODO: This timer is janky for some reason. I'll fix it later.
    
    def addAgent(self, name:str, state:str, startTime:datetime):
        agentRow = AgentRowData(name, state, startTime)
        agentList = self.agentLists.get(state, self.otherList)

        # Iterate through each element of the row and add the agent
        for rowIndex in range(agentList.count()):
            if agentRow.getStateTime() > agentList.itemAt(rowIndex).getStateTime():
                # Add the widget to its proper location
                agentList.insertLayout(rowIndex, agentRow)
                return
        
        # If the state is the shortest time, put it at the bottom
        agentList.addLayout(agentRow)

    def changeAgent(self, name:str, state:str, startTime:datetime):
        # Remove the agent from the list and store it
        self.removeAgent(name)

        # Re-add the agent to the new state
        self.addAgent(name, state, startTime)

    def removeAgent(self, name:str):
        # Check every list for the technician and remove them when found
        for agentList in self.agentLists.values():
            for rowIndex in range(agentList.count()):
                if agentList.itemAt(rowIndex).agentName == name:
                    agentList.takeAt(rowIndex)
                    return

    def updateTimes(self):
        # Update the timer for every row in every list
        for agentList in self.agentLists.values():
            for rowIndex in range(agentList.count()):
                agentList.itemAt(rowIndex).updateTimer()