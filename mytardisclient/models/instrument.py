"""
Model class for MyTardis API v1's InstrumentResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import json

from .facility import Facility
from .resultset import ResultSet
# from mytardisclient.logs import logger


class Instrument(object):
    """
    Model class for MyTardis API v1's InstrumentResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, instrument_json):
        self.config = config
        self.id = instrument_json['id']  # pylint: disable=invalid-name
        self.name = instrument_json['name']
        self.json = instrument_json
        self.facility = Facility(config, instrument_json['facility'])

    def __str__(self):
        return self.name

    @staticmethod
    def list(config, facility_id=None, limit=None):
        """
        Get instruments in facility with ID facility_id.
        """
        url = "%s/api/v1/instrument/?format=json" % config.mytardis_url
        if facility_id:
            url += "&facility__id=%s" % facility_id
        if limit:
            url += "&limit=%s" % limit
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            response.close()
            raise Exception(message)

        if facility_id or limit:
            filters = dict(facility_id=facility_id, limit=limit)
            return ResultSet(Instrument, config, url, response.json(),
                             **filters)
        else:
            return ResultSet(Instrument, config, url, response.json())

    @staticmethod
    def get(config, instrument_id):
        """
        Get instruments with id instrument_id
        """
        url = config.mytardis_url + "/api/v1/instrument/?format=json" + "&id=%s" % instrument_id
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            response.close()
            raise Exception(message)

        return Instrument(config=config, instrument_json=response.json()['objects'][0])

    @staticmethod
    def create(config, facility_id, name):
        """
        Create an instrument.
        """
        new_instrument_json = {
            "name": name,
            "facility": "/api/v1/facility/%s/" % facility_id
        }
        url = config.mytardis_url + "/api/v1/instrument/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_instrument_json))
        if response.status_code != 201:
            message = response.text
            response.close()
            raise Exception(message)
        instrument_json = response.json()
        return Instrument(config, instrument_json)

    @staticmethod
    def update(config, instrument_id, name):
        """
        Update an instrument record.
        """
        updated_fields_json = {
            "name": name,
        }
        url = "%s/api/v1/instrument/%s/" % \
            (config.mytardis_url, instrument_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            message = response.text
            response.close()
            raise Exception(message)
        instrument_json = response.json()
        return Instrument(config, instrument_json)
