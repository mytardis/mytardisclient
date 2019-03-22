"""
Model class for MyTardis API v1's FacilityResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import logging
import requests

from mytardisclient.conf import config
from .model import Model
from .resultset import ResultSet
from .group import Group

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Facility(Model):
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
        """
        Return a string representation of a facility
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

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
        response.raise_for_status()
        return ResultSet(Facility, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Facility")
    def get(**kwargs):
        """
        Get facility by ID

        :param facility_id: The ID of a facility to retrieve.

        :return: A :class:`Facility` record.

        :raises requests.exceptions.HTTPError:
        """
        if "facility_id" in kwargs:
            facility_id = kwargs["facility_id"]
        else:
            facility_id = kwargs["id"]
        url = "%s/api/v1/facility/%s/?format=json" % (config.url,
                                                      facility_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        facility_json = response.json()
        return Facility(facility_json=facility_json)
