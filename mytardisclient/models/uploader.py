"""
Model class for MyTardis API v1's UploaderResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import logging
import json
import requests

from mytardisclient.conf import config
from .resultset import ResultSet

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Uploader(object):
    """
    Model class for MyTardis API v1's UploaderResource.
    See: https://github.com/wettenhj/mytardis-app-mydata/blob/master/api.py
    """
    # pylint: disable=too-many-instance-settings
    def __init__(self, uploader_json):
        self.id = uploader_json['id']  # pylint: disable=invalid-name
        self.name = uploader_json['name']
        self.settings_updated = uploader_json['settings_updated']
        self.settings_downloaded = uploader_json['settings_downloaded']
        self.json = uploader_json
        self.settings = []
        for setting_json in uploader_json['settings']:
            self.settings.append(UploaderSetting(setting_json))

    def __str__(self):
        return self.name

    @staticmethod
    @config.region.cache_on_arguments(namespace="Uploader")
    def list(limit=None, offset=None, order_by=None):
        """
        Retrieve a list of storage boxes.

        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Uploader` records, encapsulated in a
            `ResultSet` object`.
        """
        url = "%s/api/v1/mydata_uploader/?format=json" % config.url
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print "URL: %s" % url
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        return ResultSet(Uploader, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Uploader")
    def get(uploader_id):
        """
        Get storage box with ID uploader_id

        :param uploader_id: The ID of a storage box to retrieve.

        :return: A :class:`Uploader` record.
        """
        url = "%s/api/v1/mydata_uploader/%s/?format=json" % \
            (config.url, uploader_id)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        uploader_json = response.json()
        return Uploader(uploader_json=uploader_json)

    @staticmethod
    def update(uploader_id, uuid, settings_json):
        """
        Update the settings in an uploader record.

        Even if you're a facility manager, you're only allowed to
        update an Uploader record if you know its UUID.
        """
        patch_data = {
            'settings': settings_json,
            'uuid': uuid
        }
        url = "%s/api/v1/mydata_uploader/%s/" % (config.url, uploader_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(patch_data))
        logger.debug("PATCH %s %s", url, response.status_code)
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        uploader_json = response.json()
        return Uploader(uploader_json)


class UploaderSetting(object):
    """
    Model class for MyTardis API v1's UploaderSettingAppResource.
    See: https://github.com/wettenhj/mytardis-app-mydata/blob/master/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, uploader_setting_json):
        self.key = uploader_setting_json['key']
        self.value = uploader_setting_json['value']
        self.json = uploader_setting_json
