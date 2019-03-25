"""
Model class for MyTardis API v1's StorageBoxResource.
"""
from __future__ import print_function

import logging
import requests

from ..conf import config
from ..utils import extend_url
from .model import Model
from .resultset import ResultSet

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class StorageBox(Model):
    """
    Model class for MyTardis API v1's StorageBoxResource.
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
        """
        Return a string representation of a storage box
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

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
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(StorageBox, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="StorageBox")
    def get(**kwargs):
        r"""
        Retrieve a single storage box record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the StorageBox to retrieve

        :return: A :class:`StorageBox` record.

        :raises requests.exceptions.HTTPError:
        """
        storage_box_id = kwargs.get("id")
        if not storage_box_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for StorageBox get "
                "at this stage.")
        url = "%s/api/v1/storagebox/%s/?format=json" % \
            (config.url, storage_box_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        storage_box_json = response.json()
        return StorageBox(storage_box_json=storage_box_json)


class StorageBoxAttribute(object):
    """
    Model class for MyTardis API v1's StorageBoxAttributeResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, storage_box_attribute_json):
        self.key = storage_box_attribute_json['key']
        self.value = storage_box_attribute_json['value']
        self.json = storage_box_attribute_json


class StorageBoxOption(object):
    """
    Model class for MyTardis API v1's StorageBoxOptionResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, storage_box_option_json):
        self.key = storage_box_option_json['key']
        self.value = storage_box_option_json['value']
        self.json = storage_box_option_json
