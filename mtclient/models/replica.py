"""
Model class for MyTardis API v1's ReplicaResource.
"""


class Replica(object):
    """
    Model class for MyTardis API v1's ReplicaResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        if 'location' in response_dict:
            self.location = response_dict['location']
        else:
            self.location = ''
        self.uri = response_dict['uri']
        self.verified = response_dict['verified']
