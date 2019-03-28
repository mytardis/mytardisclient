"""
test_datafile_cli.py

Tests for querying the MyTardis REST API's datafile endpoints
via the command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.datafile import DataFileController

config.url = "https://mytardis-test.example.com"


def test_datafile_list_cli_json(capfd):
    """
    Test listing datafiles, requesting output in JSON format
    """
    mock_datafile_list = {
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
                "created_time": "2016-11-10T13:50:25.258483",
                "dataset": "/api/v1/dataset/1/",
                "directory": "",
                "filename": "testfile1.txt",
                "md5sum": "bogus",
                "mimetype": "text/plain",
                "modification_time": None,
                "parameter_sets": [
                ],
                "replicas": [
                    {
                        "datafile": "/api/v1/dataset_file/1/",
                        "id": 1,
                        "location": "local box at /home/mytardis/var/local",
                        "resource_uri": "/api/v1/replica/1/",
                        "uri": "subdir/testfile1.txt",
                        "verified": True
                    }
                ],
                "resource_uri": "/api/v1/dataset_file/1/",
                "size": 32
            }
        ]
    }
    mock_df_list_response = json.dumps(mock_datafile_list)
    with requests_mock.Mocker() as mocker:
        datafile_list_url = "%s/api/v1/dataset_file/?format=json&dataset__id=1" % config.url
        mocker.get(datafile_list_url, text=mock_df_list_response)
        df_controller = DataFileController()
        args = Namespace(
            model='datafile', command='list', dataset='1',
            directory=None, filename=None,
            json=True, verbose=False,
            filter=None, limit=None, offset=None, order_by=None)

        df_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_datafile_list

        df_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_datafile_list

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'datafile', 'list', '--dataset', '1', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_datafile_list
        sys.argv = sys_argv


def test_datafile_list_cli_table(capfd):
    """
    Test listing datafile records, requesting output in ASCII table format
    """
    mock_datafile_list = {
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
                "created_time": "2016-11-10T13:50:25.258483",
                "dataset": "/api/v1/dataset/1/",
                "directory": "",
                "filename": "testfile1.txt",
                "md5sum": "bogus",
                "mimetype": "text/plain",
                "modification_time": None,
                "parameter_sets": [
                ],
                "replicas": [
                    {
                        "datafile": "/api/v1/dataset_file/1/",
                        "id": 1,
                        "location": "local box at /home/mytardis/var/local",
                        "resource_uri": "/api/v1/replica/1/",
                        "uri": "subdir/testfile1.txt",
                        "verified": True
                    }
                ],
                "resource_uri": "/api/v1/dataset_file/1/",
                "size": 32
            }
        ]
    }
    mock_df_list_response = json.dumps(mock_datafile_list)
    expected = textwrap.dedent("""
        Model: DataFile
        Query: https://mytardis-test.example.com/api/v1/dataset_file/?format=json
        Total Count: 1
        Limit: 20
        Offset: 0

        +-------------+---------------+---------------------------------------+----------------------+----------+-----------+---------+
        | DataFile ID |   Filename    |              Storage Box              |         URI          | Verified |   Size    | MD5 Sum |
        +=============+===============+=======================================+======================+==========+===========+=========+
        |           1 | testfile1.txt | local box at /home/mytardis/var/local | subdir/testfile1.txt | True     |  32 bytes | bogus   |
        +-------------+---------------+---------------------------------------+----------------------+----------+-----------+---------+
    """)
    with requests_mock.Mocker() as mocker:
        datafile_list_url = "%s/api/v1/dataset_file/?format=json" % config.url
        mocker.get(datafile_list_url, text=mock_df_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'datafile', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_datafile_get_cli_json(capfd):
    """
    Test looking up and displaying an datafile via the command-line interface
    """
    mock_datafile = {
        "id": 1,
        "created_time": "2016-11-10T13:50:25.258483",
        "dataset": "/api/v1/dataset/1/",
        "directory": "",
        "filename": "testfile1.txt",
        "md5sum": "bogus",
        "mimetype": "text/plain",
        "modification_time": None,
        "parameter_sets": [
        ],
        "replicas": [
            {
                "datafile": "/api/v1/dataset_file/1/",
                "id": 1,
                "location": "local box at /home/mytardis/var/local",
                "resource_uri": "/api/v1/replica/1/",
                "uri": "subdir/testfile1.txt",
                "verified": True
            }
        ],
        "resource_uri": "/api/v1/dataset_file/1/",
        "size": 32
    }
    mock_datafile_get_response = json.dumps(mock_datafile)
    with requests_mock.Mocker() as mocker:
        get_datafile_url = "%s/api/v1/dataset_file/1/?format=json" % config.url
        mocker.get(get_datafile_url, text=mock_datafile_get_response)
        df_controller = DataFileController()
        args = Namespace(
            model='datafile', command='get', datafile_id=1, json=True,
            metadata=False, verbose=False)
        df_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_datafile


def test_datafile_get_cli_table(capfd):
    """
    Test getting datafile record via the command-line interface,
    requesting output in ASCII table format
    """
    mock_datafile = {
        "id": 1,
        "created_time": "2016-11-10T13:50:25.258483",
        "dataset": "/api/v1/dataset/1/",
        "directory": "",
        "filename": "testfile1.txt",
        "md5sum": "bogus",
        "mimetype": "text/plain",
        "modification_time": None,
        "parameter_sets": [
            {
                "id": 1,
                "datafile": "/api/v1/dataset_file/1/",
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
                        "parameterset": "/api/v1/datafileparameterset/1/",
                        "resource_uri": "/api/v1/datafileparameter/1/",
                        "string_value": "param value",
                        "numerical_value": None,
                        "datetime_value": None,
                        "link_id": None,
                        "value": None
                    }
                ]
            }
        ],
        "replicas": [
            {
                "datafile": "/api/v1/dataset_file/1/",
                "id": 1,
                "location": "local box at /home/mytardis/var/local",
                "resource_uri": "/api/v1/replica/1/",
                "uri": "subdir/testfile1.txt",
                "verified": True
            }
        ],
        "resource_uri": "/api/v1/dataset_file/1/",
        "size": 32
    }
    mock_datafile_get_response = json.dumps(mock_datafile)
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
    expected = textwrap.dedent("""
        +----------------+---------------------------------------+
        | DataFile field |                 Value                 |
        +================+=======================================+
        | ID             | 1                                     |
        +----------------+---------------------------------------+
        | Dataset        | /api/v1/dataset/1/                    |
        +----------------+---------------------------------------+
        | Storage Box    | local box at /home/mytardis/var/local |
        +----------------+---------------------------------------+
        | Directory      |                                       |
        +----------------+---------------------------------------+
        | Filename       | testfile1.txt                         |
        +----------------+---------------------------------------+
        | URI            | subdir/testfile1.txt                  |
        +----------------+---------------------------------------+
        | Verified       | True                                  |
        +----------------+---------------------------------------+
        | Size           |  32 bytes                             |
        +----------------+---------------------------------------+
        | MD5 Sum        | bogus                                 |
        +----------------+---------------------------------------+

        +----------------------+-------------+----------------+--------------+-----------------+----------------+---------+
        | DataFileParameter ID |   Schema    | Parameter Name | String Value | Numerical Value | Datetime Value | Link ID |
        +======================+=============+================+==============+=================+================+=========+
        |                    1 | Schema Name | param name     | param value  |                 |                |         |
        +----------------------+-------------+----------------+--------------+-----------------+----------------+---------+
    """)
    with requests_mock.Mocker() as mocker:
        get_datafile_url = "%s/api/v1/dataset_file/1/?format=json" % config.url
        mocker.get(get_datafile_url, text=mock_datafile_get_response)
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_schema_response)
        get_pname_url = "%s/api/v1/parametername/1/?format=json" % config.url
        mocker.get(get_pname_url, text=mock_pname_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'datafile', 'get', '1', '--metadata']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
