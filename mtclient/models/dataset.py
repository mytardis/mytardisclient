"""
Model class for MyTardis API v1's DatasetResource.
"""
from __future__ import print_function

import logging

import requests

from ..conf import config
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
    def __init__(self, dataset_json=None, include_metadata=False):
        self.json = dataset_json
        self.id = None  # pylint: disable=invalid-name
        self.description = None
        self.instrument = None
        self.experiments = []
        self.parameter_sets = []
        if dataset_json:
            for key in self.__dict__:
                if key in dataset_json:
                    self.__dict__[key] = dataset_json[key]
            if dataset_json['instrument']:
                self.instrument = Instrument(dataset_json['instrument'])
            if include_metadata:
                self.parameter_sets = []
                for dataset_param_set_json in dataset_json['parameter_sets']:
                    self.parameter_sets.append(
                        DatasetParameterSet(dataset_param_set_json))

    def __str__(self):
        """
        Return a string representation of a dataset
        """
        return "<%s: %s>" % (type(self).__name__, self.description)

    @staticmethod
    @config.region.cache_on_arguments(namespace="Dataset")
    def list(experiment_id=None, filters=None,
             limit=None, offset=None, order_by=None):
        """
        Retrieve a list of datasets.

        :param experiment_id: The ID of an experiment to retrieve datasets from.
        :param filters: Filters, e.g. "description=Dataset Description"
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Dataset` records, encapsulated in a
            `ResultSet` object.
        """
        from ..utils import extend_url, add_filters

        url = "%s/api/v1/dataset/?format=json" % config.url

        if experiment_id:
            url += "&experiments__id=%s"  % experiment_id
        url = add_filters(url, filters)
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Dataset, url, response.json())

    @staticmethod
    @config.region.cache_on_arguments(namespace="Dataset")
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
        from ..utils.exceptions import DoesNotExist

        dataset_id = kwargs.get("id")
        if not dataset_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for Dataset get "
                "at this stage.")
        include_metadata = kwargs.get("include_metadata", False)
        url = config.url + "/api/v1/dataset/?format=json" + "&id=%s" % dataset_id
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        datasets_json = response.json()
        if datasets_json['meta']['total_count'] == 0:
            message = "Dataset matching filter doesn't exist."
            raise DoesNotExist(message, url, response, Dataset)
        return Dataset(dataset_json=datasets_json['objects'][0],
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
        url = config.url + "/api/v1/dataset/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_dataset_json))
        response.raise_for_status()
        dataset_json = response.json()
        return Dataset(dataset_json)

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


class DatasetParameterSet(object):
    """
    Model class for MyTardis API v1's DatasetParameterSetResource.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, dataset_paramset_json):
        self.json = dataset_paramset_json
        self.id = dataset_paramset_json['id']  # pylint: disable=invalid-name
        self.dataset = dataset_paramset_json['dataset']
        self.schema = Schema(dataset_paramset_json['schema'])
        self.parameters = []
        for dataset_param_json in dataset_paramset_json['parameters']:
            self.parameters.append(DatasetParameter(dataset_param_json))

    @staticmethod
    @config.region.cache_on_arguments(namespace="DatasetParameterSet")
    def list(dataset_id):
        """
        List dataset parameter sets associated with dataset ID
        dataset_id.

        :param dataset_id: The ID of the dataset to retrieve parameter
            sets for.

        :return: A list of :class:`DatasetParameterSet` records,
            encapsulated in a `ResultSet` object`.
        """
        url = "%s/api/v1/datasetparameterset/?format=json" % config.url
        url += "&datasets__id=%s"  % dataset_id
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(DatasetParameterSet, url, response.json())


class DatasetParameter(object):
    """
    Model class for MyTardis API v1's DatasetParameterResource.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, dataset_param_json):
        self.json = dataset_param_json
        self.id = dataset_param_json['id']  # pylint: disable=invalid-name
        self.name = ParameterName.get(dataset_param_json['name'].split('/')[-2])
        self.string_value = dataset_param_json['string_value']
        self.numerical_value = dataset_param_json['numerical_value']
        self.datetime_value = dataset_param_json['datetime_value']
        self.link_id = dataset_param_json['link_id']
        self.value = dataset_param_json['value']

    @staticmethod
    @config.region.cache_on_arguments(namespace="DatasetParameter")
    def list(dataset_param_set):
        """
        List dataset parameter records in parameter set.
        """
