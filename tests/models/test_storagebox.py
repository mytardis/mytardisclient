"""
test_storagebox.py

Tests for functionality to query the StorageBox model via
the MyTardis REST API's facility resource
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.storagebox import StorageBox


def test_storagebox_list():
    """
    Test listing storage box records exposed in a MyTardis REST API
    """
    mock_storagebox_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [
            {
                "attributes": [
                ],
                "description": "Storage box description",
                "django_storage_class":
                    "tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage",
                "id": 1,
                "max_size": "9999999999",
                "name": "local box at /home/mytardis/var/local",
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
                "status": "online"
            }
        ]
    }
    mock_list_response = json.dumps(mock_storagebox_list)
    with requests_mock.Mocker() as mocker:
        list_storageboxes_url = "%s/api/v1/storagebox/?format=json" % config.url
        mocker.get(list_storageboxes_url, text=mock_list_response)
        boxes = StorageBox.objects.all()
        boxes._execute_query()
        assert boxes._result_set.response_dict == mock_storagebox_list


def test_storagebox_get():
    """
    Test getting a storage box record by ID
    """
    mock_storagebox = {
        "attributes": [
        ],
        "description": "Storage box description",
        "django_storage_class": "tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage",
        "id": 1,
        "max_size": "9999999999",
        "name": "local box at /home/mytardis/var/local",
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
        "status": "online"
    }
    mock_get_response = json.dumps(mock_storagebox)
    with requests_mock.Mocker() as mocker:
        get_storagebox_url = "%s/api/v1/storagebox/1/?format=json" % config.url
        mocker.get(get_storagebox_url, text=mock_get_response)
        storagebox = StorageBox.objects.get(id=1)
        assert storagebox.response_dict == mock_storagebox
