"""
Model class for MyTardis API v1's GroupResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

# pylint: disable=missing-docstring


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
