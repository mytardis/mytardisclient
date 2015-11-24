"""
Model class for MyTardis API v1's StorageBoxResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from mytardisclient.conf import config
from .resultset import ResultSet


class StorageBox(object):
    """
    Model class for MyTardis API v1's StorageBoxResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, storage_box_json):
        self.id = storage_box_json['id']  # pylint: disable=invalid-name
        self.name = storage_box_json['name']
        self.json = storage_box_json
        self.attributes = []
        for attribute_json in storage_box_json['attributes']:
            self.attributes.append(StorageBoxAttribute(attribute_json))
        self.options = []
        for option_json in storage_box_json['options']:
            self.options.append(StorageBoxOption(option_json))

    def __str__(self):
        return self.name

    @staticmethod
    def list(limit=None, offset=None, order_by=None):
        """
        Get storage_boxes I have access to
        """
        url = "%s/api/v1/storagebox/?format=json" % config.url
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            print "URL: %s" % url
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)

        if limit or offset:
            filters = dict(limit=limit, offset=offset)
            return ResultSet(StorageBox, url, response.json(),
                             **filters)
        else:
            return ResultSet(StorageBox, url, response.json())

    @staticmethod
    def get(storage_box_id):
        """
        Get storage_box with id storage_box_id
        """
        url = "%s/api/v1/storagebox/%s/?format=json" % \
            (config.url, storage_box_id)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        storage_box_json = response.json()
        return StorageBox(storage_box_json=storage_box_json)


class StorageBoxAttribute(object):
    """
    Model class for MyTardis API v1's StorageBoxAttributeResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, storage_box_attribute_json):
        self.key = storage_box_attribute_json['key']
        self.value = storage_box_attribute_json['value']
        self.json = storage_box_attribute_json


class StorageBoxOption(object):
    """
    Model class for MyTardis API v1's StorageBoxOptionResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, storage_box_option_json):
        self.key = storage_box_option_json['key']
        self.value = storage_box_option_json['value']
        self.json = storage_box_option_json