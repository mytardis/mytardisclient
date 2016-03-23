"""
Model class for MyTardis API v1's StorageBoxResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""
from __future__ import print_function

import logging
import requests

from mytardisclient.conf import config
from .resultset import ResultSet

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class StorageBox(object):
    """
    Model class for MyTardis API v1's StorageBoxResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, storage_box_json):
        self.id = storage_box_json['id']  # pylint: disable=invalid-name
        self.name = storage_box_json['name']
        self.description = storage_box_json['description']
        self.django_storage_class = storage_box_json['django_storage_class']
        self.max_size = storage_box_json['max_size']
        self.status = storage_box_json['status']
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
    @config.region.cache_on_arguments(namespace="StorageBox")
    def list(limit=None, offset=None, order_by=None):
        """
        Retrieve a list of storage boxes.

        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`StorageBox` records, encapsulated in a
            `ResultSet` object`.
        """
        url = "%s/api/v1/storagebox/?format=json" % config.url
        if limit:
            url += "&limit=%s" % limit
        if offset:
            url += "&offset=%s" % offset
        if order_by:
            url += "&order_by=%s" % order_by
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
        if response.status_code != 200:
            print("URL: %s" % url)
            print("HTTP %s" % response.status_code)
            message = response.text
            raise Exception(message)
        return ResultSet(StorageBox, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="StorageBox")
    def get(storage_box_id):
        """
        Get storage box with ID storage_box_id

        :param storage_box_id: The ID of a storage box to retrieve.

        :return: A :class:`StorageBox` record.
        """
        url = "%s/api/v1/storagebox/%s/?format=json" % \
            (config.url, storage_box_id)
        response = requests.get(url=url, headers=config.default_headers)
        logger.debug("GET %s %s", url, response.status_code)
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
