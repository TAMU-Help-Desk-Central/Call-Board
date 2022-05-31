from datetime import datetime, timedelta
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class AgentRowData(QHBoxLayout):
    def __init__(self, name:str, state:str, startTime:datetime):
        super().__init__()

        # Initialize variables
        self.agentName = name
        self.agentState = state
        self.stateStart = startTime

        # Set the initial state of the labels based on initial variables
        self.stateLabel = QLabel()
        self.stateLabel.setObjectName("SubSectionHeader")
        self.nameLabel = QLabel(name)
        self.nameLabel.setObjectName("SubSectionHeader")
        self.timeLabel = QLabel("0:00")
        self.timeLabel.setObjectName("SubSectionHeader")

        # Set the color of the state section
        self.stateLabel.setStyleSheet("background-color: " +   {"talking": "#CCCCFF",
                                                                "reserved": "#A7A7A7",
                                                                "ready": "#CCFFCC",
                                                                "work": "#FFFF99",
                                                                "not ready": "#FF8494"
                                                                }.get(state, "white"))
        
        # Align the timer text to the right
        self.timeLabel.setStyleSheet("qproperty-alignment: AlignRight")

        # Add all of the widgets to the layout
        self.addWidget(self.stateLabel, stretch=1)
        self.addWidget(self.nameLabel, stretch=18)
        self.addWidget(self.timeLabel, stretch=7)

    def updateTimer(self):
        # Convert the start time of the state into a timedelta
        timeInState = datetime.now() - self.stateStart

        # Display the timedelta of the state's time
        minutes = timeInState.seconds // 60
        seconds = timeInState.seconds % 60
        self.timeLabel.setText("{:d}:{:02d}".format(minutes, seconds))

        # Set the color of the cell based on the time of the call
        if timeInState > timedelta(minutes=30) and self.agentState == "talking":
            self.timeLabel.setStyleSheet("background-color: #FF2348")
        elif timeInState > timedelta(minutes=15) and self.agentState == "talking":
            self.timeLabel.setStyleSheet("background-color: #FFAD21")

    def getStateTime(self):
        return datetime.now() - self.stateStart
    
    def setPrimaryRowColor(self):
        self.nameLabel.setStyleSheet("background-color: #EDEDED")
        self.timeLabel.setStyleSheet("background-color: #EDEDED")

    def setAlternateRowColor(self):
        self.nameLabel.setStyleSheet("background-color: #BCBCBC")
        self.timeLabel.setStyleSheet("background-color: #BCBCBC")

class AgentStateContentsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Set all spacing to 0
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # Initialize a condition for whether the table was just updated or not
        self.justUpdated = True

        # Initialize a layout for the header of the table
        self.headerLayout = QHBoxLayout()
        
        # Initialize the labels for each section
        stateLabel = QLabel("")
        stateLabel.setObjectName("SectionHeader")
        nameLabel = QLabel("Name")
        nameLabel.setObjectName("SectionHeader")
        timeLabel = QLabel("Time")
        timeLabel.setObjectName("SectionHeader")

        # Right-align time
        timeLabel.setStyleSheet("qproperty-alignment: AlignRight")

        # Add the labels for each section of the header
        self.headerLayout.addWidget(stateLabel, stretch=1)
        self.headerLayout.addWidget(nameLabel, stretch=18)
        self.headerLayout.addWidget(timeLabel, stretch=7)
        
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
            "work": self.workList,
            "not ready": self.notReadyList
            # Other is omitted and will be used as a default
        }

        # Add the header to the layout
        self.addLayout(self.headerLayout)

        # Add each of the subdivisions to the layout
        self.addLayout(self.talkingList)
        self.addLayout(self.reservedList)
        self.addLayout(self.readyList)
        self.addLayout(self.workList)
        self.addLayout(self.notReadyList)
        self.addLayout(self.otherList)

        # Initialize a timer to keep track of the waiting time
        timer = QtCore.QTimer(self)

        # Attach the timer update method to the timer
        timer.timeout.connect(self.updateTimes)

        # Update the timer every second
        timer.start(100)  # TODO: This timer is janky for some reason. I'll fix it later.
    
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
        alternateColor = False

        # Update the timer for every row in every list
        for agentList in self.agentLists.values():
            for rowIndex in range(agentList.count()):
                # Change the color of the row
                if self.justUpdated:
                    if alternateColor:
                        agentList.itemAt(rowIndex).setAlternateRowColor()
                    else:
                        agentList.itemAt(rowIndex).setPrimaryRowColor()
                    
                    # Flip the alternate color flag
                    alternateColor = not alternateColor
                
                agentList.itemAt(rowIndex).updateTimer()
        
        # Deactivate justUpdated
        if self.justUpdated:
            self.justUpdated = False

class AgentStateFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("SectionFrame")

        # Give all of the labels borders
        #self.setStyleSheet("QLabel { border-color: #500000; border-style: solid; border-width: 1px; }")

        # Initialize and set the layout
        self.contentsLayout = AgentStateContentsLayout()
        self.setLayout(self.contentsLayout)

class AgentState(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize a frame that will display all of the contents
        self.contentsFrame = AgentStateFrame()

        # Surround the frame by stretches to center it
        self.addWidget(self.contentsFrame)
        self.addStretch()
    
    def addAgent(self, name:str, state:str, startTime:datetime):
        # Call the lower level method which will add the agent
        self.contentsFrame.contentsLayout.addAgent(name, state, startTime)

    def changeAgent(self, name:str, state:str, startTime:datetime):
        # Call the lower level method which will change the agent
        self.contentsFrame.contentsLayout.changeAgent(name, state, startTime)

    def removeAgent(self, name:str):
        # Call the lower level method which will remove the agent
        self.contentsFrame.contentsLayout.removeAgent(name)