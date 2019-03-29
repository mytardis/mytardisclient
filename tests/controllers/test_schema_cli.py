"""
test_schema_cli.py

Tests for querying the MyTardis REST API's schema endpoints
via the command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.schema import SchemaController


def test_schema_list_cli_json(capfd):
    """
    Test listing schemas, requesting output in JSON format
    """
    mock_schema_list = {
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
                "hidden": True,
                "immutable": True,
                "name": "Schema Name",
                "namespace": "http://schema/namespace/1",
                "resource_uri": "/api/v1/schema/1/",
                "subtype": None,
                "type": 1
            }
        ]
    }
    mock_schema_list_response = json.dumps(mock_schema_list)
    with requests_mock.Mocker() as mocker:
        schema_list_url = "%s/api/v1/schema/?format=json" % config.url
        mocker.get(schema_list_url, text=mock_schema_list_response)
        schema_controller = SchemaController()
        args = Namespace(
            model='schema', command='list', json=True, verbose=False,
            limit=None, offset=None, order_by=None)

        schema_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_schema_list

        schema_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_schema_list

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'schema', 'list', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_schema_list
        sys.argv = sys_argv


def test_schema_list_cli_table(capfd):
    """
    Test listing schema records, requesting output in ASCII table format
    """
    mock_schema_list = {
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
                "hidden": True,
                "immutable": True,
                "name": "Schema Name",
                "namespace": "http://schema/namespace/1",
                "resource_uri": "/api/v1/schema/1/",
                "subtype": None,
                "type": 1
            }
        ]
    }
    mock_schema_list_response = json.dumps(mock_schema_list)
    expected = textwrap.dedent("""
        Model: Schema
        Query: %s/api/v1/schema/?format=json
        Total Count: 1
        Limit: 20
        Offset: 0

        +----+-------------+---------------------------+-------------------+---------+-----------+--------+
        | ID |    Name     |         Namespace         |       Type        | Subtype | Immutable | Hidden |
        +====+=============+===========================+===================+=========+===========+========+
        |  1 | Schema Name | http://schema/namespace/1 | Experiment schema |         | True      | True   |
        +----+-------------+---------------------------+-------------------+---------+-----------+--------+
    """) % config.url
    with requests_mock.Mocker() as mocker:
        schema_list_url = "%s/api/v1/schema/?format=json" % config.url
        mocker.get(schema_list_url, text=mock_schema_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'schema', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_schema_get_cli_json(capfd):
    """
    Test looking up and displaying a schema via the command-line interface
    """
    mock_schema = {
        "id": 1,
        "hidden": True,
        "immutable": True,
        "name": "Schema Name",
        "namespace": "http://schema/namespace/1",
        "resource_uri": "/api/v1/schema/1/",
        "subtype": None,
        "type": 1
    }
    mock_schema_get_response = json.dumps(mock_schema)
    with requests_mock.Mocker() as mocker:
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_schema_get_response)
        schema_controller = SchemaController()
        args = Namespace(
            model='schema', command='get', schema_id=1, params=False,
            json=True, verbose=False)
        schema_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_schema


def test_schema_get_cli_table(capfd):
    """
    Test getting schema record via the command-line interface,
    requesting output in ASCII table format
    """
    mock_schema = {
        "id": 1,
        "hidden": True,
        "immutable": True,
        "name": "Schema Name",
        "namespace": "http://schema/namespace/1",
        "resource_uri": "/api/v1/schema/1/",
        "subtype": None,
        "type": 1
    }
    mock_schema_get_response = json.dumps(mock_schema)
    mock_pname_list = {
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
                "name": "param-name1",
                "full_name": "Parameter Name1",
                "choices": "",
                "comparison_type": 8,
                "data_type": 7,
                "immutable": False,
                "is_searchable": False,
                "order": 1,
                "resource_uri": "/api/v1/parametername/1/",
                "schema": "/api/v1/schema/1/",
                "units": ""
            }
        ]
    }
    mock_pnames_response = json.dumps(mock_pname_list)
    expected = textwrap.dedent("""
        +--------------+---------------------------+
        | Schema field |           Value           |
        +==============+===========================+
        | ID           | 1                         |
        +--------------+---------------------------+
        | Name         | Schema Name               |
        +--------------+---------------------------+
        | Namespace    | http://schema/namespace/1 |
        +--------------+---------------------------+
        | Type         | Experiment schema         |
        +--------------+---------------------------+
        | Subtype      | None                      |
        +--------------+---------------------------+
        | Immutable    | True                      |
        +--------------+---------------------------+
        | Hidden       | True                      |
        +--------------+---------------------------+

        +------------------+-----------------+-------------+-------------+-------+-----------+---------------+-------+---------+-----------------+
        | ParameterName ID |    Full Name    |    Name     |  Data Type  | Units | Immutable | Is Searchable | Order | Choices | Comparison Type |
        +==================+=================+=============+=============+=======+===========+===============+=======+=========+=================+
        |                1 | Parameter Name1 | param-name1 | Long String |       | False     | False         | 1     |         | Contains        |
        +------------------+-----------------+-------------+-------------+-------+-----------+---------------+-------+---------+-----------------+
    """)
    with requests_mock.Mocker() as mocker:
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_schema_get_response)
        pnames_url = "%s/api/v1/parametername/?format=json&schema__id=1" % config.url
        mocker.get(pnames_url, text=mock_pnames_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'schema', 'get', '1', '--params']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
