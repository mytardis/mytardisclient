"""
test_api_cli.py

Tests for querying the REST API, listing its endpoints and describing each
endpoint's schema from a command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.api import ApiController

config.url = "https://mytardis-test.example.com"


def test_api_list_cli_json(capfd):
    """
    Test listing API endpoints, requesting output in JSON format
    """
    mock_api_endpoints = {
        "dataset": {
            "list_endpoint": "/api/v1/dataset/",
            "schema": "/api/v1/dataset/schema/"
        },
        "dataset_file": {
            "list_endpoint": "/api/v1/dataset_file/",
            "schema": "/api/v1/dataset_file/schema/"
        },
        "experiment": {
            "list_endpoint": "/api/v1/experiment/",
            "schema": "/api/v1/experiment/schema/"
        }
    }
    mock_api_list_response = json.dumps(mock_api_endpoints)
    with requests_mock.Mocker() as mocker:
        list_api_endpoints_url = "%s/api/v1/?format=json" % config.url
        mocker.get(list_api_endpoints_url, text=mock_api_list_response)
        api_controller = ApiController()
        args = Namespace(model='api', command='list', json=True, verbose=False)

        api_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_api_endpoints

        api_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_api_endpoints

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'api', 'list', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_api_endpoints
        sys.argv = sys_argv


def test_api_list_cli_table(capfd):
    """
    Test listing API endpoints, requesting output in ASCII table format
    """
    mock_api_endpoints = {
        "dataset": {
            "list_endpoint": "/api/v1/dataset/",
            "schema": "/api/v1/dataset/schema/"
        },
        "dataset_file": {
            "list_endpoint": "/api/v1/dataset_file/",
            "schema": "/api/v1/dataset_file/schema/"
        },
        "experiment": {
            "list_endpoint": "/api/v1/experiment/",
            "schema": "/api/v1/experiment/schema/"
        }
    }
    mock_api_list_response = json.dumps(mock_api_endpoints)
    expected = textwrap.dedent("""
        API Endpoints
        +--------------+-----------------------+------------------------------+
        |    Model     |     List Endpoint     |            Schema            |
        +==============+=======================+==============================+
        | dataset      | /api/v1/dataset/      | /api/v1/dataset/schema/      |
        +--------------+-----------------------+------------------------------+
        | dataset_file | /api/v1/dataset_file/ | /api/v1/dataset_file/schema/ |
        +--------------+-----------------------+------------------------------+
        | experiment   | /api/v1/experiment/   | /api/v1/experiment/schema/   |
        +--------------+-----------------------+------------------------------+
    """)
    with requests_mock.Mocker() as mocker:
        list_api_endpoints_url = "%s/api/v1/?format=json" % config.url
        mocker.get(list_api_endpoints_url, text=mock_api_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'api', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_api_get_cli_json(capfd):
    """
    Test getting API endpoint schema via the command-line interface
    """
    mock_api_schema = {
        "allowed_detail_http_methods": [
            "get",
            "post"
        ],
        "allowed_list_http_methods": [
            "get",
            "post"
        ],
        "default_format": "application/json",
        "default_limit": 20,
        "fields": {
            "description": {
                "blank": True,
                "default": "",
                "nullable": False,
                "primary_key": False,
                "readonly": False,
                "type": "string",
                "unique": False,
                "verbose_name": "description"
            }
        },
        "filtering": {
            "description": [
                "exact"
            ]
        },
        "ordering": [
            "description"
        ]
    }
    mock_api_get_response = json.dumps(mock_api_schema)
    with requests_mock.Mocker() as mocker:
        get_api_schema_url = "%s/api/v1/dataset/schema/?format=json" % config.url
        mocker.get(get_api_schema_url, text=mock_api_get_response)
        api_controller = ApiController()
        args = Namespace(
            model='api', api_model='dataset', command='get', json=True,
            verbose=False)
        api_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_api_schema


def test_api_get_cli_table(capfd):
    """
    Test getting API endpoint schema via the command-line interface,
    requesting output in ASCII table format
    """
    mock_api_schema = {
        "allowed_detail_http_methods": [
            "get",
            "post"
        ],
        "allowed_list_http_methods": [
            "get",
            "post"
        ],
        "default_format": "application/json",
        "default_limit": 20,
        "fields": {
            "description": {
                "blank": True,
                "default": "",
                "nullable": False,
                "primary_key": False,
                "readonly": False,
                "type": "string",
                "unique": False,
                "verbose_name": "description"
            }
        },
        "filtering": {
            "description": [
                "exact"
            ]
        },
        "ordering": [
            "description"
        ]
    }
    mock_api_get_response = json.dumps(mock_api_schema)
    expected = textwrap.dedent("""
        +------------------+--------------------+
        | API Schema field |       Value        |
        +==================+====================+
        | Model            | dataset            |
        +------------------+--------------------+
        | Fields           | description        |
        +------------------+--------------------+
        | Filtering        | {                  |
        |                  |   "description": [ |
        |                  |     "exact"        |
        |                  |   ]                |
        |                  | }                  |
        +------------------+--------------------+
        | Ordering         | [                  |
        |                  |   "description"    |
        |                  | ]                  |
        +------------------+--------------------+
    """)
    with requests_mock.Mocker() as mocker:
        get_api_schema_url = "%s/api/v1/dataset/schema/?format=json" % config.url
        mocker.get(get_api_schema_url, text=mock_api_get_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'api', 'get', 'dataset']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
