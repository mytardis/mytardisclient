"""
Model class for MyTardis API v1's SchemaResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from mytardisclient.conf import config
from .resultset import ResultSet
from mytardisclient.utils.exceptions import DoesNotExist


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
        _schema_types = ['', 'Experiment schema', 'Dataset schema', 'Datafile schema',
                         'None', 'Instrument schema']
        self.type = _schema_types[type_index]  # pylint: disable=invalid-name
        self.subtype = schema_json['subtype']

        self.parameter_names = ParameterName.list(schema=self)

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
            if response.status_code == 404:
                message = "Schema ID %s doesn't exist." % schema_id
                raise DoesNotExist(message, url, response, Schema)
            message = response.text
            raise Exception(message)

        schema_json = response.json()
        return Schema(schema_json=schema_json)


class ParameterName(object):
    """
    Model class for MyTardis API v1's ParameterNameResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, parametername_json):
        self.json = parametername_json
        self.schema = parametername_json['schema']
        self.id = parametername_json['id']  # pylint: disable=invalid-name
        self.name = parametername_json['name']
        self.full_name = parametername_json['full_name']
        _type_choices = ['', 'Numeric', 'String', 'URL', 'Link',
                         'Filename', 'DateTime', 'Long String', 'JSON']
        self.data_type = _type_choices[parametername_json['data_type']]
        self.units = parametername_json['units']
        self.immutable = parametername_json['immutable']
        self.is_searchable = parametername_json['is_searchable']
        self.order = parametername_json['order']
        self.choices = parametername_json['choices']
        _comparison_types = \
            ['', 'Exact value', 'Not equal',
             'Range', 'Greater than', 'Greater than or equal to',
             'Less than', 'Less than or equal to', 'Contains']
        self.comparison_type = \
            _comparison_types[parametername_json['comparison_type']]

    def __str__(self):
        return self.name

    @staticmethod
    def list(schema):
        """
        List parameter name records in schema.
        """
        # We would use "&schema__id=" if it were supported by MyTardis:
        url = "%s/api/v1/parametername/?format=json" % config.url
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "URL: %s" % url
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        parameter_names_json = response.json()
        num_records = len(parameter_names_json['objects'])

        schema_resource_uri = "/api/v1/schema/%s/" % schema.id
        parameter_names_json['objects'] = \
            [pn for pn in parameter_names_json['objects']
             if pn['schema'] == schema_resource_uri]

        offset = 0
        limit = parameter_names_json['meta']['limit']
        total_count = parameter_names_json['meta']['total_count']
        while num_records < total_count:
            offset += limit
            url = "%s/api/v1/parametername/?format=json" % config.url
            url += "&offset=%s" % offset
            response = requests.get(url=url, headers=config.default_headers)
            if response.status_code != 200:
                print "URL: %s" % url
                print "HTTP %s" % response.status_code
                message = response.text
                raise Exception(message)
            parameter_names_page_json = response.json()
            num_records += len(parameter_names_page_json['objects'])
            parameter_names_page_json['objects'] = \
                [pn for pn in parameter_names_page_json['objects']
                 if pn['schema'] == schema_resource_uri]
            parameter_names_json['objects'].extend(parameter_names_page_json['objects'])

        return ResultSet(ParameterName, url, parameter_names_json)
