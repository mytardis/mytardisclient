"""
Model class for MyTardis API v1's ExperimentResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import json
import os

from .resultset import ResultSet
from .schema import Schema
from .schema import ParameterName
from mytardisclient.conf import config
from mytardisclient.utils.exceptions import DoesNotExist


class Experiment(object):
    """
    Model class for MyTardis API v1's ExperimentResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, experiment_json=None):
        self.json = experiment_json
        self.id = None  # pylint: disable=invalid-name
        self.title = None
        self.description = None
        self.institution_name = None
        if experiment_json:
            for key in self.__dict__.keys():
                if key in experiment_json:
                    self.__dict__[key] = experiment_json[key]
        self.parameter_sets = []
        for exp_param_set_json in experiment_json['parameter_sets']:
            self.parameter_sets.append(
                ExperimentParameterSet(exp_param_set_json))

    @staticmethod
    @config.region.cache_on_arguments(namespace="Experiment")
    def list(limit=None, offset=None, order_by=None):
        """
        Get experiments I have access to
        """
        url = config.url + "/api/v1/experiment/?format=json"
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        if limit or offset:
            filters = dict(limit=limit, offset=offset)
            return ResultSet(Experiment, url, response.json(), **filters)
        else:
            return ResultSet(Experiment, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Experiment")
    def get(exp_id):
        """
        Get experiment with id exp_id
        """
        url = "%s/api/v1/experiment/?format=json&id=%s" \
            % (config.url, exp_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        experiments_json = response.json()
        if experiments_json['meta']['total_count'] == 0:
            message = "Experiment matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Experiment)
        return Experiment(experiment_json=experiments_json['objects'][0])

    @staticmethod
    def create(title, description="", institution=None, params_file_json=None):
        """
        Create an experiment.
        """
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
        if response.status_code != 201:
            message = response.text
            raise Exception(message)
        experiment_json = response.json()
        return Experiment(experiment_json)

    @staticmethod
    def update(experiment_id, title, description):
        """
        Update an experiment record.
        """
        updated_fields_json = dict()
        updated_fields_json['title'] = title
        updated_fields_json['description'] = description
        url = "%s/api/v1/experiment/%s/" % \
            (config.url, experiment_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        experiment_json = response.json()
        return Experiment(experiment_json)


class ExperimentParameterSet(object):
    """
    Model class for MyTardis API v1's ExperimentParameterSetResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, expparamset_json):
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
        """
        url = "%s/api/v1/experimentparameterset/?format=json" % config.url
        url += "&experiments__id=%s" % experiment_id
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        filters = dict(experiment_id=experiment_id)
        return ResultSet(ExperimentParameterSet, url, response.json(),
                         **filters)


class ExperimentParameter(object):
    """
    Model class for MyTardis API v1's ExperimentParameterResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, expparam_json):
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
        pass
