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
    def __init__(self, model, endpoint_type, endpoint):
        self.model = model
        self.endpoint_type = endpoint_type
        self.endpoint = endpoint

    def __unicode__(self):
        return "%s: %s" % (self.endpoint_type, self.endpoint)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    @staticmethod
    def list():
        """
        Get a list of API endpoints.
        """
        url = config.url + "/api/v1/?format=json"
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        endpoints_json = response.json()
        endpoints = {}
        for model in endpoints_json.keys():
            endpoints[model] = dict()
            for endpoint_type in endpoints_json[model].keys():
                endpoint = endpoints_json[model][endpoint_type]
                endpoints[model][endpoint_type] = \
                    ApiEndpoint(model, endpoint_type, endpoint)
        return endpoints
