"""
Views for MyTardis records
"""
from __future__ import print_function

import json
from texttable import Texttable

from ..models.api import ApiEndpoints, ApiSchema
from ..models.facility import Facility
from ..models.instrument import Instrument
from ..models.experiment import Experiment
from ..models.dataset import Dataset
from ..models.datafile import DataFile
from ..models.storagebox import StorageBox
from ..models.schema import Schema
from ..models.resultset import ResultSet

from .api import render_api_endpoints, render_api_schema
from .facility import render_facility, render_facilities
from .instrument import render_instrument, render_instruments
from .experiment import render_experiment, render_experiments
from .dataset import render_dataset, render_datasets
from .datafile import render_datafile, render_datafiles
from .storagebox import render_storage_box, render_storage_boxes
from .schema import render_schema, render_schemas


def render(data, render_format='table', display_heading=True):
    """
    Generic render function.

    Calls a more specific render function depending on the data type
    to display (render) the data in the desired format.

    :param data: The data to be displayed.  An instance of a model class
        (e.g.  :class:`mtclient.models.dataset.Dataset`) or an instance of
        :class:`mtclient.models.resultset.ResultSet`
        or an instance of :class:`mtclient.models.api.ApiEndpoints`.
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for a
        `ResultSet` containing multiple records, setting
        `display_heading` to True ensures that the meta information
        returned by the query is summarized in a 'heading' before
        displaying the table.  This meta information can be used to
        determine whether the query results have been truncated due
        to pagination.
    """
    if data.__class__ == ResultSet:
        return render_result_set(data, render_format, display_heading)
    if data.__class__ == ApiEndpoints:
        return render_api_endpoints(data, render_format, display_heading)
    return render_single_record(data, render_format)


def render_single_record(data, render_format):
    """
    Render single record.

    Calls a more specific render function depending on the data type
    to display (render) the data in the desired format.

    :param data: The data to be displayed.  An instance of a model class
        (e.g.  :class:`mtclient.models.dataset.Dataset`).
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if not data:
        return ""
    renderers = dict(
        ApiSchema=render_api_schema,
        Facility=render_facility,
        Instrument=render_instrument,
        Experiment=render_experiment,
        Dataset=render_dataset,
        DataFile=render_datafile,
        StorageBox=render_storage_box,
        Schema=render_schema)
    data_type = data.__class__.__name__
    if data_type not in renderers:
        raise NotImplementedError("Unexpected data type: %s" % data_type)
    return renderers[data_type](data, render_format)


def render_result_set(result_set, render_format, display_heading=True):
    """
    Render result set.

    Calls a more specific render function depending on the type of data
    stored within the `ResultSet` to display (render) the data in the
    desired format.

    :param result_set: The result set to be rendered.
    :type result_set: :class:`mtclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for a
        `ResultSet` containing multiple records, setting
        `display_heading` to True ensures that the meta information
        returned by the query is summarized in a 'heading' before
        displaying the table.  This meta information can be used to
        determine whether the query results have been truncated due
        to pagination.
    """
    renderers = dict(
        Facility=render_facilities,
        Instrument=render_instruments,
        Experiment=render_experiments,
        Dataset=render_datasets,
        DataFile=render_datafiles,
        StorageBox=render_storage_boxes,
        Schema=render_schemas)
    data_type = result_set.model.__name__
    if data_type not in renderers:
        raise NotImplementedError("Unexpected data type: %s" % data_type)
    return renderers[data_type](result_set, render_format, display_heading)
