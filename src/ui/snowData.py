from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Active(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize a label for the different incident count views
        self.activeTotal = QLabel("x")
        self.over4 = QLabel("x ≥ 4 hrs")
        self.over2 = QLabel("x ≥ 2 hrs")
        self.under2 = QLabel("x < 2 hrs")

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
        self.addWidget(QLabel("Active Incidents"))
        self.addLayout(hLayout)
    
    def updateIncidents(self, over4:int, over2:int, under2:int):
        # Set the individual views to hold the corresponding new value
        self.over4.setText(str(over4) + " ≥ 4 hrs")
        self.over2.setText(str(over2) + " ≥ 2 hrs")
        self.under2.setText(str(under2) + " < 2 hrs")

        # Set the total to the sum of all the incidents
        self.activeTotal.setText(str(over4 + over2 + under2))

class OnHoldTriage(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        # Initialize labels for the on hold and triage incidents
        self.onHold = QLabel("x")
        self.triage = QLabel("x")
        
        # Initialize and fill the vertical layout for the on hold tickets
        onHoldLayout = QVBoxLayout()
        onHoldLayout.addWidget(QLabel("On Hold"))
        onHoldLayout.addWidget(self.onHold)

        # Initialize and fill the vertical layout for the triage tickets
        triageLayout = QVBoxLayout()
        triageLayout.addWidget(QLabel("Triage"))
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

class ServiceNowData(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        # Initialize the two separate view layouts
        self.activeLayout = Active()
        self.ohtLayout = OnHoldTriage()

        # Add the layouts under a label for the section
        self.addWidget(QLabel("ServiceNow"))
        self.addLayout(self.activeLayout)
        self.addLayout(self.ohtLayout)
        self.addStretch()

    def updateIncidents(self, over4:int, over2:int, under2:int, onHold:int, triage:int):
        # Call the lower-level methods which will update the data
        self.activeLayout.updateIncidents(over4, over2, under2)

        # Call the lower-level method that updates on hold incidents
        self.ohtLayout.updateOnHold(onHold)

        # Call the lower-level method that updates triage calls
        self.ohtLayout.updateTriage(triage)
    
    def updateActiveIncidents(self, over4:int, over2:int, under2:int):
        # Call the lower-level method that updates active incident counts
        self.activeLayout.updateIncidents(over4, over2, under2)

    def updateOnHold(self, onHold:int):
        # Call the lower-level method that updates on hold incidents
        self.ohtLayout.updateOnHold(onHold)

    def updateTriage(self, triage:int):
        # Call the lower-level method that updates triage calls
        self.ohtLayout.updateTriage(triage)