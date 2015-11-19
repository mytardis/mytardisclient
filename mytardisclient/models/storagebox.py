"""
Model class for MyTardis API v1's StorageBoxResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests

from .resultset import ResultSet


class StorageBox(object):
    """
    Model class for MyTardis API v1's StorageBoxResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, storage_box_json):
        self.config = config
        self.id = storage_box_json['id']  # pylint: disable=invalid-name
        self.name = storage_box_json['name']
        self.json = storage_box_json
        self.attributes = []
        for attribute_json in storage_box_json['attributes']:
            self.attributes.append(StorageBoxAttribute(config, attribute_json))
        self.options = []
        for option_json in storage_box_json['options']:
            self.options.append(StorageBoxOption(config, option_json))

    def __str__(self):
        return self.name

    @staticmethod
    def list(config, limit=None, offset=None, order_by=None):
        """
        Get storage_boxes I have access to
        """
        url = "%s/api/v1/storagebox/?format=json" % config.mytardis_url
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
            return ResultSet(StorageBox, config, url, response.json(),
                             **filters)
        else:
            return ResultSet(StorageBox, config, url, response.json())

    @staticmethod
    def get(config, storage_box_id):
        """
        Get storage_box with id storage_box_id
        """
        url = "%s/api/v1/storagebox/%s/?format=json" % \
            (config.mytardis_url, storage_box_id)
        headers = {
            "Authorization": "ApiKey %s:%s" % (config.username,
                                               config.api_key),
            "Content-Type": "application/json",
            "Accept": "application/json"}
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        storage_box_json = response.json()
        return StorageBox(config=config, storage_box_json=storage_box_json)


class StorageBoxAttribute(object):
    """
    Model class for MyTardis API v1's StorageBoxAttributeResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, storage_box_attribute_json):
        self.config = config
        self.key = storage_box_attribute_json['key']
        self.value = storage_box_attribute_json['value']
        self.json = storage_box_attribute_json


class StorageBoxOption(object):
    """
    Model class for MyTardis API v1's StorageBoxOptionResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, storage_box_option_json):
        self.config = config
        self.key = storage_box_option_json['key']
        self.value = storage_box_option_json['value']
        self.json = storage_box_option_json
