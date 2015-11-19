"""
Model class for MyTardis API v1's ExperimentResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import json

from .resultset import ResultSet
# from mytardisclient.logs import logger


class Experiment(object):
    """
    Model class for MyTardis API v1's ExperimentResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, experiment_json):
        self.config = config
        self.json = experiment_json
        self.id = experiment_json['id']  # pylint: disable=invalid-name
        self.title = experiment_json['title']
        self.description = experiment_json['description']

    @staticmethod
    def list(config, limit=None):
        """
        Get experiments I have access to
        """
        url = config.mytardis_url + "/api/v1/experiment/?format=json"
        if limit:
            url += "&limit=%s" % limit
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key),
            "Content-Type": "application/json",
            "Accept": "application/json"}
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            message = response.text
            response.close()
            raise Exception(message)

        if limit:
            return ResultSet(Experiment, config, url, response.json(), limit=limit)
        else:
            return ResultSet(Experiment, config, url, response.json())

    @staticmethod
    def get(config, exp_id):
        """
        Get experiment with id exp_id
        """
        url = config.mytardis_url + "/api/v1/experiment/?format=json" + "&id=%s" % exp_id
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key),
            "Content-Type": "application/json",
            "Accept": "application/json"}
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            message = response.text
            response.close()
            raise Exception(message)

        experiments_json = response.json()
        return Experiment(config=config, experiment_json=experiments_json['objects'][0])

    @staticmethod
    def create(config, experiment_title, description=""):
        """
        Create an experiment.
        """
        new_exp_json = {
            "title": experiment_title,
            "description": description,
            "immutable": False
        }
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key),
            "Content-Type": "application/json",
            "Accept": "application/json"}
        url = config.mytardis_url + "/api/v1/experiment/"
        response = requests.post(headers=headers, url=url,
                                 data=json.dumps(new_exp_json))
        if response.status_code != 201:
            message = response.text
            response.close()
            raise Exception(message)
        experiment_json = response.json()
        return Experiment(config, experiment_json)
