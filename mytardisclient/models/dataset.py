"""
Model class for MyTardis API v1's DatasetResource.
See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
"""

import requests
import json

from .resultset import ResultSet
from .instrument import Instrument
# from mytardisclient.logs import logger
from mytardisclient.utils.exceptions import DoesNotExist


class Dataset(object):
    """
    Model class for MyTardis API v1's DatasetResource.
    See: https://github.com/mytardis/mytardis/blob/3.7/tardis/tardis_portal/api.py
    """
    def __init__(self, config, dataset_json):
        self.config = config
        self.json = dataset_json
        self.id = dataset_json['id']  # pylint: disable=invalid-name
        self.description = dataset_json['description']
        if dataset_json['instrument']:
            self.instrument = Instrument(config, dataset_json['instrument'])
        else:
            self.instrument = None
        self.experiments = dataset_json['experiments']

    @staticmethod
    def list(config, experiment_id=None,
             limit=None, offset=None, order_by=None):
        """
        Get datasets I have access to
        """
        url = "%s/api/v1/dataset/?format=json" % config.mytardis_url
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
            return ResultSet(Dataset, config, url, response.json(), **filters)
        else:
            return ResultSet(Dataset, config, url, response.json())

    @staticmethod
    def get(config, exp_id):
        """
        Get dataset with id exp_id
        """
        url = config.mytardis_url + "/api/v1/dataset/?format=json" + "&id=%s" % exp_id
        response = requests.get(url=url, headers=config.default_headers)
        if response.status_code != 200:
            message = response.text
            raise Exception(message)

        datasets_json = response.json()
        if datasets_json['meta']['total_count'] == 0:
            message = "Dataset matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Dataset)
        return Dataset(config=config, dataset_json=datasets_json['objects'][0])

    @staticmethod
    def create(config, experiment_id, description, instrument_id=None):
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
        url = config.mytardis_url + "/api/v1/dataset/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_dataset_json))
        if response.status_code != 201:
            message = response.text
            raise Exception(message)
        dataset_json = response.json()
        return Dataset(config, dataset_json)

    @staticmethod
    def update(config, dataset_id, description):
        """
        Update an dataset record.
        """
        updated_fields_json = {'description': description}
        url = "%s/api/v1/dataset/%s/" % \
            (config.mytardis_url, dataset_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        if response.status_code != 202:
            print "HTTP %s" % response.status_code
            message = response.text
            raise Exception(message)
        dataset_json = response.json()
        return Dataset(config, dataset_json)
