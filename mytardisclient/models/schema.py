"""
Model class for MyTardis API v1's SchemaResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from mytardisclient.conf import config
from .resultset import ResultSet


class Schema(object):
    """
    Model class for MyTardis API v1's SchemaResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, schema_json):
        self.json = schema_json
        self.id = schema_json['id']  # pylint: disable=invalid-name
        self.name = schema_json['name']
        self.hidden = schema_json['hidden']
        self.immutable = schema_json['immutable']
        self.namespace = schema_json['namespace']
        type_index = schema_json['type']
        types = ['', 'Experiment schema', 'Dataset schema', 'Datafile schema',
                 'None', 'Instrument schema']
        self.type = types[type_index]  # pylint: disable=invalid-name
        self.subtype = schema_json['subtype']

    def __str__(self):
        return self.name

    @staticmethod
    def list(limit=None, offset=None, order_by=None):
        """
        Get schemas I have access to
        """
        url = "%s/api/v1/schema/?format=json" % config.url
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "URL: %s" % url
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)

        if limit or offset:
            filters = dict(limit=limit, offset=offset)
            return ResultSet(Schema, url, response.json(), **filters)
        else:
            return ResultSet(Schema, url, response.json())

    @staticmethod
    def get(schema_id):
        """
        Get schema with id schema_id
        """
        url = "%s/api/v1/schema/%s/?format=json" % (config.url, schema_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        schema_json = response.json()
        return Schema(schema_json=schema_json)
