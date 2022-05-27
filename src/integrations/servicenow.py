from os import environ as env
import requests


def getServiceNowData(filter):
    """Get data from ServiceNow
    
    Args:
        filter (str): The filter to use in the ServiceNow query

    Returns:
        dict: The data from ServiceNow
    """
    output = requests.get(filter, auth=(env["SERVICENOW_USERNAME"], env["SERVICENOW_PASSWORD"])).json()["result"]
    if output == []:
        return 0
    else:
        return output["stats"]["count"]

filters = {
    "onHold16Hours": "https://tamu.service-now.com/api/now/table/incident?sysparm_query=active=true^state=on_hold^state_duration=16^ORDERBYDESCsys_updated_on",
    "activeIncidents": lambda i, j: "https://tamu.service-now.com/api/now/table/incident?sysparm_query=active=true^state=active^state_duration={}^state_duration={}^ORDERBYDESCsys_updated_on".format(i, j)
}


# print((getServiceNowData(filters().onHold16Hours)))
# print((getServiceNowData(filters().active(0, 2))))