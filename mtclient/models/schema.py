"""
Model class for MyTardis API v1's SchemaResource.
"""
from __future__ import print_function

import logging
import requests

from ..conf import config
from .model import Model
from .resultset import ResultSet

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Schema(Model):
    """
    Model class for MyTardis API v1's SchemaResource.
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

        self.parameter_names = ParameterName.list(schema_id=self.id)

    def __str__(self):
        """
        Return a string representation of a schema
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

    @staticmethod
    @config.region.cache_on_arguments(namespace="Schema")
    def list(limit=None, offset=None, order_by=None):
        """
        Retrieve a list of schemas.

        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Schema` records, encapsulated in a
            `ResultSet` object`.
        """
        url = "%s/api/v1/schema/?format=json" % config.url
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Schema, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Schema")
    def get(**kwargs):
        """
        Get schema by ID

        :param schema_id: The ID of a schema to retrieve.

        :return: A :class:`Schema` record.

        :raises requests.exceptions.HTTPError:
        """
        if "schema_id" in kwargs:
            schema_id = kwargs["schema_id"]
        else:
            schema_id = kwargs["id"]
        url = "%s/api/v1/schema/%s/?format=json" % (config.url, schema_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        schema_json = response.json()
        return Schema(schema_json=schema_json)


class ParameterName(object):
    """
    Model class for MyTardis API v1's ParameterNameResource.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, parametername_json):
        self.json = parametername_json
        schema_id = parametername_json['schema'].split('/')[-2]
        self.schema = Schema.objects.get(id=schema_id)
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
        """
        Return a string representation of a parameter name
        """
        return "<%s: %s>" % (type(self).__name__, self.full_name)

    @staticmethod
    @config.region.cache_on_arguments(namespace="ParameterName")
    def list(schema_id):
        """
        Retrieve the list of parameter name records in a schema.

        :param schema_id: The ID of the schema to retrieve parameter names for.

        :return: A list of :class:`ParameterName` records,
            encapsulated in a `ResultSet` object`.
        """
        url = "%s/api/v1/parametername/?format=json&schema__id=%s" \
            % (config.url, schema_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        parameter_names_json = response.json()
        num_records = len(parameter_names_json['objects'])

        schema_resource_uri = "/api/v1/schema/%s/" % schema_id
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
            response.raise_for_status()
            parameter_names_page_json = response.json()
            num_records += len(parameter_names_page_json['objects'])
            parameter_names_page_json['objects'] = \
                [pn for pn in parameter_names_page_json['objects']
                 if pn['schema'] == schema_resource_uri]
            parameter_names_json['objects'].extend(parameter_names_page_json['objects'])

        return ResultSet(ParameterName, url, parameter_names_json)

    @staticmethod
    @config.region.cache_on_arguments(namespace="ParameterName")
    def get(parametername_id):
        """
        Get parameter name with id parametername_id

        :param parametername_id: The ID of a parameter name to retrieve.

        :return: A :class:`ParameterName` record.
        """
        url = "%s/api/v1/parametername/%s/?format=json" % (config.url,
                                                           parametername_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        parametername_json = response.json()
        return ParameterName(parametername_json=parametername_json)
