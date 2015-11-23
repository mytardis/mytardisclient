"""
Model class for MyTardis API v1's ExperimentResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import json

from .resultset import ResultSet
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

    @staticmethod
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
    def get(exp_id):
        """
        Get experiment with id exp_id
        """
        url = config.url + "/api/v1/experiment/?format=json" + "&id=%s" % exp_id
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
    def create(experiment_title, description=""):
        """
        Create an experiment.
        """
        new_exp_json = {
            "title": experiment_title,
            "description": description,
            "immutable": False
        }
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
