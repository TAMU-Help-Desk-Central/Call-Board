from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Active(QVBoxLayout):
    def __init__(self):
        super().__init__()

        incidentTimesLayout = QVBoxLayout()
        self.over4 = QLabel("x ≥ 4 hrs")
        incidentTimesLayout.addWidget(self.over4)
        self.over2 = QLabel("x ≥ 2 hrs")
        incidentTimesLayout.addWidget(self.over2)
        self.under2 = QLabel("x < 2 hrs")
        incidentTimesLayout.addWidget(self.under2)

        hLayout = QHBoxLayout()
        self.activeTotal = QLabel("x")
        hLayout.addWidget(self.activeTotal)
        hLayout.addLayout(incidentTimesLayout)

        self.addWidget(QLabel("Active Incidents"))
        self.addLayout(hLayout)
    
    def updateIncidents(self, over4, over2, under2):
        self.over4.setText(str(over4) + " ≥ 4 hrs")
        self.over2.setText(str(over2) + " ≥ 2 hrs")
        self.under2.setText(str(under2) + " < 2 hrs")

        self.activeTotal.setText(str(over4 + over2 + under2))



class OnHoldTriage(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        onHoldLayout = QVBoxLayout()
        onHoldLayout.addWidget(QLabel("On Hold"))
        self.onHold = QLabel("x")
        onHoldLayout.addWidget(self.onHold)

        triageLayout = QVBoxLayout()
        triageLayout.addWidget(QLabel("Triage"))
        self.triage = QLabel("x")
        triageLayout.addWidget(self.triage)

        self.addLayout(onHoldLayout)
        self.addLayout(triageLayout)

    def updateIncidents(self, onHold, triage):
        self.onHold.setText(str(onHold))
        self.triage.setText(str(triage))

class ServiceNowData(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.addWidget(QLabel("ServiceNow"))
        self.activeLayout = Active()
        self.addLayout(self.activeLayout)
        self.ohtLayout = OnHoldTriage()
        self.addLayout(self.ohtLayout)

    def updateIncidents(self, over4, over2, under2, onHold, triage):
        self.activeLayout.updateIncidents(over4, over2, under2)
        self.ohtLayout.updateIncidents(onHold, triage)