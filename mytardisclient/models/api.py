"""
Model class for MyTardis API v1's endpoints.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py

This following lists all of the supported endpoints:
    /api/v1/?format=json

And this lists supported methods on an endpoint:
    /api/v1/facility/schema/?format=json

The 'schema' request above requires authentication.
"""

import requests

from mytardisclient.conf import config


class ApiEndpoint(object):
    """
    Model class for MyTardis API v1's endpoints.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, model, endpoint_json):
        self.json = endpoint_json
        self.model = model
        self.list_endpoint = endpoint_json['list_endpoint']
        self.schema = endpoint_json['schema']

    def __unicode__(self):
        return "%s: %s, %s" % (self.model, self.list_endpoint, self.schema)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    @staticmethod
    def list():
        """
        Get a list of API endpoints.
        """
        url = "%s/api/v1/?format=json" % config.url
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        endpoints_json = response.json()
        return ApiEndpoints(endpoints_json)


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
        """
        self.json = json
        self.index = -1
        self.total_count = len(self.json.keys())

    def __len__(self):
        """
        Return number of models accessible via API.
        """
        return len(self.json.keys())

    def __getitem__(self, model):
        """
        Get an endpoint from the set.
        """
        return ApiEndpoint(model, self.json[model])

    def __iter__(self):
        """__iter__"""
        return self

    def next(self):
        """next"""
        self.index += 1
        if self.index >= len(self):
            raise StopIteration
        model = self.json.keys()[self.index]
        return ApiEndpoint(model, self.json[model])
