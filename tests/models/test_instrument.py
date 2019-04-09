"""
test_instrument.py

Tests for functionality to query the Instrument model via
the MyTardis REST API's instrument resource
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.instrument import Instrument


def test_instrument_list():
    """
    Test listing instrument records exposed in a MyTardis REST API
    """
    mock_instrument_list = {
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
                "facility": {
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
                },
                "id": 1,
                "modified_time": None,
                "name": "Test Instrument",
                "resource_uri": "/api/v1/instrument/1/"
            }
        ]
    }
    mock_list_response = json.dumps(mock_instrument_list)
    with requests_mock.Mocker() as mocker:
        list_instruments_url = "%s/api/v1/instrument/?format=json&facility__id=1" % config.url
        mocker.get(list_instruments_url, text=mock_list_response)
        instruments = Instrument.list(filters="facility__id=1")
        assert instruments.response_dict == mock_instrument_list


def test_instrument_get():
    """
    Test getting a instrument record by ID
    """
    mock_instrument = {
        "created_time": None,
        "facility": {
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
        },
        "id": 1,
        "modified_time": None,
        "name": "Test Instrument",
        "resource_uri": "/api/v1/instrument/1/"
    }
    mock_get_response = json.dumps(mock_instrument)
    with requests_mock.Mocker() as mocker:
        get_instrument_url = "%s/api/v1/instrument/1/?format=json" % config.url
        mocker.get(get_instrument_url, text=mock_get_response)
        instrument = Instrument.objects.get(id=1)
        assert instrument.response_dict == mock_instrument
