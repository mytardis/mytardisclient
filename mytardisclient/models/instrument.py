"""
Model class for MyTardis API v1's InstrumentResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""
from __future__ import print_function

import json
import logging

import requests

from mytardisclient.conf import config
from .facility import Facility
from .resultset import ResultSet
from mytardisclient.utils.exceptions import DoesNotExist

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Instrument(object):
    """
    Model class for MyTardis API v1's InstrumentResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, instrument_json):
        self.id = instrument_json['id']  # pylint: disable=invalid-name
        self.name = instrument_json['name']
        self.json = instrument_json
        self.facility = Facility(instrument_json['facility'])

    def __str__(self):
        return self.name

    @staticmethod
    @config.region.cache_on_arguments(namespace="Instrument")
    def list(facility_id=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of instruments in a facility with ID facility_id.

        :param facility_id: The ID of a facility to retrieve instruments from.
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Instrument` records, encapsulated in a
            ResultSet object.
        """
        url = "%s/api/v1/instrument/?format=json" % config.url
        if facility_id:
            url += "&facility__id=%s" % facility_id
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
        return ResultSet(Instrument, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Instrument")
    def get(instrument_id):
        """
        Get instrument with ID instrument_id

        :param instrument_id: The ID of an instrument to retrieve.

        :return: An :class:`Instrument` record.
        """
        url = "%s/api/v1/instrument/?format=json&id=%s" % \
            (config.url, instrument_id)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        instruments_json = response.json()
        if instruments_json['meta']['total_count'] == 0:
            message = "Instrument matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Instrument)
        return Instrument(instrument_json=instruments_json['objects'][0])

    @staticmethod
    def create(facility_id, name):
        """
        Create an instrument record.

        :param facility_id: The ID of the facility to create the instrument in.
        :param name: The name of the instrument.

        :return: A new :class:`Instrument` record.
        """
        new_instrument_json = {
            "name": name,
            "facility": "/api/v1/facility/%s/" % facility_id
        }
        url = config.url + "/api/v1/instrument/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_instrument_json))
        logger.debug("POST %s %s", url, response.status_code)
        if response.status_code != 201:
            message = response.text
            raise Exception(message)
        instrument_json = response.json()
        return Instrument(instrument_json)

    @staticmethod
    def update(instrument_id, name):
        """
        Update an instrument record.

        :param instrument_id: The ID of the instrument record to update.
        :param name: The new name of the instrument.

        :return: An updated :class:`Instrument` record.
        """
        updated_fields_json = {
            "name": name,
        }
        url = "%s/api/v1/instrument/%s/" % (config.url, instrument_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print("HTTP %s" % response.status_code)
            message = response.text
            raise Exception(message)
        instrument_json = response.json()
        return Instrument(instrument_json)
