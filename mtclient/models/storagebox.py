"""
Model class for MyTardis API v1's StorageBoxResource.
"""
from __future__ import print_function

import logging
import requests

from ..conf import config
from .model import Model

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class StorageBox(Model):
    """
    Model class for MyTardis API v1's StorageBoxResource.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, response_dict):
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.name = response_dict['name']
        self.description = response_dict['description']
        self.django_storage_class = response_dict['django_storage_class']
        self.max_size = response_dict['max_size']
        self.status = response_dict['status']
        self.response_dict = response_dict
        self.attributes = []
        for attribute_json in response_dict['attributes']:
            self.attributes.append(StorageBoxAttribute(attribute_json))
        self.options = []
        for option_json in response_dict['options']:
            self.options.append(StorageBoxOption(option_json))

    def __str__(self):
        """
        Return a string representation of a storage box
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of storage boxes.

        :param filters: Filters, e.g. "id=123" or "name=box1"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`StorageBox` records, encapsulated in a
            `ResultSet` object`.
        """
        from ..utils import add_filters, extend_url
        from .resultset import ResultSet

        url = "%s/api/v1/storagebox/?format=json" % config.url
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(StorageBox, url, response.json())

    @staticmethod
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
        return StorageBox(response.json())


class StorageBoxAttribute(object):
    """
    Model class for MyTardis API v1's StorageBoxAttributeResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, response_dict):
        self.key = response_dict['key']
        self.value = response_dict['value']
        self.response_dict = response_dict


class StorageBoxOption(object):
    """
    Model class for MyTardis API v1's StorageBoxOptionResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, response_dict):
        self.key = response_dict['key']
        self.value = response_dict['value']
        self.response_dict = response_dict
