"""
Model class for MyTardis API v1's FacilityResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import logging
import requests

from mytardisclient.conf import config
from .resultset import ResultSet
from .group import Group
from mytardisclient.utils.exceptions import DoesNotExist

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


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
        Retrieve a list of facilities.

        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Facility` records, encapsulated in a
            `ResultSet` object`.
        """
        url = config.url + "/api/v1/facility/?format=json"
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)
        return ResultSet(Facility, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Facility")
    def get(facility_id):
        """
        Get facility with ID facility_id

        :param facility_id: The ID of a facility to retrieve.

        :return: A :class:`Facility` record.
        """
        url = "%s/api/v1/facility/?format=json&id=%s" % (config.url,
                                                         facility_id)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        facilities_json = response.json()
        if facilities_json['meta']['total_count'] == 0:
            message = "Facility matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Facility)
        return Facility(facility_json=facilities_json['objects'][0])
