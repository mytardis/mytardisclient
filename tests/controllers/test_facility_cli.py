"""
test_facility_cli.py

Tests for querying the MyTardis REST API's facility endpoints
via the command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.facility import FacilityController

config.url = "https://mytardis-test.example.com"


def test_facility_list_cli_json(capfd):
    """
    Test listing facilities, requesting output in JSON format
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
                "id": 1,
                "manager_group": {
                    "id": 1,
                    "name": "test-facility-managers",
                    "resource_uri": "/api/v1/group/1/"
                },
                "name": "Test Facility",
                "resource_uri": "/api/v1/facility/1/"
            }
        ]
    }
    mock_facility_list_response = json.dumps(mock_facility_list)
    with requests_mock.Mocker() as mocker:
        facility_list_url = "%s/api/v1/facility/?format=json" % config.url
        mocker.get(facility_list_url, text=mock_facility_list_response)
        facility_controller = FacilityController()
        args = Namespace(
            model='facility', command='list', json=True, verbose=False,
            limit=None, offset=None, order_by=None)

        facility_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_facility_list

        facility_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_facility_list

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'facility', 'list', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_facility_list
        sys.argv = sys_argv


def test_facility_list_cli_table(capfd):
    """
    Test listing facility records, requesting output in ASCII table format
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
                "id": 1,
                "manager_group": {
                    "id": 1,
                    "name": "test-facility-managers",
                    "resource_uri": "/api/v1/group/1/"
                },
                "name": "Test Facility",
                "resource_uri": "/api/v1/facility/1/"
            }
        ]
    }
    mock_facility_list_response = json.dumps(mock_facility_list)
    expected = textwrap.dedent("""
        Model: Facility
        Query: https://mytardis-test.example.com/api/v1/facility/?format=json
        Total Count: 1
        Limit: 20
        Offset: 0

        +----+---------------+------------------------+
        | ID |     Name      |     Manager Group      |
        +====+===============+========================+
        |  1 | Test Facility | test-facility-managers |
        +----+---------------+------------------------+
    """)
    with requests_mock.Mocker() as mocker:
        facility_list_url = "%s/api/v1/facility/?format=json" % config.url
        mocker.get(facility_list_url, text=mock_facility_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'facility', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_facility_get_cli_json(capfd):
    """
    Test looking up and displaying a facility via the command-line interface
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
    with requests_mock.Mocker() as mocker:
        get_facility_url = "%s/api/v1/facility/1/?format=json" % config.url
        mocker.get(get_facility_url, text=mock_facility_get_response)
        facility_controller = FacilityController()
        args = Namespace(
            model='facility', command='get', facility_id=1, json=True,
            verbose=False)
        facility_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_facility


def test_facility_get_cli_table(capfd):
    """
    Test getting facility record via the command-line interface,
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
    mock_instruments_response = json.dumps(mock_instrument_list)
    expected = textwrap.dedent("""
        Model: Facility

        +----------------+------------------------+
        | Facility field |         Value          |
        +================+========================+
        | ID             | 1                      |
        +----------------+------------------------+
        | Name           | Test Facility          |
        +----------------+------------------------+
        | Manager Group  | test-facility-managers |
        +----------------+------------------------+


        Model: Instrument
        Query: https://mytardis-test.example.com/api/v1/instrument/?format=json&facility__id=1
        Total Count: 1
        Limit: 20
        Offset: 0

        +----+-----------------+---------------------------+
        | ID |      Name       |         Facility          |
        +====+=================+===========================+
        |  1 | Test Instrument | <Facility: Test Facility> |
        +----+-----------------+---------------------------+
    """)
    with requests_mock.Mocker() as mocker:
        get_facility_url = "%s/api/v1/facility/1/?format=json" % config.url
        mocker.get(get_facility_url, text=mock_facility_get_response)
        instruments_url = "%s/api/v1/instrument/?format=json&facility__id=1" % config.url
        mocker.get(instruments_url, text=mock_instruments_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'facility', 'get', '1']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
