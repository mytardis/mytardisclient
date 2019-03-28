"""
test_render_instrument.py

Tests for rendering a view of an instrument record
"""
import json
import textwrap

import requests_mock

from mtclient.conf import config
from mtclient.models.instrument import Instrument
from mtclient.views import render

config.url = "https://mytardis-test.example.com"


def test_render_instrument():
    """
    Test rendering a view of an instrument record
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

        instrument = Instrument.objects.get(id=1)

        assert render(instrument).strip() == expected.strip()
