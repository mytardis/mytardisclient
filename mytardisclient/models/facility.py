"""
Model class for MyTardis API v1's FacilityResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from .resultset import ResultSet
# from mytardisclient.logs import logger
from .group import Group


class Facility(object):
    """
    Model class for MyTardis API v1's FacilityResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, facility_json):
        self.config = config
        self.id = facility_json['id']  # pylint: disable=invalid-name
        self.name = facility_json['name']
        self.json = facility_json
        self.manager_group = \
            Group(group_json=facility_json['manager_group'])

    def __str__(self):
        return self.name

    @staticmethod
    def list(config, limit=None):
        """
        Get facilities I have access to
        """
        url = config.mytardis_url + "/api/v1/facility/?format=json"
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
            return ResultSet(Facility, config, url, response.json(),
                             limit=limit)
        else:
            return ResultSet(Facility, config, url, response.json())

    @staticmethod
    def get(config, facility_id):
        """
        Get facilities with id facility_id
        """
        url = "%s/api/v1/facility/?format=json&id=%s" % (config.mytardis_url,
                                                         facility_id)
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

        return Facility(config=config,
                        facility_json=response.json()['objects'][0])
