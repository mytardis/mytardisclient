"""
test_dataset_cli.py

Tests for querying the MyTardis REST API's dataset endpoints
via the command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.dataset import DatasetController

config.url = "https://mytardis-test.example.com"


def test_dataset_list_cli_json(capfd):
    """
    Test listing datasets, requesting output in JSON format
    """
    mock_dataset_list = {
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
                "description": "dataset description",
                "experiments": [
                    "/api/v1/experiment/1/"
                ],
                "immutable": False,
                "instrument": None,
                "parameter_sets": [],
                "resource_uri": "/api/v1/dataset/1/"
            }
        ]
    }
    mock_ds_list_response = json.dumps(mock_dataset_list)
    with requests_mock.Mocker() as mocker:
        dataset_list_url = "%s/api/v1/dataset/?format=json&experiments__id=1" % config.url
        mocker.get(dataset_list_url, text=mock_ds_list_response)
        ds_controller = DatasetController()
        args = Namespace(
            model='dataset', command='list', exp='1', json=True, verbose=False,
            filter=None, limit=None, offset=None, order_by=None)

        ds_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_dataset_list

        ds_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_dataset_list

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'dataset', 'list', '--exp', '1', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_dataset_list
        sys.argv = sys_argv


def test_dataset_list_cli_table(capfd):
    """
    Test listing dataset records, requesting output in ASCII table format
    """
    mock_dataset_list = {
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
                "description": "dataset description",
                "experiments": [
                    "/api/v1/experiment/1/"
                ],
                "immutable": False,
                "instrument": None,
                "parameter_sets": [],
                "resource_uri": "/api/v1/dataset/1/"
            }
        ]
    }
    mock_ds_list_response = json.dumps(mock_dataset_list)
    expected = textwrap.dedent("""
        Model: Dataset
        Query: https://mytardis-test.example.com/api/v1/dataset/?format=json
        Total Count: 1
        Limit: 20
        Offset: 0
        
        +------------+-----------------------+---------------------+------------+
        | Dataset ID |     Experiment(s)     |     Description     | Instrument |
        +============+=======================+=====================+============+
        |          1 | /api/v1/experiment/1/ | dataset description | None       |
        +------------+-----------------------+---------------------+------------+
    """)
    with requests_mock.Mocker() as mocker:
        dataset_list_url = "%s/api/v1/dataset/?format=json" % config.url
        mocker.get(dataset_list_url, text=mock_ds_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'dataset', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_dataset_get_cli_json(capfd):
    """
    Test looking up and displaying an dataset via the command-line interface
    """
    mock_dataset = {
        "id": 1,
        "description": "dataset description",
        "experiments": [
            "/api/v1/experiment/1/"
        ],
        "immutable": False,
        "instrument": None,
        "parameter_sets": [],
        "resource_uri": "/api/v1/dataset/1/"
    }
    mock_dataset_get_response = json.dumps(mock_dataset)
    with requests_mock.Mocker() as mocker:
        get_dataset_url = "%s/api/v1/dataset/1/?format=json" % config.url
        mocker.get(get_dataset_url, text=mock_dataset_get_response)
        ds_controller = DatasetController()
        args = Namespace(
            model='dataset', command='get', dataset_id=1, json=True,
            verbose=False)
        ds_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_dataset


def test_dataset_get_cli_table(capfd):
    """
    Test getting dataset record via the command-line interface,
    requesting output in ASCII table format
    """
    mock_dataset = {
        "id": 1,
        "description": "dataset description",
        "experiments": [
            "/api/v1/experiment/1/"
        ],
        "immutable": False,
        "instrument": None,
        "parameter_sets": [],
        "resource_uri": "/api/v1/dataset/1/"
    }
    mock_dataset_get_response = json.dumps(mock_dataset)
    mock_datafile_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 0
        },
        "objects": [
        ]
    }
    mock_df_list_response = json.dumps(mock_datafile_list)
    expected = textwrap.dedent("""
        +---------------+-----------------------+
        | Dataset field |         Value         |
        +===============+=======================+
        | ID            | 1                     |
        +---------------+-----------------------+
        | Experiment(s) | /api/v1/experiment/1/ |
        +---------------+-----------------------+
        | Description   | dataset description   |
        +---------------+-----------------------+
        | Instrument    | None                  |
        +---------------+-----------------------+
    """)
    with requests_mock.Mocker() as mocker:
        get_dataset_url = "%s/api/v1/dataset/1/?format=json" % config.url
        mocker.get(get_dataset_url, text=mock_dataset_get_response)
        df_list_url = "%s/api/v1/dataset_file/?format=json&dataset__id=1" % config.url
        mocker.get(df_list_url, text=mock_df_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'dataset', 'get', '1']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
