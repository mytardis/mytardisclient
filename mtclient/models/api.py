"""
The api module contains model classes for MyTardis API v1's endpoints.

This following lists all of the supported endpoints: /api/v1/?format=json

API functionality available for a particular model can be retrieved with:
    /api/v1/facility/schema/?format=json

The 'schema' request above requires authentication.
"""
from __future__ import print_function

import requests
import six

from ..conf import config


class ApiEndpoint(object):
    """
    Model class for MyTardis API v1's endpoints.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, model, endpoint_json):
        self.json = endpoint_json
        self.model = model
        self.list_endpoint = endpoint_json['list_endpoint']
        self.schema = endpoint_json['schema']

    def __str__(self):
        """
        Return a string representation of an API endpoint
        """
        return "%s: %s, %s" % (self.model, self.list_endpoint, self.schema)

    def __repr__(self):
        """
        Return a string representation of an API endpoint
        """
        return self.__str__()

    @staticmethod
    def list():
        """
        Retrieve a list of API endpoints, encapsulated in
        an :class:`ApiEndpoints` object.

        The :class:`ApiEndpoints` object encapsulates the entire JSON response
        from the /api/v1/ query.

        :return: A list of API endpoints, encapsulated in
            an :class:`ApiEndpoints` object.
        """
        url = "%s/api/v1/?format=json" % config.url
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        endpoints_json = response.json()
        return ApiEndpoints(endpoints_json)


class ApiSchema(object):
    """
    Model class for MyTardis API v1's schemas.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    def __init__(self, model, schema_json):
        """
        :param model: The name of an API-accessible model, e.g. 'dataset_file'.
        :param schema_json: The JSON returned from an /api/v1/model/schema/
            query.
        """
        self.model = model
        self.json = schema_json
        self.fields = schema_json['fields']
        self.filtering = schema_json['filtering'] if 'filtering' in schema_json else {}
        for key, val in six.iteritems(self.filtering):
            if val == 1:
                self.filtering[key] = "ALL"
            elif val == 2:
                self.filtering[key] = "ALL_WITH_RELATIONS"
        self.ordering = schema_json['ordering'] if 'ordering' in schema_json else {}
        self.allowed_list_http_methods = schema_json['allowed_list_http_methods']
        self.allowed_detail_http_methods = schema_json['allowed_detail_http_methods']
        self.default_format = schema_json['default_format']
        self.default_limit = schema_json['default_limit']

    @staticmethod
    def get(model):
        """
        Get a list of API-accessible functionality for a particular model.

        :param model: The name of an API-accessible model, e.g. 'dataset_file'.
        :return: An :class:`ApiSchema` object, which encapsulates the list of
                API-accessible functionality for a particular model.
        """
        if model == "datafile":
            model = "dataset_file"
        url = "%s/api/v1/%s/schema/?format=json" % (config.url, model)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        api_schema = response.json()
        return ApiSchema(model, api_schema)


class ApiEndpoints(object):
    """
    Dictionary of API endpoints (list_endpoint and schema)
    with model names as keys.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, json):
        """
        Dictionary of API endpoints with model names as keys.

        :param json: The JSON returned by the /api/v1/ query.
        """
        self.json = json
        self.total_count = len(self.json.keys())

    def __len__(self):
        """
        Return the number of models accessible via the API.
        :return: The number of models accessible via the API.
        """
        return len(self.json.keys())

    def __getitem__(self, model):
        """
        Return the API endpoint for a particular model.

        :param model: The name of an API-accessible model, e.g. 'dataset_file'.
        :return: The :class:`ApiEndpoint` object for that supplied model.
        """
        return ApiEndpoint(model, self.json[model])

    def __iter__(self):
        """
        Iterate the :class:`ApiEndpoints` set.
        """
        for index in range(0, len(self)):
            model = list(self.json.keys())[index]
            yield ApiEndpoint(model, self.json[model])
