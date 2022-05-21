from dataclasses import replace
import requests
import datetime
from os import environ as env

defaultStations = ["Student Leader", "Counter", "Email", "Info Desk", "Phones", "Tier 2"]


def getStationUrl(stationName: str):
    """Get the REST API URL for a station at the current time

    Args:
                    stationName (str): The name of the station in ScheduleSource

    Returns:
                    str: the REST API URL
    """
    # Get 12:30 AM today
    currentTime = datetime.datetime.now()
    returnUrl = "https://www.schedulesource.net/Enterprise/teamwork/services/genericio.aspx?token={}&entitytype=ScheduleShift&Fields=LastName,FirstName&MaxDate={}&StationName={}&ShiftStart={{<=}}1900-01-{}T{}&ShiftEnd={{>=}}1900-01-{}T{}".format(
        env["SCHEDULESOURCE_TOKEN"],
        currentTime.strftime("%m/%d/%Y"),
        stationName,
        "02" if currentTime.hour < 1 else "01",
        currentTime.strftime("%H:%M:%S"),
        "02" if currentTime.hour < 1 else "01",
        currentTime.strftime("%H:%M:%S")
    ) #.replace("-", "%2D"),replace(" ", "%20")
    # print(returnUrl)
    return returnUrl


def getListOfEmployees(stations: list[str] = defaultStations):
    """Get a list of employees at the current time

        Args:
                stations (list[str], optional): The list of stations to get employees from. Defaults to defaultStations.

        Returns:
                list[dict]: A list of employees at the current time
    """
    employees = []
    for station in stations:
        jsonData = requests.get(getStationUrl(station)).json()
        for employeeIndex in range(len(jsonData)):
            jsonData[employeeIndex]["station"] = station
        employees.extend(jsonData)
    return employees

for employee in getListOfEmployees():
	print(employee["LastName"] + ", " + employee["FirstName"] + " - " + employee["station"])
