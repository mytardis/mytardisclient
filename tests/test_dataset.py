"""
test_dataset.py

Tests for functionality to query the Dataset model via
the MyTardis REST API's dataset resource
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.dataset import Dataset

config.url = "https://mytardis-test.example.com"


def test_dataset_list():
    """
    Test listing dataset records exposed in a MyTardis REST API
    """
    mock_dataset_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [{
            "created_time": None,
            "description": "dataset description",
            "directory": None,
            "experiments": [
                "/api/v1/experiment/1/"
            ],
            "id": 1,
            "immutable": False,
            "instrument": {
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
            },
            "modified_time": None,
            "parameter_sets": [],
            "resource_uri": "/api/v1/dataset/1/"
        }]
    }
    mock_list_response = json.dumps(mock_dataset_list)
    with requests_mock.Mocker() as mocker:
        list_datasets_url = "%s/api/v1/dataset/?format=json&experiments__id=1" % config.url
        mocker.get(list_datasets_url, text=mock_list_response)
        datasets = Dataset.list(experiment_id=1)
        assert datasets.response_dict == mock_dataset_list


def test_dataset_get():
    """
    Test getting a dataset record by ID
    """
    mock_dataset = {
        "created_time": None,
        "description": "dataset description",
        "directory": None,
        "experiments": [
            "/api/v1/experiment/1/"
        ],
        "id": 1,
        "immutable": False,
        "instrument": {
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
        },
        "modified_time": None,
        "parameter_sets": [],
        "resource_uri": "/api/v1/dataset/1/"
    }
    mock_get_response = json.dumps(mock_dataset)
    with requests_mock.Mocker() as mocker:
        get_dataset_url = "%s/api/v1/dataset/1/?format=json" % config.url
        mocker.get(get_dataset_url, text=mock_get_response)
        dataset = Dataset.objects.get(id=1)
        assert dataset.response_dict == mock_dataset


def test_dataset_create():
    """
    Test creating a dataset record
    """
    mock_dataset = {
        "created_time": None,
        "description": "dataset description",
        "directory": None,
        "experiments": [
            "/api/v1/experiment/1/"
        ],
        "id": 1,
        "immutable": False,
        "instrument": {
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
        },
        "modified_time": None,
        "parameter_sets": [],
        "resource_uri": "/api/v1/dataset/1/"
    }
    mock_post_response = json.dumps(mock_dataset)
    with requests_mock.Mocker() as mocker:
        post_dataset_url = "%s/api/v1/dataset/" % config.url
        mocker.post(post_dataset_url, text=mock_post_response)
        dataset = Dataset.objects.create(
            experiment_id=1, instrument_id=1,
            description="dataset description")
        assert dataset.response_dict == mock_dataset
