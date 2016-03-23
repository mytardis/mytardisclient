"""
Views for MyTardis records.
"""
# pylint: disable=too-many-lines

from __future__ import print_function

import json
from texttable import Texttable

from mytardisclient.models.api import ApiEndpoints
from mytardisclient.models.api import ApiSchema
from mytardisclient.models.facility import Facility
from mytardisclient.models.instrument import Instrument
from mytardisclient.models.experiment import Experiment
from mytardisclient.models.dataset import Dataset
from mytardisclient.models.datafile import DataFile
from mytardisclient.models.storagebox import StorageBox
from mytardisclient.models.schema import Schema
from mytardisclient.models.resultset import ResultSet
from mytardisclient.utils import human_readable_size_string


def render(data, render_format='table', display_heading=True):
    """
    Generic render function.

    Calls a more specific render function depending on the data type
    to display (render) the data in the desired format.

    :param data: The data to be displayed.  An instance of a model class
        (e.g.  :class:`mytardisclient.models.dataset.Dataset`) or an instance of
        :class:`mytardisclient.models.resultset.ResultSet`
        or an instance of :class:`mytardisclient.models.api.ApiEndpoints`.
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
    elif data.__class__ == ApiEndpoints:
        return render_api_endpoints(data, render_format, display_heading)
    else:
        return render_single_record(data, render_format)


def render_single_record(data, render_format):
    """
    Render single record.

    Calls a more specific render function depending on the data type
    to display (render) the data in the desired format.

    :param data: The data to be displayed.  An instance of a model class
        (e.g.  :class:`mytardisclient.models.dataset.Dataset`).
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    # pylint: disable=too-many-return-statements
    if data.__class__ == ApiSchema:
        return render_api_schema(data, render_format)
    elif data.__class__ == Facility:
        return render_facility(data, render_format)
    elif data.__class__ == Instrument:
        return render_instrument(data, render_format)
    elif data.__class__ == Experiment:
        return render_experiment(data, render_format)
    elif data.__class__ == Dataset:
        return render_dataset(data, render_format)
    elif data.__class__ == DataFile:
        return render_datafile(data, render_format)
    elif data.__class__ == StorageBox:
        return render_storage_box(data, render_format)
    elif data.__class__ == Schema:
        return render_schema(data, render_format)
    else:
        print("Class is " + data.__class__.__name__)


def render_result_set(result_set, render_format, display_heading=True):
    """
    Render result set.

    Calls a more specific render function depending on the type of data
    stored within the `ResultSet` to display (render) the data in the
    desired format.

    :param result_set: The result set to be rendered.
    :type result_set: :class:`mytardisclient.models.resultset.ResultSet`
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
    # pylint: disable=too-many-return-statements
    if result_set.model == Facility:
        return render_facilities(result_set, render_format, display_heading)
    elif result_set.model == Instrument:
        return render_instruments(result_set, render_format, display_heading)
    elif result_set.model == Experiment:
        return render_experiments(result_set, render_format, display_heading)
    elif result_set.model == Dataset:
        return render_datasets(result_set, render_format, display_heading)
    elif result_set.model == DataFile:
        return render_datafiles(result_set, render_format, display_heading)
    elif result_set.model == StorageBox:
        return render_storage_boxes(result_set, render_format, display_heading)
    elif result_set.model == Schema:
        return render_schemas(result_set, render_format, display_heading)
    else:
        print("Class is " + result_set.model.__name__)


def render_api_schema(api_schema, render_format):
    """
    Render API schema

    :param api_schema: The API schema model to be displayed.
    :type api_schema: :class:`mytardisclient.models.api.ApiSchema`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_api_schema_as_json(api_schema)
    else:
        return render_api_schema_as_table(api_schema)


def render_api_schema_as_json(api_schema, indent=2, sort_keys=True):
    """
    Returns JSON representation of API schema.

    :param api_schema: The API schema model to be displayed.
    :type api_schema: :class:`mytardisclient.models.api.ApiSchema`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(api_schema.json, indent=indent, sort_keys=sort_keys)


def render_api_schema_as_table(api_schema):
    """
    Returns ASCII table view of API schema.

    :param api_schema: The API schema model to be displayed.
    :type api_schema: :class:`mytardisclient.models.api.ApiSchema`
    """
    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(["t", "t"])
    table.header(["API Schema field", "Value"])
    table.add_row(["Model", api_schema.model])
    table.add_row(["Fields",
                   "\n".join(sorted([field for field in api_schema.fields]))])
    table.add_row(["Filtering",
                   json.dumps(api_schema.filtering, indent=2, sort_keys=True)])
    table.add_row(["Ordering",
                   json.dumps(api_schema.ordering, indent=2, sort_keys=True)])
    return table.draw() + "\n"


def render_api_endpoints(api_endpoints, render_format, display_heading=True):
    """
    Render API endpoints

    :param api_endpoints: The API endpoints to be rendered.
    :type api_endpoints: :class:`mytardisclient.models.api.ApiEndpoints`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for
        an `ApiEndpoints` set, setting `display_heading` to True
        ensures that a heading is displayed before the results table.
        The heading includes the URL resolved to perform the query.
    """
    if render_format == 'json':
        return render_api_endpoints_as_json(api_endpoints)
    else:
        return render_api_endpoints_as_table(api_endpoints, display_heading)


def render_api_endpoints_as_json(api_endpoints, indent=2, sort_keys=True):
    """
    Returns JSON representation of api_endpoints.

    :param api_endpoints: The API endpoints to be rendered.
    :type api_endpoints: :class:`mytardisclient.models.api.ApiEndpoints`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(api_endpoints.json, indent=indent, sort_keys=sort_keys)


def render_api_endpoints_as_table(api_endpoints, display_heading=True):
    """
    Returns ASCII table view of api_endpoints.

    :param api_endpoints: The API endpoints to be rendered.
    :type api_endpoints: :class:`mytardisclient.models.api.ApiEndpoints`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for
        an `ApiEndpoints` set, setting `display_heading` to True
        ensures that a heading is displayed before the results table.
        The heading includes the URL resolved to perform the query.
    """
    heading = "\n" \
        "API Endpoints\n" if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["l", 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(["Model", "List Endpoint", "Schema"])
    for api_endpoint in api_endpoints:
        table.add_row([api_endpoint.model, api_endpoint.list_endpoint,
                       api_endpoint.schema])
    return heading + table.draw() + "\n"


def render_facility(facility, render_format, display_heading=True):
    """
    Render facility

    :param facility: The facility to be rendered.
    :type facility: :class:`mytardisclient.models.facility.Facility`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for
        an `ApiEndpoints` set, setting `display_heading` to True
        ensures that a heading is displayed before the results table.
        The heading includes the URL resolved to perform the query.
    """
    if render_format == 'json':
        return render_facility_as_json(facility)
    else:
        return render_facility_as_table(facility, display_heading)


def render_facility_as_json(facility, indent=2, sort_keys=True):
    """
    Returns JSON representation of facility.

    :param facility: The facility to be rendered.
    :type facility: :class:`mytardisclient.models.facility.Facility`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(facility.json, indent=indent, sort_keys=sort_keys)


def render_facility_as_table(facility, display_heading=True):
    """
    Returns ASCII table view of facility.

    :param facility: The facility to be rendered.
    :type facility: :class:`mytardisclient.models.facility.Facility`
    :param display_heading: When using the 'table' render format for
        an `ApiEndpoints` set, setting `display_heading` to True
        ensures that a heading is displayed before the results table.
        The heading includes the URL resolved to perform the query.
    """
    heading = "\nModel: Facility\n\n" if display_heading else ""

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Facility field", "Value"])
    table.add_row(["ID", facility.id])
    table.add_row(["Name", facility.name])
    table.add_row(["Manager Group", facility.manager_group])
    return heading + table.draw() + "\n"


def render_facilities(facilities, render_format, display_heading=True):
    """
    Render facilities

    :param facilities: The `ResultSet` of facilities to be rendered.
    :type facilities: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_facilities_as_json(facilities)
    else:
        return render_facilities_as_table(facilities, display_heading)


def render_facilities_as_json(facilities, indent=2, sort_keys=True):
    """
    Returns JSON representation of facilities.

    :param facilities: The result set of facilities to be displayed.
    :type facilities: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(facilities.json, indent=indent, sort_keys=sort_keys)


def render_facilities_as_table(facilities, display_heading=True):
    """
    Returns ASCII table view of facilities.

    :param facilities: The facilities to be rendered.
    :type facilities: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: Facility\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (facilities.url, facilities.total_count,
           facilities.limit, facilities.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(["ID", "Name", "Manager Group"])
    for facility in facilities:
        table.add_row([facility.id, facility.name, facility.manager_group])
    return heading + table.draw() + "\n"


def render_instrument(instrument, render_format):
    """
    Render instrument

    :param instrument: The instrument to be rendered.
    :type instrument: :class:`mytardisclient.models.instrument.Instrument`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_instrument_as_json(instrument)
    else:
        return render_instrument_as_table(instrument)


def render_instrument_as_json(instrument, indent=2, sort_keys=True):
    """
    Returns JSON representation of instrument.

    :param instrument: The instrument to be rendered.
    :type instrument: :class:`mytardisclient.models.instrument.Instrument`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(instrument.json, indent=indent, sort_keys=sort_keys)


def render_instrument_as_table(instrument):
    """
    Returns ASCII table view of instrument.

    :param instrument: The instrument to be rendered.
    :type instrument: :class:`mytardisclient.models.instrument.Instrument`
    """
    instrument_table = Texttable()
    instrument_table.set_cols_align(['l', 'l'])
    instrument_table.set_cols_valign(['m', 'm'])
    instrument_table.header(["Instrument field", "Value"])
    instrument_table.add_row(["ID", instrument.id])
    instrument_table.add_row(["Name", instrument.name])
    instrument_table.add_row(["Facility", instrument.facility])
    return instrument_table.draw() + "\n"


def render_instruments(instruments, render_format, display_heading=True):
    """
    Render instruments

    :param instruments: The `ResultSet` of instruments to be rendered.
    :type instruments: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_instruments_as_json(instruments)
    else:
        return render_instruments_as_table(instruments, display_heading)


def render_instruments_as_json(instruments, indent=2, sort_keys=True):
    """
    Returns JSON representation of instruments.

    :param instruments: The result set of instruments to be displayed.
    :type instruments: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(instruments.json, indent=indent, sort_keys=sort_keys)


def render_instruments_as_table(instruments, display_heading=True):
    """
    Returns ASCII table view of instruments.

    :param instruments: The instruments to be rendered.
    :type instruments: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: Instrument\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (instruments.url, instruments.total_count,
           instruments.limit, instruments.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(["ID", "Name", "Facility"])
    for instrument in instruments:
        table.add_row([instrument.id, instrument.name, instrument.facility])
    return heading + table.draw() + "\n"


def render_experiment(experiment, render_format):
    """
    Render experiment

    :param experiment: The experiment to be rendered.
    :type experiment: :class:`mytardisclient.models.experiment.Experiment`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_experiment_as_json(experiment)
    else:
        return render_experiment_as_table(experiment)


def render_experiment_as_json(experiment, indent=2, sort_keys=True):
    """
    Returns JSON representation of experiment.

    :param experiment: The experiment to be rendered.
    :type experiment: :class:`mytardisclient.models.experiment.Experiment`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(experiment.json, indent=indent, sort_keys=sort_keys)


def render_experiment_as_table(experiment):
    """
    Returns ASCII table view of experiment.

    :param experiment: The experiment to be rendered.
    :type experiment: :class:`mytardisclient.models.experiment.Experiment`
    """
    exp_and_param_sets = ""

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Experiment field", "Value"])
    table.add_row(["ID", experiment.id])
    table.add_row(["Institution", experiment.institution_name])
    table.add_row(["Title", experiment.title])
    table.add_row(["Description", experiment.description])
    exp_and_param_sets += table.draw() + "\n"

    for exp_param_set in experiment.parameter_sets:
        exp_and_param_sets += "\n"
        table = Texttable(max_width=0)
        table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l'])
        table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm'])
        table.header(["ExperimentParameter ID", "Schema", "Parameter Name",
                      "String Value", "Numerical Value", "Datetime Value",
                      "Link ID"])
        for exp_param in exp_param_set.parameters:
            table.add_row([exp_param.id,
                           exp_param.name.schema,
                           exp_param.name,
                           exp_param.string_value,
                           exp_param.numerical_value or '',
                           exp_param.datetime_value or '',
                           exp_param.link_id or ''])
        exp_and_param_sets += table.draw() + "\n"

    return exp_and_param_sets


def render_experiments(experiments, render_format, display_heading=True):
    """
    Render experiments

    :param experiments: The `ResultSet` of experiments to be rendered.
    :type experiments: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_experiments_as_json(experiments)
    else:
        return render_experiments_as_table(experiments, display_heading)


def render_experiments_as_json(experiments, indent=2, sort_keys=True):
    """
    Returns JSON representation of experiments.

    :param experiments: The result set of experiments to be displayed.
    :type experiments: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(experiments.json, indent=indent, sort_keys=sort_keys)


def render_experiments_as_table(experiments, display_heading=True):
    """
    Returns ASCII table view of experiments.

    :param experiments: The experiments to be rendered.
    :type experiments: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: Experiment\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (experiments.url, experiments.total_count,
           experiments.limit, experiments.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(["ID", "Institution", "Title"])
    for experiment in experiments:
        table.add_row([experiment.id, experiment.institution_name,
                       experiment.title])
    return heading + table.draw() + "\n"


def render_dataset(dataset, render_format):
    """
    Render dataset

    :param dataset: The dataset to be rendered.
    :type dataset: :class:`mytardisclient.models.dataset.Dataset`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_dataset_as_json(dataset)
    else:
        return render_dataset_as_table(dataset)


def render_dataset_as_json(dataset, indent=2, sort_keys=True):
    """
    Returns JSON representation of dataset.

    :param dataset: The dataset to be rendered.
    :type dataset: :class:`mytardisclient.models.dataset.Dataset`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(dataset.json, indent=indent, sort_keys=sort_keys)


def render_dataset_as_table(dataset):
    """
    Returns ASCII table view of dataset.

    :param dataset: The dataset to be rendered.
    :type dataset: :class:`mytardisclient.models.dataset.Dataset`
    """
    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Dataset field", "Value"])
    table.add_row(["ID", dataset.id])
    table.add_row(["Experiment(s)", "\n".join(dataset.experiments)])
    table.add_row(["Description", dataset.description])
    table.add_row(["Instrument", dataset.instrument])
    dataset_and_param_sets = table.draw() + "\n"

    for dataset_param_set in dataset.parameter_sets:
        dataset_and_param_sets += "\n"
        table = Texttable(max_width=0)
        table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l'])
        table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm'])
        table.header(["DatasetParameter ID", "Schema", "Parameter Name",
                      "String Value", "Numerical Value", "Datetime Value",
                      "Link ID"])
        for dataset_param in dataset_param_set.parameters:
            table.add_row([dataset_param.id,
                           dataset_param.name.schema,
                           dataset_param.name,
                           dataset_param.string_value,
                           dataset_param.numerical_value or '',
                           dataset_param.datetime_value or '',
                           dataset_param.link_id or ''])
        dataset_and_param_sets += table.draw() + "\n"

    return dataset_and_param_sets


def render_datasets(datasets, render_format, display_heading=True):
    """
    Render datasets

    :param datasets: The `ResultSet` of datasets to be rendered.
    :type datasets: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_datasets_as_json(datasets)
    else:
        return render_datasets_as_table(datasets, display_heading)


def render_datasets_as_json(datasets, indent=2, sort_keys=True):
    """
    Returns JSON representation of datasets.

    :param datasets: The result set of datasets to be displayed.
    :type datasets: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(datasets.json, indent=indent, sort_keys=sort_keys)


def render_datasets_as_table(datasets, display_heading=True):
    """
    Returns ASCII table view of datasets.

    :param datasets: The datasets to be rendered.
    :type datasets: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: Dataset\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (datasets.url, datasets.total_count,
           datasets.limit, datasets.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm'])
    table.header(["Dataset ID", "Experiment(s)", "Description", "Instrument"])
    for dataset in datasets:
        table.add_row([dataset.id, "\n".join(dataset.experiments),
                       dataset.description, dataset.instrument])
    return heading + table.draw() + "\n"


def render_datafile(datafile, render_format):
    """
    Render datafile

    :param datafile: The datafile to be rendered.
    :type datafile: :class:`mytardisclient.models.datafile.DataFile`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_datafile_as_json(datafile)
    else:
        return render_datafile_as_table(datafile)


def render_datafile_as_json(datafile, indent=2, sort_keys=True):
    """
    Returns JSON representation of datafile.

    :param datafile: The datafile to be rendered.
    :type datafile: :class:`mytardisclient.models.datafile.DataFile`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(datafile.json, indent=indent, sort_keys=sort_keys)


def render_datafile_as_table(datafile):
    """
    Returns ASCII table view of datafile.

    :param datafile: The datafile to be rendered.
    :type datafile: :class:`mytardisclient.models.datafile.DataFile`
    """
    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["DataFile field", "Value"])
    table.add_row(["ID", datafile.id])
    table.add_row(["Dataset", datafile.dataset])
    locations = [replica.location for replica in datafile.replicas]
    table.add_row(["Storage Box", "\n".join(locations)])
    table.add_row(["Directory", datafile.directory])
    table.add_row(["Filename", datafile.filename])
    uris = [replica.uri for replica in datafile.replicas]
    table.add_row(["URI", "\n".join(uris)])
    table.add_row(["Verified", str(datafile.verified)])
    table.add_row(["Size", human_readable_size_string(datafile.size)])
    table.add_row(["MD5 Sum", datafile.md5sum])
    datafile_and_param_sets = table.draw() + "\n"

    for datafile_param_set in datafile.parameter_sets:
        datafile_and_param_sets += "\n"
        table = Texttable(max_width=0)
        table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l'])
        table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm'])
        table.header(["DataFileParameter ID", "Schema", "Parameter Name",
                      "String Value", "Numerical Value", "Datetime Value",
                      "Link ID"])
        for datafile_param in datafile_param_set.parameters:
            table.add_row([datafile_param.id,
                           datafile_param.name.schema,
                           datafile_param.name,
                           datafile_param.string_value,
                           datafile_param.numerical_value or '',
                           datafile_param.datetime_value or '',
                           datafile_param.link_id or ''])
        datafile_and_param_sets += table.draw() + "\n"

    return datafile_and_param_sets


def render_datafiles(datafiles, render_format, display_heading=True):
    """
    Render datafiles

    :param datafiles: The `ResultSet` of datafiles to be rendered.
    :type datafiles: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_datafiles_as_json(datafiles)
    else:
        return render_datafiles_as_table(datafiles, display_heading)


def render_datafiles_as_json(datafiles, indent=2, sort_keys=True):
    """
    Returns JSON representation of datafiles.

    :param datafiles: The result set of datafiles to be displayed.
    :type datafiles: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(datafiles.json, indent=indent, sort_keys=sort_keys)


def render_datafiles_as_table(datafiles, display_heading=True):
    """
    Returns ASCII table view of datafiles.

    :param datafiles: The datafiles to be rendered.
    :type datafiles: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: DataFile\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (datafiles.url, datafiles.total_count, datafiles.limit,
           datafiles.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm'])
    table.header(["DataFile ID", "Filename", "Storage Box",
                  "URI", "Verified", "Size", "MD5 Sum"])
    for datafile in datafiles:
        uris = [replica.uri for replica in datafile.replicas]
        locations = [replica.location for replica in datafile.replicas]
        table.add_row([datafile.id, datafile.filename, "\n".join(locations),
                       "\n".join(uris), str(datafile.verified),
                       human_readable_size_string(datafile.size),
                       datafile.md5sum])
    return heading + table.draw() + "\n"


def render_storage_box(storage_box, render_format):
    """
    Render storage box

    :param storage_box: The storage box to be rendered.
    :type storage_box: :class:`mytardisclient.models.storagebox.StorageBox`
    """
    if render_format == 'json':
        return render_storage_box_as_json(storage_box)
    else:
        return render_storage_box_as_table(storage_box)


def render_storage_box_as_json(storage_box, indent=2, sort_keys=True):
    """
    Returns JSON representation of storage_box.

    :param storage_box: The storage box to be rendered.
    :type storage_box: :class:`mytardisclient.models.storagebox.StorageBox`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(storage_box.json, indent=indent, sort_keys=sort_keys)


def render_storage_box_as_table(storage_box):
    """
    Returns ASCII table view of storage_box.
    """
    storage_box_options_attributes = ""

    table = Texttable(max_width=0)
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["StorageBox field", "Value"])
    table.add_row(["ID", storage_box.id])
    table.add_row(["Name", storage_box.name])
    table.add_row(["Description", storage_box.description])
    table.add_row(["Django Storage Class", storage_box.django_storage_class])
    table.add_row(["Max Size", storage_box.max_size])
    table.add_row(["Status", storage_box.status])
    storage_box_options_attributes += table.draw() + "\n"

    storage_box_options_attributes += "\n"
    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["StorageBoxOption Key", "StorageBoxOption Value"])
    for option in storage_box.options:
        table.add_row([option.key, option.value])
    storage_box_options_attributes += table.draw() + "\n"

    storage_box_options_attributes += "\n"
    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["StorageBoxAttribute Key", "StorageBoxAttribute Value"])
    for attribute in storage_box.attributes:
        table.add_row([attribute.key, attribute.value])
    storage_box_options_attributes += table.draw() + "\n"

    return storage_box_options_attributes


def render_storage_boxes(storage_boxes, render_format, display_heading=True):
    """
    Render storage boxes.

    :param storage_boxes: The `ResultSet` of storage boxes to be rendered.
    :type storage_boxes: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_storage_boxes_as_json(storage_boxes)
    else:
        return render_storage_boxes_as_table(storage_boxes, display_heading)


def render_storage_boxes_as_json(storage_boxes, indent=2, sort_keys=True):
    """
    Returns JSON representation of storage_boxes.

    :param storage_boxes: The result set of storage boxes to be displayed.
    :type storage_boxes: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(storage_boxes.json, indent=indent, sort_keys=sort_keys)


def render_storage_boxes_as_table(storage_boxes, display_heading=True):
    """
    Returns ASCII table view of storage_boxes.

    :param storage_boxes: The storage boxes to be rendered.
    :type storage_boxes: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: StorageBox\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (storage_boxes.url, storage_boxes.total_count,
           storage_boxes.limit,
           storage_boxes.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(["ID", "Name", "Description"])
    for storage_box in storage_boxes:
        table.add_row([storage_box.id, storage_box.name,
                       storage_box.description])
    return heading + table.draw() + "\n"


def render_schema(schema, render_format):
    """
    Render schema

    :param schema: The schema to be rendered.
    :type schema: :class:`mytardisclient.models.schema.Schema`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_schema_as_json(schema)
    else:
        return render_schema_as_table(schema)


def render_schema_as_json(schema, indent=2, sort_keys=True):
    """
    Returns JSON representation of schema.

    :param schema: The schema to be rendered.
    :type schema: :class:`mytardisclient.models.schema.Schema`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(schema.json, indent=indent, sort_keys=sort_keys)


def render_schema_as_table(schema):
    """
    Returns ASCII table view of schema.

    :param schema: The schema to be rendered.
    :type schema: :class:`mytardisclient.models.schema.Schema`
    """
    schema_parameter_names = ""

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Schema field", "Value"])
    table.add_row(["ID", schema.id])
    table.add_row(["Name", schema.name])
    table.add_row(["Namespace", schema.namespace])
    table.add_row(["Type", schema.type])
    table.add_row(["Subtype", schema.subtype])
    table.add_row(["Immutable", str(bool(schema.immutable))])
    table.add_row(["Hidden", str(bool(schema.hidden))])
    schema_parameter_names += table.draw() + "\n"

    schema_parameter_names += "\n"
    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'])
    table.header(["ParameterName ID", "Full Name", "Name", "Data Type",
                  "Units", "Immutable", "Is Searchable", "Order", "Choices",
                  "Comparison Type"])
    for parameter_name in schema.parameter_names:
        table.add_row([parameter_name.id,
                       parameter_name.full_name.encode('utf8', 'ignore'),
                       parameter_name.name, parameter_name.data_type,
                       parameter_name.units.encode('utf8', 'ignore'),
                       str(bool(parameter_name.immutable)),
                       str(bool(parameter_name.is_searchable)),
                       parameter_name.order,
                       parameter_name.choices,
                       parameter_name.comparison_type])
    schema_parameter_names += table.draw() + "\n"

    return schema_parameter_names


def render_schemas(schemas, render_format, display_heading=True):
    """
    Render schemas

    :param schemas: The `ResultSet` of schemas to be rendered.
    :type schemas: :class:`mytardisclient.models.resultset.ResultSet`
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
    if render_format == 'json':
        return render_schemas_as_json(schemas)
    else:
        return render_schemas_as_table(schemas, display_heading)


def render_schemas_as_json(schemas, indent=2, sort_keys=True):
    """
    Returns JSON representation of schemas.

    :param schemas: The result set of schemas boxes to be displayed.
    :type schemas: :class:`mytardisclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(schemas.json, indent=indent, sort_keys=sort_keys)


def render_schemas_as_table(schemas, display_heading=True):
    """
    Returns ASCII table view of schemas.

    :param schemas: The schemas to be rendered.
    :type schemas: :class:`mytardisclient.models.resultset.ResultSet`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: Setting `display_heading` to True ensures
        that the meta information returned by the query is summarized
        in a 'heading' before displaying the table.  This meta
        information can be used to determine whether the query results
        have been truncated due to pagination.
    """
    heading = "\n" \
        "Model: Schema\n" \
        "Query: %s\n" \
        "Total Count: %s\n" \
        "Limit: %s\n" \
        "Offset: %s\n\n" \
        % (schemas.url, schemas.total_count,
           schemas.limit, schemas.offset) if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm'])
    table.header(["ID", "Name", "Namespace", "Type", "Subtype", "Immutable",
                  "Hidden"])
    for schema in schemas:
        table.add_row([schema.id, schema.name, schema.namespace,
                       schema.type, schema.subtype or '',
                       str(bool(schema.immutable)), str(bool(schema.hidden))])
    return heading + table.draw() + "\n"
