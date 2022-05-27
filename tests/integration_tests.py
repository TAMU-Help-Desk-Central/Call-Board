import pytest

class TestClass:
    def test_returnTypes_schedulesource(self):
        from src.integrations import schedulesource
        assert isinstance(schedulesource.getListOfEmployees(), (type(None), list))
        for each in schedulesource.getListOfEmployees():
            assert isinstance(each, dict)
            assert "LastName" in each
            assert "FirstName" in each
            assert "station" in each
            assert isinstance(each["LastName"], str)
            assert isinstance(each["FirstName"], str)
            assert isinstance(each["station"], str)
    def test_returnTypes_servicenow(self):
        from src.integrations import servicenow
        onHold = servicenow.getServiceNowData(servicenow.filters["onHold16Hours"])
        assert isinstance(onHold, int)
        assert onHold >= 0
        minHours = 0
        maxHours = 6
        for i in range(minHours, maxHours-1):
            for j in range(i+1, maxHours):
                print(i, j)
                num = servicenow.getServiceNowData(servicenow.filters["activeIncidents"](i,j))
                assert isinstance(num, int)
                # assert greater than or equal to 0
                assert num >= 0
        