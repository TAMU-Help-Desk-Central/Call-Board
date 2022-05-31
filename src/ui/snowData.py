from turtle import update
from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Active(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize a label for the different incident count views
        self.activeTotal = QLabel("0")
        self.activeTotal.setObjectName("IncidentCounter")
        self.over4 = QLabel("0 ≥ 4 hrs")
        self.over4.setObjectName("SmallIncidentCounter")
        self.over2 = QLabel("0 ≥ 2 hrs")
        self.over2.setObjectName("SmallIncidentCounter")
        self.under2 = QLabel("0 < 2 hrs")
        self.under2.setObjectName("SmallIncidentCounter")

        # Create the vertical layout for the time breakdown on the right
        incidentTimesLayout = QVBoxLayout()
        incidentTimesLayout.addWidget(self.over4)
        incidentTimesLayout.addWidget(self.over2)
        incidentTimesLayout.addWidget(self.under2)

        # Create the horizontal layout which encompasses the total and breakdown
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.activeTotal)
        hLayout.addLayout(incidentTimesLayout)

        # Add a label to the top and attach the layout
        activeLabel = QLabel("Active Incidents")
        activeLabel.setObjectName("SubSectionHeader")
        self.addWidget(activeLabel)
        self.addLayout(hLayout)
        self.updateIncidents(2, 0, 1)
    
    def updateIncidents(self, over4:int, over2:int, under2:int):
        # Set the individual views to hold the corresponding new value
        self.over4.setText(str(over4) + " ≥ 4 hrs")
        self.over2.setText(str(over2) + " ≥ 2 hrs")
        self.under2.setText(str(under2) + " < 2 hrs")

        # Set the background color of the main incident count
        if over4 > 0:
            self.activeTotal.setStyleSheet("background-color: #FF8494")  # Pastel red
        elif over2 > 0:
            self.activeTotal.setStyleSheet("background-color: #FFD87F")  # Pastel yellow
        elif under2 > 0:
            self.activeTotal.setStyleSheet("background-color: #D0FFCE")  # Pastel green
        else:
            self.activeTotal.setStyleSheet("background-color: white")

        # Set the total to the sum of all the incidents
        self.activeTotal.setText(str(over4 + over2 + under2))

class OnHoldTriage(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        # Initialize labels for the on hold and triage incidents
        self.onHold = QLabel("0")
        self.triage = QLabel("0")
        self.onHold.setObjectName("IncidentCounter")
        self.triage.setObjectName("IncidentCounter")
        
        # Initialize and fill the vertical layout for the on hold tickets
        onHoldLayout = QVBoxLayout()
        onHoldLabel = QLabel("On Hold")
        onHoldLabel.setObjectName("SubSectionHeader")
        onHoldLayout.addWidget(onHoldLabel)
        onHoldLayout.addWidget(self.onHold)

        # Initialize and fill the vertical layout for the triage tickets
        triageLayout = QVBoxLayout()
        triageLabel = QLabel("Triage")
        triageLabel.setObjectName("SubSectionHeader")
        triageLayout.addWidget(triageLabel)
        triageLayout.addWidget(self.triage)

        # Attach the two layouts
        self.addLayout(onHoldLayout)
        self.addLayout(triageLayout)
    
    def updateOnHold(self, onHold:int):
        # Set the text of on hold label
        self.onHold.setText(str(onHold))

    def updateTriage(self, triage:int):
        # Set the text of on triage label
        self.triage.setText(str(triage))

class ServiceNowContentsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Remove all spacing around the elements
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        
        # Initialize the two separate view layouts
        self.activeLayout = Active()
        self.ohtLayout = OnHoldTriage()

        # Add the layouts under a label for the section
        snowHeader = QLabel("ServiceNow")
        snowHeader.setObjectName("SectionHeader")
        self.addWidget(snowHeader)
        self.addLayout(self.activeLayout)
        self.addLayout(self.ohtLayout)

class ServiceNowContentsFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("SectionFrame")

        # Set the alignment of all text in this element to centered
        self.setStyleSheet("QLabel { qproperty-alignment: AlignCenter; }")

        # Initialize and set the layout
        self.contentsLayout = ServiceNowContentsLayout()
        self.setLayout(self.contentsLayout)

class ServiceNowData(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize a frame that will display all of the contents
        self.contentsFrame = ServiceNowContentsFrame()

        # Surround the frame by stretches to center it
        self.addWidget(self.contentsFrame)
        self.addStretch()

    def updateIncidents(self, over4:int, over2:int, under2:int, onHold:int, triage:int):
        # Call the lower-level methods which will update the data
        self.contentsFrame.contentsLayout.activeLayout.updateIncidents(over4, over2, under2)

        # Call the lower-level method that updates on hold incidents
        self.contentsFrame.contentsLayout.ohtLayout.updateOnHold(onHold)

        # Call the lower-level method that updates triage calls
        self.contentsFrame.contentsLayout.ohtLayout.updateTriage(triage)
    
    def updateActiveIncidents(self, over4:int, over2:int, under2:int):
        # Call the lower-level method that updates active incident counts
        self.contentsFrame.contentsLayout.activeLayout.updateIncidents(over4, over2, under2)

    def updateOnHold(self, onHold:int):
        # Call the lower-level method that updates on hold incidents
        self.contentsFrame.contentsLayout.ohtLayout.updateOnHold(onHold)

    def updateTriage(self, triage:int):
        # Call the lower-level method that updates triage calls
        self.contentsFrame.contentsLayout.ohtLayout.updateTriage(triage)