"""
Model class for MyTardis API v1's ReplicaResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

# from mytardisclient.logs import logger


class Replica(object):
    """
    Model class for MyTardis API v1's ReplicaResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, config, replica_json):
        self.config = config
        self.json = replica_json
        self.id = replica_json['id']  # pylint: disable=invalid-name
        self.verified = replica_json['verified']
