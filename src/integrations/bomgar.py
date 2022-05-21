from datetime import datetime
import websocket
import rel
import json
import requests
from os import environ as env

teamId = 2

bearerToken = ""
queueId = ""


class sessions:
    currentSessions = []

    def __sessionExists__(self, sessionId):
        for session in self.currentSessions:
            if session["id"] == sessionId:
                return True
        return False

    def addSession(self, thisSessionId: int, thisQueueId: int, startTime: int):
        """Add (or update) a session

        Args:
                thisSessionId (int): the session ID from Bomgar
                thisQueueId (int): the queue ID from Bomgar
                startTime (int): the start time from Bomgar, in epoch time

        Returns:
                bool: True if something was added or updated, False if removed or ignored
        """

        if self.__sessionExists__(thisSessionId):
            # Update
            for sessionIndex in range(len(self.currentSessions)):
                if (self.currentSessions[sessionIndex]["id"] == thisSessionId) and (thisQueueId != queueId):
                    self.currentSessions.pop(sessionIndex)
                    return False
                return True
        else:
            # Add
            if queueId == thisQueueId:
                self.currentSessions.append(
                    {"id": thisSessionId, "startTime": datetime.fromtimestamp(startTime)})
                return True
            return False

    def removeSession(self, thisSessionId: int):
        """Remove a session if it exists

        Args:
                thisSessionId (int): the session ID from Bomgar

        Returns:
                bool: Returns True if something was removed, False if else
        """
        if self.__sessionExists__(thisSessionId):
            # Update
            for sessionIndex in range(len(self.currentSessions)):
                if (self.currentSessions[sessionIndex]["id"] == thisSessionId):
                    self.currentSessions.pop(sessionIndex)
                    return True
                return False
        else:
            return False

    def earliestStartTime(self):
        if len(self.currentSessions) == 0:
            return datetime.now()
        return sorted(self.currentSessions, key=lambda x: x["startTime"])[0]["startTime"]

    def numberSessions(self):
        return len(self.currentSessions)


currentSessions = sessions()


def onModelInsert(ws, jsonData):
    root = jsonData["insert"]
    for table in root:
        if table == "support_session":
            for session in root[table]:
                # if root[table][session]["queue_id"] == queueId:
                print("--------------------\n" +
                      str(json.dumps(root[table][session], indent=4)) + "\n--------------------")
                currentSessions.addSession(
                    session, root[table][session]["queue_id"], root[table][session]["queue_entry_timestamp"])
    print(currentSessions.earliestStartTime())
    print(currentSessions.numberSessions())


def onModelUpdate(ws, jsonData):
    root = jsonData["update"]
    for table in root:
        if table == "support_session":
            for session in root[table]:
                # if root[table][session]["queue_id"] == queueId:
                currentSessions.addSession(
                    session, root[table][session]["queue_id"], root[table][session]["queue_entry_timestamp"])
                print("--------------------\n" +
                      str(json.dumps(root[table][session], indent=4)) + "\n--------------------")
    print(currentSessions.earliestStartTime())
    print(currentSessions.numberSessions())


def onModelDelete(ws, jsonData):
    root = jsonData["delete"]
    for table in root:
        if table == "support_session":
            for session in root[table]:
                # if root[table][session]["queue_id"] == queueId:
                print("--------------------\n" +
                      str(json.dumps(root[table], indent=4)) + "\n--------------------")
                currentSessions.removeSession(root[table][0])
    print(currentSessions.earliestStartTime())
    print(currentSessions.numberSessions())


def updateBearerToken(func):
    def wrap(*args, **kwargs):
        global bearerToken
        bearerToken = (json.loads(requests.post("https://bomgar-app.tamu.edu/oauth2/token?grant_type=client_credentials",
                       auth=requests.auth.HTTPBasicAuth(env["BOMGAR_USERNAME"], env["BOMGAR_PASSWORD"])).text)["access_token"])
        print("Bearer Token:", bearerToken)
        func(*args, **kwargs)
    return wrap


def on_message(ws, message):
    global queueId
    jsonData = json.loads(message)
    for key in jsonData:
        if key == "insert":
            if "queue" in jsonData["insert"]:
                for queue in jsonData["insert"]["queue"]:
                    if (jsonData["insert"]["queue"][queue]["type"] == "team") and (jsonData["insert"]["queue"][queue]["support_team_id"] == teamId):
                        queueId = queue
        elif key == "update":
            if "queue" in jsonData["update"]:
                for queue in jsonData["update"]["queue"]:
                    if (jsonData["update"]["queue"][queue]["type"] == "team") and (jsonData["update"]["queue"][queue]["support_team_id"] == teamId):
                        queueId = queue

        # currentQueueId = jsonData[]
    if jsonData["type"] == "model_update":
        if "update" in jsonData:
            print("\033[93m", end="")
            print("--------------------\n" +
                  str(json.dumps(jsonData, indent=4)) + "\n--------------------")
            onModelUpdate(ws, jsonData)
            print("\033[0m", end="")
        elif "insert" in jsonData:
            print("\033[92m", end="")
            onModelInsert(ws, jsonData)
            print("\033[0m", end="")
        elif "delete" in jsonData:
            print("\033[91m", end="")
            onModelDelete(ws, jsonData)
            print("\033[0m", end="")
    else:
        print("\033[96m", end="")
        print("--------------------\n" +
              str(json.dumps(jsonData, indent=4)) + "\n--------------------")
        print("\033[0m", end="")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


@updateBearerToken
def on_open(ws):
    auth = (
        """{"type" : "authenticate","credentials" :{"bearer_token" : \"""" + bearerToken + """\"}}\n""")
    ws.send(auth)
    ws.send(
        """{"type" : "subscribe","tables" : ["support_session", "queue"]}\n""")
    print("Opened connection")


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://bomgar-app.tamu.edu/nw",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                subprotocols=["ingredi state api"])

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
