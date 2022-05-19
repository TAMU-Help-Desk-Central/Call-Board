class bomgar():
    def __init__(self):
        self.username = ""
        self.password = ""
class scheduleSource():
    def __init__(self):
        self.token = ""
class servicenow():
    def __init__(self):
        self.username = ""
        self.password = ""

class secrets():
    def __init__(self):
        self.bomgar = bomgar()
        self.scheduleSource = scheduleSource()
        self.servicenow = servicenow()