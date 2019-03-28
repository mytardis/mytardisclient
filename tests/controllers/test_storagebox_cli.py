"""
test_storagebox_cli.py

Tests for querying the MyTardis REST API's storage box endpoints
via the command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.storagebox import StorageBoxController

config.url = "https://mytardis-test.example.com"


def test_storagebox_list_cli_json(capfd):
    """
    Test listing storage boxes, requesting output in JSON format
    """
    mock_boxes_list = {
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
                "django_storage_class": "tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage",
                "name": "local box at /home/mytardis/var/local",
                "description": "Storage box description",
                "status": "online",
                "max_size": None,
                "attributes": [
                ],
                "options": [
                    {
                        "id": 1,
                        "key": "location",
                        "resource_uri": "/api/v1/storageboxoption/1/",
                        "storage_box": "/api/v1/storagebox/1/",
                        "value": "/home/mytardis/var/local",
                        "value_type": "string"
                    }
                ],
                "resource_uri": "/api/v1/storagebox/1/"
            }
        ]
    }
    mock_boxes_list_response = json.dumps(mock_boxes_list)
    with requests_mock.Mocker() as mocker:
        boxes_list_url = "%s/api/v1/storagebox/?format=json" % config.url
        mocker.get(boxes_list_url, text=mock_boxes_list_response)
        storagebox_controller = StorageBoxController()
        args = Namespace(
            model='storagebox', command='list', json=True, verbose=False,
            limit=None, offset=None, order_by=None)

        storagebox_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_boxes_list

        storagebox_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_boxes_list

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'storagebox', 'list', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_boxes_list
        sys.argv = sys_argv


def test_storagebox_list_cli_table(capfd):
    """
    Test listing storage box records, requesting output in ASCII table format
    """
    mock_boxes_list = {
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
                "django_storage_class": "tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage",
                "name": "local box at /home/mytardis/var/local",
                "description": "Storage box description",
                "status": "online",
                "max_size": None,
                "attributes": [
                ],
                "options": [
                    {
                        "id": 1,
                        "key": "location",
                        "resource_uri": "/api/v1/storageboxoption/1/",
                        "storage_box": "/api/v1/storagebox/1/",
                        "value": "/home/mytardis/var/local",
                        "value_type": "string"
                    }
                ],
                "resource_uri": "/api/v1/storagebox/1/",
            }
        ]
    }
    mock_boxes_list_response = json.dumps(mock_boxes_list)
    expected = textwrap.dedent("""
        Model: StorageBox
        Query: https://mytardis-test.example.com/api/v1/storagebox/?format=json
        Total Count: 1
        Limit: 20
        Offset: 0
              
        +----+---------------------------------------+-------------------------+
        | ID |                 Name                  |       Description       |
        +====+=======================================+=========================+
        |  1 | local box at /home/mytardis/var/local | Storage box description |
        +----+---------------------------------------+-------------------------+
    """)
    with requests_mock.Mocker() as mocker:
        boxes_list_url = "%s/api/v1/storagebox/?format=json" % config.url
        mocker.get(boxes_list_url, text=mock_boxes_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'storagebox', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_storagebox_get_cli_json(capfd):
    """
    Test looking up and displaying a storage box via the command-line interface
    """
    mock_storagebox = {
        "id": 1,
        "django_storage_class": "tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage",
        "name": "local box at /home/mytardis/var/local",
        "description": "Storage box description",
        "status": "online",
        "max_size": None,
        "attributes": [
        ],
        "options": [
            {
                "id": 1,
                "key": "location",
                "resource_uri": "/api/v1/storageboxoption/1/",
                "storage_box": "/api/v1/storagebox/1/",
                "value": "/home/mytardis/var/local",
                "value_type": "string"
            }
        ],
        "resource_uri": "/api/v1/storagebox/1/",
    }
    mock_storagebox_get_response = json.dumps(mock_storagebox)
    with requests_mock.Mocker() as mocker:
        get_storagebox_url = "%s/api/v1/storagebox/1/?format=json" % config.url
        mocker.get(get_storagebox_url, text=mock_storagebox_get_response)
        storagebox_controller = StorageBoxController()
        args = Namespace(
            model='storagebox', command='get', storage_box_id=1, params=False,
            json=True, verbose=False)
        storagebox_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_storagebox


def test_storagebox_get_cli_table(capfd):
    """
    Test getting storage box record via the command-line interface,
    requesting output in ASCII table format
    """
    mock_storagebox = {
        "id": 1,
        "django_storage_class": "tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage",
        "name": "local box at /home/mytardis/var/local",
        "description": "Storage box description",
        "status": "online",
        "max_size": None,
        "attributes": [
            {
                "id": 1,
                "key": "test_attr_key",
                "resource_uri": "/api/v1/storageboxattribute/1/",
                "storage_box": "/api/v1/storagebox/1/",
                "value": "test_attr_value",
                "value_type": "string"
            }
        ],
        "options": [
            {
                "id": 1,
                "key": "location",
                "resource_uri": "/api/v1/storageboxoption/1/",
                "storage_box": "/api/v1/storagebox/1/",
                "value": "/home/mytardis/var/local",
                "value_type": "string"
            }
        ],
        "resource_uri": "/api/v1/storagebox/1/",
    }
    mock_storagebox_get_response = json.dumps(mock_storagebox)
    expected = textwrap.dedent("""
        +----------------------+-------------------------------------------------------------+
        |   StorageBox field   |                            Value                            |
        +======================+=============================================================+
        | ID                   | 1                                                           |
        +----------------------+-------------------------------------------------------------+
        | Name                 | local box at /home/mytardis/var/local                       |
        +----------------------+-------------------------------------------------------------+
        | Description          | Storage box description                                     |
        +----------------------+-------------------------------------------------------------+
        | Django Storage Class | tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage |
        +----------------------+-------------------------------------------------------------+
        | Max Size             | None                                                        |
        +----------------------+-------------------------------------------------------------+
        | Status               | online                                                      |
        +----------------------+-------------------------------------------------------------+

        +----------------------+--------------------------+
        | StorageBoxOption Key |  StorageBoxOption Value  |
        +======================+==========================+
        |             location | /home/mytardis/var/local |
        +----------------------+--------------------------+

        +-------------------------+---------------------------+
        | StorageBoxAttribute Key | StorageBoxAttribute Value |
        +=========================+===========================+
        |           test_attr_key | test_attr_value           |
        +-------------------------+---------------------------+
    """)
    with requests_mock.Mocker() as mocker:
        get_storagebox_url = "%s/api/v1/storagebox/1/?format=json" % config.url
        mocker.get(get_storagebox_url, text=mock_storagebox_get_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'storagebox', 'get', '1']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
