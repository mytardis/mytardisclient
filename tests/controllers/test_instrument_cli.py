"""
test_facility_cli.py

Tests for querying the MyTardis REST API's facility endpoints
via the command-line interface
"""
import json
import sys
import textwrap

import requests_mock

import mtclient.client
from mtclient.conf import config

config.url = "https://mytardis-test.example.com"


def test_instrument_get_cli_table(capfd):
    """
    Test getting instrument record via the command-line interface,
    requesting output in ASCII table format
    """
    mock_facility = {
        "id": 1,
        "manager_group": {
            "id": 1,
            "name": "test-facility-managers",
            "resource_uri": "/api/v1/group/1/"
        },
        "name": "Test Facility",
        "resource_uri": "/api/v1/facility/1/"
    }
    mock_facility_get_response = json.dumps(mock_facility)
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
    mock_instrument_get_response = json.dumps(mock_instrument)
    expected = textwrap.dedent("""
        +------------------+---------------------------+
        | Instrument field |           Value           |
        +==================+===========================+
        | ID               | 1                         |
        +------------------+---------------------------+
        | Name             | Test Instrument           |
        +------------------+---------------------------+
        | Facility         | <Facility: Test Facility> |
        +------------------+---------------------------+
    """)
    with requests_mock.Mocker() as mocker:
        get_facility_url = "%s/api/v1/facility/1/?format=json" % config.url
        mocker.get(get_facility_url, text=mock_facility_get_response)
        get_instrument_url = "%s/api/v1/instrument/1/?format=json" % config.url
        mocker.get(get_instrument_url, text=mock_instrument_get_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'instrument', 'get', '1']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
