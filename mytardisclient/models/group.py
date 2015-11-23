"""
Model class for MyTardis API v1's GroupResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

# pylint: disable=missing-docstring

import requests
import urllib

from mytardisclient.conf import config
from mytardisclient.logs import logger
from mytardisclient.utils.exceptions import DoesNotExist


class Group(object):
    """
    Model class for MyTardis API v1's GroupResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, name=None, group_json=None):
        self.group_id = None
        self.name = name
        self.group_json = group_json

        if group_json is not None:
            self.group_id = group_json['id']
            if name is None:
                self.name = group_json['name']

    def __str__(self):
        return self.name

    @staticmethod
    def get_group_by_name(name):
        url = config.url + "/api/v1/group/?format=json&name=" + \
            urllib.quote(name)
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            logger.debug("Failed to look up group record for name \"" +
                         name + "\".")
            logger.debug(response.text)
            raise Exception(response.text)
        groups_json = response.json()
        num_groups_found = groups_json['meta']['total_count']

        if num_groups_found == 0:
            raise DoesNotExist(
                message="Group \"%s\" was not found in MyTardis" % name,
                url=url, response=response)
        else:
            logger.debug("Found group record for name '" + name + "'.")
            return Group(name=name, group_json=groups_json['objects'][0])
