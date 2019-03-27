"""
test_experiment.py

Tests for functionality to query the Experiment model via
the MyTardis REST API's experiment resource
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.experiment import Experiment

config.url = "https://mytardis-test.example.com"


def test_experiment_list():
    """
    Test listing experiment records exposed in a MyTardis REST API
    """
    mock_experiment_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [{
            "id": 1,
            "title": "Test Experiment",
            "description": "exp description",
            "authors": [
            ],
            "created_by": "/api/v1/user/1/",
            "created_time": "2017-08-03T12:59:48.600082",
            "institution_name": "Monash University",
            "owner_ids": [
                1,
            ],
            "parameter_sets": [
            ],
            "public_access": 1,
            "update_time": "2017-08-03T12:59:48.600106",
            "resource_uri": "/api/v1/experiment/1/",
        }]
    }
    mock_list_response = json.dumps(mock_experiment_list)
    with requests_mock.Mocker() as mocker:
        list_exps_url = "%s/api/v1/experiment/?format=json" % config.url
        mocker.get(list_exps_url, text=mock_list_response)
        experiments = Experiment.list()
        assert experiments.response_dict == mock_experiment_list


def test_experiment_get():
    """
    Test getting a experiment record by ID
    """
    mock_experiment = {
        "id": 1,
        "title": "Test Experiment",
        "description": "exp description",
        "authors": [
        ],
        "created_by": "/api/v1/user/1/",
        "created_time": "2017-08-03T12:59:48.600082",
        "institution_name": "Monash University",
        "owner_ids": [
            1,
        ],
        "parameter_sets": [
        ],
        "public_access": 1,
        "update_time": "2017-08-03T12:59:48.600106",
        "resource_uri": "/api/v1/experiment/1/",
    }
    mock_get_response = json.dumps(mock_experiment)
    with requests_mock.Mocker() as mocker:
        get_experiment_url = "%s/api/v1/experiment/1/?format=json" % config.url
        mocker.get(get_experiment_url, text=mock_get_response)
        experiment = Experiment.objects.get(id=1)
        assert experiment.response_dict == mock_experiment


def test_experiment_create():
    """
    Test creating a experiment record
    """
    mock_experiment = {
        "id": 1,
        "title": "Test Experiment",
        "description": "exp description",
        "authors": [
        ],
        "created_by": "/api/v1/user/1/",
        "created_time": "2017-08-03T12:59:48.600082",
        "institution_name": "Monash University",
        "owner_ids": [
            1,
        ],
        "parameter_sets": [
        ],
        "public_access": 1,
        "update_time": "2017-08-03T12:59:48.600106",
        "resource_uri": "/api/v1/experiment/1/",
    }
    mock_post_response = json.dumps(mock_experiment)
    with requests_mock.Mocker() as mocker:
        post_experiment_url = "%s/api/v1/experiment/" % config.url
        mocker.post(post_experiment_url, text=mock_post_response)
        experiment = Experiment.objects.create(title="experiment title")
        assert experiment.response_dict == mock_experiment
