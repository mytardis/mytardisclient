"""
Model class for MyTardis API v1's SchemaResource.
"""
from __future__ import print_function

import logging
import requests

from ..conf import config
from ..utils import extend_url
from .model import Model
from .resultset import ResultSet

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Schema(Model):
    """
    Model class for MyTardis API v1's SchemaResource.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, response_dict, param_names=False):
        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.name = response_dict['name']
        self.hidden = response_dict['hidden']
        self.immutable = response_dict['immutable']
        self.namespace = response_dict['namespace']
        type_index = response_dict['type']
        _schema_types = ['', 'Experiment schema', 'Dataset schema', 'Datafile schema',
                         'None', 'Instrument schema']
        self.type = _schema_types[type_index]  # pylint: disable=invalid-name
        self.subtype = response_dict['subtype']

        if param_names:
            self.parameter_names = ParameterName.list(schema_id=self.id)
        else:
            self.parameter_names = ResultSet.empty(ParameterName)

    def __str__(self):
        """
        Return a string representation of a schema
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

    @staticmethod
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
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Schema, url, response.json())

    @staticmethod
    def get(**kwargs):
        r"""
        Retrieve a single schema record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the Schema to retrieve

        :return: A :class:`Schema` record.

        :raises requests.exceptions.HTTPError:
        """
        schema_id = kwargs.get("id")
        if not schema_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for Schema get "
                "at this stage.")
        param_names = kwargs.get("param_names", False)
        url = "%s/api/v1/schema/%s/?format=json" % (config.url, schema_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return Schema(response.json(), param_names)


class ParameterName(Model):
    """
    Model class for MyTardis API v1's ParameterNameResource.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, response_dict):
        self.response_dict = response_dict
        schema_id = response_dict['schema'].split('/')[-2]
        self.schema = Schema.objects.get(id=schema_id)
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.name = response_dict['name']
        self.full_name = response_dict['full_name']
        _type_choices = ['', 'Numeric', 'String', 'URL', 'Link',
                         'Filename', 'DateTime', 'Long String', 'JSON']
        self.data_type = _type_choices[response_dict['data_type']]
        self.units = response_dict['units']
        self.immutable = response_dict['immutable']
        self.is_searchable = response_dict['is_searchable']
        self.order = response_dict['order']
        self.choices = response_dict['choices']
        _comparison_types = \
            ['', 'Exact value', 'Not equal',
             'Range', 'Greater than', 'Greater than or equal to',
             'Less than', 'Less than or equal to', 'Contains']
        self.comparison_type = \
            _comparison_types[response_dict['comparison_type']]

    def __str__(self):
        """
        Return a string representation of a parameter name
        """
        return "<%s: %s>" % (type(self).__name__, self.full_name)

    @staticmethod
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
    def get(**kwargs):
        r"""
        Retrieve a single parameter name record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the ParameterName to retrieve

        :return: A :class:`ParameterName` record.
        """
        pname_id = kwargs.get("id")
        if not pname_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for ParameterName "
                "get at this stage.")
        url = "%s/api/v1/parametername/%s/?format=json" % (config.url,
                                                           pname_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ParameterName(response.json())
