"""
test_facility.py

Tests for functionality to query the Facility model via
the MyTardis REST API's facility resource
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.facility import Facility

config.url = "https://mytardis-test.example.com"


def test_facility_list():
    """
    Test listing facility records exposed in a MyTardis REST API
    """
    mock_facility_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [
            {
                "created_time": None,
                "id": 1,
                "manager_group": {
                    "id": 1,
                    "name": "test-facility-managers",
                    "resource_uri": "/api/v1/group/1/"
                },
                "modified_time": None,
                "name": "Test Facility",
                "resource_uri": "/api/v1/facility/1/"
            }
        ]
    }
    mock_list_response = json.dumps(mock_facility_list)
    with requests_mock.Mocker() as mocker:
        list_facilities_url = "%s/api/v1/facility/?format=json" % config.url
        mocker.get(list_facilities_url, text=mock_list_response)
        facilities = Facility.objects.all()
        assert facilities.response_dict == mock_facility_list


def test_facility_get():
    """
    Test getting a facility record by ID
    """
    mock_facility = {
        "created_time": None,
        "id": 1,
        "manager_group": {
            "id": 1,
            "name": "test-facility-managers",
            "resource_uri": "/api/v1/group/1/"
        },
        "modified_time": None,
        "name": "Test Facility",
        "resource_uri": "/api/v1/facility/1/"
    }
    mock_get_response = json.dumps(mock_facility)
    with requests_mock.Mocker() as mocker:
        get_facility_url = "%s/api/v1/facility/1/?format=json" % config.url
        mocker.get(get_facility_url, text=mock_get_response)
        facility = Facility.objects.get(id=1)
        assert facility.response_dict == mock_facility
