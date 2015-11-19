"""
Model class for MyTardis API v1's FacilityResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from .resultset import ResultSet
# from mytardisclient.logs import logger
from .group import Group
from mytardisclient.utils.exceptions import DoesNotExist


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
    def list(config, limit=None, offset=None, order_by=None):
        """
        Get facilities I have access to
        """
        url = config.mytardis_url + "/api/v1/facility/?format=json"
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
            return ResultSet(Facility, config, url, response.json(),
                             **filters)
        else:
            return ResultSet(Facility, config, url, response.json())

    @staticmethod
    def get(config, facility_id):
        """
        Get facility with id facility_id
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
            raise Exception(message)

        facilities_json = response.json()
        if facilities_json['meta']['total_count'] == 0:
            message = "Facility matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Facility)
        return Facility(config=config,
                        facility_json=facilities_json['objects'][0])
