"""
Model class for MyTardis API v1's ReplicaResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""


class Replica(object):
    """
    Model class for MyTardis API v1's ReplicaResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, replica_json):
        self.json = replica_json
        self.id = replica_json['id']  # pylint: disable=invalid-name
        if 'location' in replica_json:
            self.location = replica_json['location']
        else:
            self.location = ''
        self.uri = replica_json['uri']
        self.verified = replica_json['verified']
