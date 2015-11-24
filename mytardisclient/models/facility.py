"""
Model class for MyTardis API v1's FacilityResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from mytardisclient.conf import config
from .resultset import ResultSet
from .group import Group
from mytardisclient.utils.exceptions import DoesNotExist


class Facility(object):
    """
    Model class for MyTardis API v1's FacilityResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, facility_json):
        self.id = facility_json['id']  # pylint: disable=invalid-name
        self.name = facility_json['name']
        self.json = facility_json
        self.manager_group = \
            Group(group_json=facility_json['manager_group'])

    def __str__(self):
        return self.name

    @staticmethod
    @config.region.cache_on_arguments(namespace="Facility")
    def list(limit=None, offset=None, order_by=None):
        """
        Get facilities I have access to
        """
        url = config.url + "/api/v1/facility/?format=json"
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
            return ResultSet(Facility, url, response.json(),
                             **filters)
        else:
            return ResultSet(Facility, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Facility")
    def get(facility_id):
        """
        Get facility with id facility_id
        """
        url = "%s/api/v1/facility/?format=json&id=%s" % (config.url,
                                                         facility_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        facilities_json = response.json()
        if facilities_json['meta']['total_count'] == 0:
            message = "Facility matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Facility)
        return Facility(facility_json=facilities_json['objects'][0])
