"""
Model class for MyTardis API v1's ExperimentResource.
"""
from __future__ import print_function

import logging

import requests

from ..conf import config
from .model import Model

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Experiment(Model):
    """
    Model class for MyTardis API v1's ExperimentResource.
    """
    def __init__(self, experiment_json=None, include_metadata=False):
        self.json = experiment_json
        self.id = None  # pylint: disable=invalid-name
        self.title = None
        self.description = None
        self.institution_name = None
        if experiment_json:
            for key in self.__dict__:
                if key in experiment_json:
                    self.__dict__[key] = experiment_json[key]
        if include_metadata:
            self.parameter_sets = []
            for exp_param_set_json in experiment_json['parameter_sets']:
                self.parameter_sets.append(
                    ExperimentParameterSet(exp_param_set_json))

    def __str__(self):
        """
        Return a string representation of an experiment
        """
        return "<%s: %s>" % (type(self).__name__, self.title)

    @staticmethod
    @config.region.cache_on_arguments(namespace="Experiment")
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of experiments.

        :param filters: Filters, e.g. "title=Exp Title"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Experiment` records, encapsulated in a
            `ResultSet` object.
        """
        from ..utils import extend_url, add_filters
        from .resultset import ResultSet

        url = "%s/api/v1/experiment/?format=json" % config.url
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Experiment, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Experiment")
    def get(**kwargs):
        r"""
        Retrieve a single experiment record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the Experiment to retrieve

        :return: An :class:`Experiment` record.

        :raises requests.exceptions.HTTPError:
        """
        from ..utils.exceptions import DoesNotExist

        exp_id = kwargs.get("id")
        if not exp_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for Experiment get "
                "at this stage.")
        include_metadata = kwargs.get("include_metadata", False)
        url = "%s/api/v1/experiment/?format=json&id=%s" \
            % (config.url, exp_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        experiments_json = response.json()
        if experiments_json['meta']['total_count'] == 0:
            message = "Experiment matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Experiment)
        return Experiment(experiment_json=experiments_json['objects'][0],
                          include_metadata=include_metadata)

    @staticmethod
    def create(title, description="", institution=None, params_file_json=None):
        """
        Create an experiment record.

        :param title: The title of the experiment.
        :param description: The description of the experiment.
        :param institution: The institution of the experiment.
        :param params_file_json: Path to a JSON file with experiment
            parameters.

        :return: A new :class:`Dataset` record.
        """
        import json
        import os

        new_exp_json = {
            "title": title,
            "description": description,
            "immutable": False
        }
        if institution:
            new_exp_json['institution'] = institution
        if params_file_json:
            assert os.path.exists(params_file_json)
            with open(params_file_json) as params_file:
                new_exp_json['parameter_sets'] = json.load(params_file)
        url = config.url + "/api/v1/experiment/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_exp_json))
        response.raise_for_status()
        experiment_json = response.json()
        return Experiment(experiment_json)

    @staticmethod
    def update(experiment_id, title, description):
        """
        Update an experiment record.
        """
        import json

        updated_fields_json = dict()
        updated_fields_json['title'] = title
        updated_fields_json['description'] = description
        url = "%s/api/v1/experiment/%s/" % \
            (config.url, experiment_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        response.raise_for_status()
        experiment_json = response.json()
        return Experiment(experiment_json)


class ExperimentParameterSet(object):
    """
    Model class for MyTardis API v1's ExperimentParameterSetResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, expparamset_json):
        from .schema import Schema
        self.json = expparamset_json
        self.id = expparamset_json['id']  # pylint: disable=invalid-name
        self.experiment = expparamset_json['experiment']
        self.schema = Schema(expparamset_json['schema'])
        self.parameters = []
        for exp_param_json in expparamset_json['parameters']:
            self.parameters.append(ExperimentParameter(exp_param_json))

    @staticmethod
    @config.region.cache_on_arguments(namespace="ExperimentParameterSet")
    def list(experiment_id):
        """
        List experiment parameter sets associated with experiment ID
        experiment_id.

        :param experiment_id: The ID of the experiment to retrieve parameter
            sets for.

        :return: A list of :class:`ExperimentParameterSet` records,
            encapsulated in a `ResultSet` object`.
        """
        from .resultset import ResultSet

        url = "%s/api/v1/experimentparameterset/?format=json" % config.url
        url += "&experiments__id=%s" % experiment_id
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(ExperimentParameterSet, url, response.json())


class ExperimentParameter(object):
    """
    Model class for MyTardis API v1's ExperimentParameterResource.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, expparam_json):
        from .schema import ParameterName
        self.json = expparam_json
        self.id = expparam_json['id']  # pylint: disable=invalid-name
        self.name = ParameterName.get(expparam_json['name'].split('/')[-2])
        self.string_value = expparam_json['string_value']
        self.numerical_value = expparam_json['numerical_value']
        self.datetime_value = expparam_json['datetime_value']
        self.link_id = expparam_json['link_id']
        self.value = expparam_json['value']

    @staticmethod
    @config.region.cache_on_arguments(namespace="ExperimentParameter")
    def list(exp_param_set):
        """
        List experiment parameter records in parameter set.
        """
