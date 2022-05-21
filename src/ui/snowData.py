from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class Active(QVBoxLayout):
    def __init__(self):
        super().__init__()

        incidentTimesLayout = QVBoxLayout()
        incidentTimesLayout.addWidget(QLabel(str(1) + " ≥ 4 hrs"))
        incidentTimesLayout.addWidget(QLabel(str(3) + " ≥ 2 hrs"))
        incidentTimesLayout.addWidget(QLabel(str(2) + " < 2 hrs"))

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("16"))
        hLayout.addLayout(incidentTimesLayout)

        self.addWidget(QLabel("Active Incidents"))
        self.addLayout(hLayout)

class OnHoldTriage(QHBoxLayout):
    def __init__(self):
        super().__init__()
        
        onHold = QVBoxLayout()
        onHold.addWidget(QLabel("On Hold"))
        onHold.addWidget(QLabel("12"))

        triage = QVBoxLayout()
        triage.addWidget(QLabel("Triage"))
        triage.addWidget(QLabel("8"))

        self.addLayout(onHold)
        self.addLayout(triage)

class ServiceNowData(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.addWidget(QLabel("ServiceNow"))
        self.addLayout(Active())
        self.addLayout(OnHoldTriage())