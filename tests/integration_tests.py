import pytest

class TestClass:
    def test_returnTypes(self):
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
