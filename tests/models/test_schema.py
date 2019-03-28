"""
test_schema.py

Tests for functionality to query the Schema model via
the MyTardis REST API's facility resource
"""
import json
import requests_mock

from mtclient.conf import config
from mtclient.models.schema import Schema, ParameterName


def test_schema_list():
    """
    Test listing schema records exposed in a MyTardis REST API
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
                "hidden": False,
                "id": 1,
                "immutable": True,
                "name": "Schema Name",
                "namespace": "http://schema/namespace",
                "resource_uri": "/api/v1/schema/1/",
                "subtype": "",
                "type": 1
            }
        ]
    }
    mock_list_response = json.dumps(mock_schema_list)
    with requests_mock.Mocker() as mocker:
        list_schemas_url = "%s/api/v1/schema/?format=json" % config.url
        mocker.get(list_schemas_url, text=mock_list_response)
        schemas = Schema.objects.all()
        assert schemas.response_dict == mock_schema_list


def test_schema_get():
    """
    Test getting a schema record by ID
    """
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
    mock_get_response = json.dumps(mock_schema)
    with requests_mock.Mocker() as mocker:
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_get_response)
        schema = Schema.objects.get(id=1)
        assert schema.response_dict == mock_schema


def test_param_names_list():
    """
    Test getting a list of parameter names from a schema ID
    """
    mock_pnames_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [
            {
                "choices": "",
                "comparison_type": 1,
                "data_type": 2,
                "full_name": "Parameter Name",
                "id": 1,
                "immutable": True,
                "is_searchable": False,
                "name": "param name",
                "order": 1,
                "resource_uri": "/api/v1/parametername/1/",
                "schema": "/api/v1/schema/1/",
                "units": ""
            }
        ]
    }
    mock_list_response = json.dumps(mock_pnames_list)
    with requests_mock.Mocker() as mocker:
        list_pnames_url = "%s/api/v1/parametername/?format=json" % config.url
        mocker.get(list_pnames_url, text=mock_list_response)
        param_names = ParameterName.list(schema_id=1)
        assert param_names.response_dict == mock_pnames_list


def test_pname_get():
    """
    Test getting a parameter name record by ID
    """
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
        "choices": "",
        "comparison_type": 1,
        "data_type": 2,
        "full_name": "Parameter Name",
        "id": 1,
        "immutable": True,
        "is_searchable": False,
        "name": "param name",
        "order": 1,
        "resource_uri": "/api/v1/parametername/1/",
        "schema": "/api/v1/schema/1/",
        "units": ""
    }
    mock_pname_response = json.dumps(mock_pname)
    with requests_mock.Mocker() as mocker:
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_schema_response)
        get_pname_url = "%s/api/v1/parametername/1/?format=json" % config.url
        mocker.get(get_pname_url, text=mock_pname_response)
        pname = ParameterName.objects.get(id=1)
        assert pname.response_dict == mock_pname
