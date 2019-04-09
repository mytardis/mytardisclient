"""
Model class for MyTardis API v1's DatasetResource.
"""
from __future__ import print_function

import logging

import requests
from six.moves import urllib

from ..conf import config
from ..utils import extend_url, add_filters

from .resultset import ResultSet
from .schema import Schema
from .schema import ParameterName
from .instrument import Instrument
from .model import Model

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Dataset(Model):
    """
    Model class for MyTardis API v1's DatasetResource.
    """
    def __init__(self, response_dict=None, include_metadata=False):
        self.response_dict = response_dict
        self.id = None  # pylint: disable=invalid-name
        self.description = None
        self.instrument = None
        self.experiments = []
        for key in self.__dict__:
            if key in response_dict:
                self.__dict__[key] = response_dict[key]
        if response_dict['instrument']:
            self.instrument = Instrument(response_dict['instrument'])
        self.parameter_sets = []
        if include_metadata:
            for dataset_param_set_json in response_dict['parameter_sets']:
                self.parameter_sets.append(
                    DatasetParameterSet(dataset_param_set_json))

    def __str__(self):
        """
        Return a string representation of a dataset
        """
        return "<%s: %s>" % (type(self).__name__, self.description)

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of datasets.

        :param filters: Filters, e.g. "experiments__id=123&description=Dataset Description"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Dataset` records, encapsulated in a
            `ResultSet` object.
        """
        url = "%s/api/v1/dataset/?format=json" % config.url

        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Dataset, url, response.json())

    @staticmethod
    def get(**kwargs):
        r"""
        Retrieve a single dataset record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the Dataset to retrieve

        :return: A :class:`Dataset` record.

        :raises requests.exceptions.HTTPError:
        """
        dataset_id = kwargs.get("id")
        if not dataset_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for Dataset get "
                "at this stage.")
        include_metadata = kwargs.get("include_metadata", False)
        url = "%s/api/v1/dataset/%s/?format=json" % (config.url, dataset_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return Dataset(response_dict=response.json(),
                       include_metadata=include_metadata)

    @staticmethod
    def create(experiment_id, description, instrument_id=None,
               params_file_json=None):
        """
        Create a dataset record.

        :param experiment_id: The ID of the experiment to create the
            dataset in.
        :param description: The description of the dataset.
        :param instrument_id: The instrument the data was collected on.
        :param params_file_json: Path to a JSON file with dataset
            parameters.

        :return: A new :class:`Dataset` record.
        """
        import json
        import os

        new_dataset_json = {
            "description": description,
            "experiments": ["/api/v1/experiment/%s/" % experiment_id],
            "immutable": False
        }
        if instrument_id:
            new_dataset_json['instrument'] = "/api/v1/instrument/%s/" \
                % instrument_id
        if params_file_json:
            assert os.path.exists(params_file_json)
            with open(params_file_json) as params_file:
                new_dataset_json['parameter_sets'] = json.load(params_file)
        url = "%s/api/v1/dataset/" % config.url
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_dataset_json))
        response.raise_for_status()
        return Dataset(response.json())

    @staticmethod
    def update(dataset_id, description):
        """
        Update an dataset record.
        """
        import json

        updated_fields_json = {'description': description}
        url = "%s/api/v1/dataset/%s/" % (config.url, dataset_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        response.raise_for_status()
        dataset_json = response.json()
        return Dataset(dataset_json)

    @staticmethod
    def download(dataset_id):
        """
        Download a dataset
        """
        import os
        from .datafile import DataFile

        dataset = Dataset.objects.get(id=dataset_id)
        path = urllib.parse.quote(
            dataset.description.encode('utf-8'), safe=" ,")
        if os.path.exists(path):
            from ..utils.confirmation import query_yes_no
            if not query_yes_no("Overwrite '%s/'?" % path):
                return
        else:
            os.makedirs(path)
        print("Downloading to: %s/" % path)
        for datafile in DataFile.objects.filter(dataset__id=dataset_id).order_by('id'):
            DataFile.download(datafile.id, basedir=path)
        print("Downloaded to: %s/" % path)


class DatasetParameterSet(object):
    """
    Model class for MyTardis API v1's DatasetParameterSetResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        self.dataset = response_dict['dataset']
        self.schema = Schema(response_dict['schema'])
        self.parameters = []
        for dataset_param_json in response_dict['parameters']:
            self.parameters.append(DatasetParameter(dataset_param_json))

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of dataset parameters.

        :param filters: Filters, e.g. "datasets__id=123"

        :return: A list of :class:`DatasetParameterSet` records,
            encapsulated in a `ResultSet` object`.
        """
        url = "%s/api/v1/datasetparameterset/?format=json" % config.url
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(DatasetParameterSet, url, response.json())


class DatasetParameter(object):
    """
    Model class for MyTardis API v1's DatasetParameterResource.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, response_dict):
        self.response_dict = response_dict
        self.id = response_dict['id']  # pylint: disable=invalid-name
        pname_id = response_dict['name'].split('/')[-2]
        self.name = ParameterName.objects.get(id=pname_id)
        self.string_value = response_dict['string_value']
        self.numerical_value = response_dict['numerical_value']
        self.datetime_value = response_dict['datetime_value']
        self.link_id = response_dict['link_id']
        self.value = response_dict['value']

    @staticmethod
    def list(filters=None, limit=None, offset=None, order_by=None):
        """
        List dataset parameter records in parameter set.
        """
