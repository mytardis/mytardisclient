"""
Model class for MyTardis API v1's DatasetResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import json

from mytardisclient.conf import config
from .resultset import ResultSet
from .instrument import Instrument
from mytardisclient.utils.exceptions import DoesNotExist


class Dataset(object):
    """
    Model class for MyTardis API v1's DatasetResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, dataset_json=None):
        self.json = dataset_json
        self.id = None  # pylint: disable=invalid-name
        self.description = None
        self.instrument = None
        self.experiments = []
        if dataset_json:
            for key in self.__dict__.keys():
                if key in dataset_json:
                    self.__dict__[key] = dataset_json[key]
            if dataset_json['instrument']:
                self.instrument = Instrument(dataset_json['instrument'])

    @staticmethod
    @config.region.cache_on_arguments(namespace="Dataset")
    def list(experiment_id=None,
             limit=None, offset=None, order_by=None):
        """
        Get datasets I have access to
        """
        url = "%s/api/v1/dataset/?format=json" % config.url
        if experiment_id:
            url += "&experiments__id=%s"  % experiment_id
        if limit:
            url += "&limit=%s"  % limit
        if offset:
            url += "&offset=%s"  % offset
        if order_by:
            url += "&order_by=%s"  % order_by
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        if experiment_id or limit or offset:
            filters = dict(experiment_id=experiment_id,
                           limit=limit, offset=offset)
            return ResultSet(Dataset, url, response.json(), **filters)
        else:
            return ResultSet(Dataset, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Dataset")
    def get(dataset_id):
        """
        Get dataset with id dataset_id
        """
        url = config.url + "/api/v1/dataset/?format=json" + "&id=%s" % dataset_id
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        datasets_json = response.json()
        if datasets_json['meta']['total_count'] == 0:
            message = "Dataset matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Dataset)
        return Dataset(dataset_json=datasets_json['objects'][0])

    @staticmethod
    def create(experiment_id, description, instrument_id=None):
        """
        Create a dataset.
        """
        new_dataset_json = {
            "description": description,
            "experiments": ["/api/v1/experiment/%s/" % experiment_id],
            "immutable": False
        }
        if instrument_id:
            new_dataset_json['instrument'] = "/api/v1/instrument/%s/" % instrument_id
        url = config.url + "/api/v1/dataset/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_dataset_json))
        if response.status_code != 201:
            message = response.text
            raise Exception(message)
        dataset_json = response.json()
        return Dataset(dataset_json)

    @staticmethod
    def update(dataset_id, description):
        """
        Update an dataset record.
        """
        updated_fields_json = {'description': description}
        url = "%s/api/v1/dataset/%s/" % (config.url, dataset_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        dataset_json = response.json()
        return Dataset(dataset_json)
