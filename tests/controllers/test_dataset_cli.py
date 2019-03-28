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
        Query: %s/api/v1/dataset/?format=json
        Total Count: 1
        Limit: 20
        Offset: 0
        
        +------------+-----------------------+---------------------+------------+
        | Dataset ID |     Experiment(s)     |     Description     | Instrument |
        +============+=======================+=====================+============+
        |          1 | /api/v1/experiment/1/ | dataset description | None       |
        +------------+-----------------------+---------------------+------------+
    """) % config.url
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
            verbose=False, metadata=False)
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
        "parameter_sets": [
            {
                "id": 1,
                "dataset": "/api/v1/dataset/1/",
                "schema": {
                    "id": 1,
                    "name": "Series Metadata",
                    "namespace": "http://schema/namespace",
                    "hidden": False,
                    "immutable": True,
                    "subtype": "",
                    "type": 1
                },
                "parameters": [
                    {
                        "id": 1,
                        "name": "/api/v1/parametername/1/",
                        "parameterset": "/api/v1/datasetparameterset/1/",
                        "resource_uri": "/api/v1/datasetparameter/1/",
                        "string_value": "param value",
                        "numerical_value": None,
                        "datetime_value": None,
                        "link_id": None,
                        "value": None
                    }
                ]
            }
        ],
        "resource_uri": "/api/v1/dataset/1/"
    }
    mock_dataset_get_response = json.dumps(mock_dataset)
    mock_schema = {
        "hidden": False,
        "id": 1,
        "immutable": True,
        "name": "Schema Name",
        "namespace": "http://schema/namespace",
        "resource_uri": "/api/v1/schema/1/",
        "subtype": "",
        "type": 1
    }
    mock_schema_response = json.dumps(mock_schema)
    mock_pname = {
        "id": 1,
        "choices": "",
        "comparison_type": 1,
        "data_type": 2,
        "full_name": "Parameter Name",
        "immutable": True,
        "is_searchable": False,
        "name": "param name",
        "order": 1,
        "resource_uri": "/api/v1/parametername/1/",
        "schema": "/api/v1/schema/1/",
        "units": ""
    }
    mock_pname_response = json.dumps(mock_pname)
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

        +---------------------+-------------+----------------+--------------+-----------------+----------------+---------+
        | DatasetParameter ID |   Schema    | Parameter Name | String Value | Numerical Value | Datetime Value | Link ID |
        +=====================+=============+================+==============+=================+================+=========+
        |                   1 | Schema Name | param name     | param value  |                 |                |         |
        +---------------------+-------------+----------------+--------------+-----------------+----------------+---------+
    """)
    with requests_mock.Mocker() as mocker:
        get_dataset_url = "%s/api/v1/dataset/1/?format=json" % config.url
        mocker.get(get_dataset_url, text=mock_dataset_get_response)
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_schema_response)
        get_pname_url = "%s/api/v1/parametername/1/?format=json" % config.url
        mocker.get(get_pname_url, text=mock_pname_response)
        df_list_url = "%s/api/v1/dataset_file/?format=json&dataset__id=1" % config.url
        mocker.get(df_list_url, text=mock_df_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'dataset', 'get', '1', '--metadata']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
