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
    def __init__(self, model, endpoint_dict):
        """
        :param model: The name of the API model resource, e.g. 'dataset_file'
        :param endpoint_dict: A dictionary with two keys: 'list_endpoint' and
            'schema', e.g. {"list_endpoint": "/api/v1/dataset_file/",
            "schema": "/api/v1/dataset_file/schema/"}. This dictionary is
            obtained by isolating a single model resource from the
            deserialized response from /api/v1/?format=json
        """
        self.response_dict = endpoint_dict
        self.model = model
        self.list_endpoint = endpoint_dict['list_endpoint']
        self.schema = endpoint_dict['schema']

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
        return ApiEndpoints(response.json())


class ApiSchema(object):
    """
    Model class for MyTardis API v1's schemas.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    def __init__(self, model, response_dict):
        """
        :param model: The name of an API-accessible model, e.g. 'dataset_file'.
        :param response_dict: The JSON-deserialized response from an
            /api/v1/model/schema/ query
        """
        self.model = model
        self.response_dict = response_dict
        self.fields = response_dict['fields']
        self.filtering = response_dict['filtering'] if 'filtering' in response_dict else {}
        for key, val in six.iteritems(self.filtering):
            if val == 1:
                self.filtering[key] = "ALL"
            elif val == 2:
                self.filtering[key] = "ALL_WITH_RELATIONS"
        self.ordering = response_dict['ordering'] if 'ordering' in response_dict else {}
        self.allowed_list_http_methods = response_dict['allowed_list_http_methods']
        self.allowed_detail_http_methods = response_dict['allowed_detail_http_methods']
        self.default_format = response_dict['default_format']
        self.default_limit = response_dict['default_limit']

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
        return ApiSchema(model, response.json())


class ApiEndpoints(object):
    """
    Dictionary of API endpoints (list_endpoint and schema)
    with model names as keys.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, response_dict):
        """
        Dictionary of API endpoints with model names as keys.

        :param response_dict: The deserialized response from the /api/v1/ query
        """
        self.response_dict = response_dict
        self.total_count = len(self.response_dict.keys())

    def __len__(self):
        """
        Return the number of models accessible via the API.
        :return: The number of models accessible via the API.
        """
        return len(self.response_dict.keys())

    def __getitem__(self, model):
        """
        Return the API endpoint for a particular model.

        :param model: The name of an API-accessible model, e.g. 'dataset_file'.
        :return: The :class:`ApiEndpoint` object for that supplied model.
        """
        return ApiEndpoint(model, self.response_dict[model])

    def __iter__(self):
        """
        Iterate the :class:`ApiEndpoints` set.
        """
        for index in range(0, len(self)):
            model = list(self.response_dict.keys())[index]
            yield ApiEndpoint(model, self.response_dict[model])
