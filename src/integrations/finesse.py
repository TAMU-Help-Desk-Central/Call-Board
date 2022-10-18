from datetime import datetime
import websocket
import rel
import json
import requests
import urllib3
from os import environ as env
import os
import re
from threading import Timer

queues = {"Phone": 0, "Software_Center": 0, "Technical_Support": 0}



class agent:
	def __init__(self, fullname, state, time):
		self.fullname = fullname
		self.state = state
		self.time = time

	def update(self, state, time):
		self.state = state
		self.time = time


agents = {}


class RepeatingTimer(object):
	"""
	USAGE:
	from time import sleep
	r = RepeatingTimer(_print, 0.5, "hello")
	r.start(); sleep(2); r.interval = 0.05; sleep(2); r.stop()
	"""

	def __init__(self, ws, keepAliveInterval, timeoutInterval):
		print("Initializing timer")
		super(RepeatingTimer, self).__init__()
		self.ws = ws
		self.keepAliveInterval = keepAliveInterval
		self.timeoutInterval = timeoutInterval
		self.timeoutTimer = None
		self.keepAliveTimer = None

	def restart(self):
		print("Restarting timer")
		self.timeoutTimer.cancel()
		self.timeoutTimer = Timer(self.timeoutInterval, self.closeConnection)
		self.timeoutTimer.start()

	def start(self):
		print("Starting timer")
		self.keepAliveTimer = Timer(self.keepAliveInterval, self.sendKeepAlive)
		self.keepAliveTimer.start()
		self.timeoutTimer = Timer(self.timeoutInterval, self.closeConnection)
		self.timeoutTimer.start()

	def stop(self):
		print("Stopping timer")
		Timer(self.keepAliveInterval, self.sendKeepAlive).cancel()
		Timer(self.timeoutInterval, self.closeConnection).cancel()

	def sendKeepAlive(self):
		print("Callback")
		self.ws.send("""2\n""")
		self.keepAliveTimer = Timer(self.keepAliveInterval, self.sendKeepAlive)
		self.keepAliveTimer.start()

	def closeConnection(self):
		print("Closing connection")
		self.ws.close()

def updateOutput():
	# clear screen
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Phone:", queues["Phone"])
	print("Software Center:", queues["Software_Center"])
	print("Technical Support:", queues["Technical_Support"])
	print("\nAgents:")
	for agent in agents:
		print(agents[agent].fullname)
		print(agents[agent].state)
		print(agents[agent].time)
		print("\n")

def on_message(ws, message):
	global keepAliveTimer
	global queues
	global agents
	# global queueId
	# print(message)
	if reTest := re.search(r"^(\d{1,2})($|\D)", message):
		match reTest.group(1):
			case "0":
				jsonData = json.loads(message[1:])
				print("Ping Interval:", jsonData["pingInterval"]/1000)
				print("Ping Timeout:", jsonData["pingTimeout"]/1000)
				keepAliveTimer = RepeatingTimer(
					ws, jsonData["pingInterval"]/1000, jsonData["pingTimeout"]/1000)
				keepAliveTimer.start()

				# global timeoutTimer
				# timeoutTimer = RepeatingTimer(timeoutWs, jsonData["pingTimeout"]/1000, ws)

			case "40":
				print("40")
			case "42":
				jsonData = json.loads(message[2:])
				match jsonData[0]:
					case 'subscribed':
						print("Subscribed")
					case 'message':
						if "VoiceIAQStats" in jsonData[1]:
							queues[jsonData[1]["id"]] = jsonData[1]["VoiceIAQStats"]["nWaitingContacts"]
							updateOutput()
						elif "ResourceIAQStats" in jsonData[1]:
							if jsonData[1]["id"] in agents:
								agents[jsonData[1]["id"]].update(
									jsonData[1]["ResourceIAQStats"]["strResourceState"], jsonData[1]["ResourceIAQStats"]["durationInStateMillis"]/1000)
							else:
								agents[jsonData[1]["id"]] = agent(
									jsonData[1]["ResourceIAQStats"]["resourceName"], jsonData[1]["ResourceIAQStats"]["strResourceState"], jsonData[1]["ResourceIAQStats"]["durationInStateMillis"]/1000)
			case "3":
				keepAliveTimer.restart()
				print("Restarted timeout timer")
			case _:
				print("default")
	else:
		print("Undefined message case")

	# jsonData = json.loads(message)


def on_error(ws, error):
	print(error)


def on_close(ws, close_status_code, close_msg):
	print("### closed ###")


# @updateBearerToken
def on_open(ws):
	# auth = (
	#     """{"type" : "authenticate","credentials" :{"bearer_token" : \"""" + bearerToken + """\"}}\n""")
	# ws.send(auth)
	ws.send(
		"""42["subscribe","VoiceIAQStats=Phone,Software_Center,Technical_Support"]\n""")
	ws.send(
		"""42["subscribe","ResourceIAQStats=carter.strickland"]\n""")
	print("Opened connection")


if __name__ == "__main__":
	requests.packages.urllib3.disable_warnings()
	requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
	try:
		requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
	except AttributeError:
		# no pyopenssl support used / needed / available
		pass
	websocket.enableTrace(False)
	authToken = requests.get("https://callcenter1.telecom.tamu.edu:9443/livedata/token/new", auth=(
		"uccxhruser", "c1148c11b120"), verify=False, params={"domain": "CCX"}).json()["token"]
	ws = websocket.WebSocketApp("wss://callcenter1.telecom.tamu.edu:12015/socket.io/?token={}&EIO=3&transport=websocket".format(authToken),
								on_open=on_open,
								on_message=on_message,
								on_error=on_error,
								on_close=on_close)

	ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
	rel.signal(2, rel.abort)  # Keyboard Interrupt
	rel.dispatch()
