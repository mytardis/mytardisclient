"""
Views for MyTardis records.
"""

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
    Generic render function
    """
    if data.__class__ == ResultSet:
        return render_result_set(data, render_format, display_heading)
    elif data.__class__ == ApiEndpoints:
        return render_api_endpoints(data, render_format, display_heading)
    else:
        return render_single_record(data, render_format, display_heading)


def render_single_record(data, render_format, display_heading=True):
    """
    Render single record.
    """
    # pylint: disable=too-many-return-statements
    if data.__class__ == ApiSchema:
        return render_api_schema(data, render_format, display_heading)
    elif data.__class__ == Facility:
        return render_facility(data, render_format, display_heading)
    elif data.__class__ == Instrument:
        return render_instrument(data, render_format, display_heading)
    elif data.__class__ == Experiment:
        return render_experiment(data, render_format, display_heading)
    elif data.__class__ == Dataset:
        return render_dataset(data, render_format, display_heading)
    elif data.__class__ == DataFile:
        return render_datafile(data, render_format, display_heading)
    elif data.__class__ == StorageBox:
        return render_storage_box(data, render_format, display_heading)
    elif data.__class__ == Schema:
        return render_schema(data, render_format, display_heading)
    else:
        print "Class is " + data.__class__.__name__


def render_result_set(data, render_format, display_heading=True):
    """
    Render result set.
    """
    # pylint: disable=too-many-return-statements
    if data.model == Facility:
        return render_facilities(data, render_format, display_heading)
    elif data.model == Instrument:
        return render_instruments(data, render_format, display_heading)
    elif data.model == Experiment:
        return render_experiments(data, render_format, display_heading)
    elif data.model == Dataset:
        return render_datasets(data, render_format, display_heading)
    elif data.model == DataFile:
        return render_datafiles(data, render_format, display_heading)
    elif data.model == StorageBox:
        return render_storage_boxes(data, render_format, display_heading)
    elif data.model == Schema:
        return render_schemas(data, render_format, display_heading)
    else:
        print "Class is " + data.model.__name__


def render_api_schema(api_schema, render_format, display_heading=True):
    """
    Render API schema
    """
    if render_format == 'json':
        return render_api_schema_as_json(api_schema)
    else:
        return render_api_schema_as_table(api_schema, display_heading)


def render_api_schema_as_json(api_schema, indent=2, sort_keys=True):
    """
    Returns JSON representation of API schema.
    """
    return json.dumps(api_schema.json, indent=indent, sort_keys=sort_keys)


def render_api_schema_as_table(api_schema, display_heading=True):
    """
    Returns ASCII table view of API schema.
    """
    heading = "\nAPI Schema:\n\n" if display_heading else ""

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
    return heading + table.draw() + "\n"


def render_api_endpoints(api_endpoints, render_format, display_heading=True):
    """
    Render API endpoints
    """
    if render_format == 'json':
        return render_api_endpoints_as_json(api_endpoints)
    else:
        return render_api_endpoints_as_table(api_endpoints, display_heading)


def render_api_endpoints_as_json(api_endpoints, indent=2, sort_keys=True):
    """
    Returns JSON representation of api_endpoints.
    """
    return json.dumps(api_endpoints.json, indent=indent, sort_keys=sort_keys)


def render_api_endpoints_as_table(api_endpoints, display_heading=True):
    """
    Returns ASCII table view of api_endpoints..
    """
    heading = "\n" \
        "API Endpoints\n" if display_heading else ""

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm'])
    table.header(["Model", "List Endpoint", "Schema"])
    for api_endpoint in api_endpoints:
        table.add_row([api_endpoint.model, api_endpoint.list_endpoint,
                       api_endpoint.schema])
    return heading + table.draw() + "\n"


def render_facility(facility, render_format, display_heading=True):
    """
    Render facility
    """
    if render_format == 'json':
        return render_facility_as_json(facility)
    else:
        return render_facility_as_table(facility, display_heading)


def render_facility_as_json(facility, indent=2, sort_keys=True):
    """
    Returns JSON representation of facility.
    """
    return json.dumps(facility.json, indent=indent, sort_keys=sort_keys)


def render_facility_as_table(facility, display_heading=True):
    """
    Returns ASCII table view of facility.
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
    """
    if render_format == 'json':
        return render_facilities_as_json(facilities)
    else:
        return render_facilities_as_table(facilities, display_heading)


def render_facilities_as_json(facilities, indent=2, sort_keys=True):
    """
    Returns JSON representation of facilities.
    """
    return json.dumps(facilities.json, indent=indent, sort_keys=sort_keys)


def render_facilities_as_table(facilities, display_heading=True):
    """
    Returns ASCII table view of facilities..
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


def render_instrument(instrument, render_format, display_heading=True):
    """
    Render instrument
    """
    if render_format == 'json':
        return render_instrument_as_json(instrument)
    else:
        return render_instrument_as_table(instrument, display_heading)


def render_instrument_as_json(instrument, indent=2, sort_keys=True):
    """
    Returns JSON representation of instrument.
    """
    return json.dumps(instrument.json, indent=indent, sort_keys=sort_keys)


def render_instrument_as_table(instrument, display_heading=True):
    """
    Returns ASCII table view of instrument.
    """
    heading = "\nModel: Instrument\n\n" if display_heading else ""

    instrument_table = Texttable()
    instrument_table.set_cols_align(['l', 'l'])
    instrument_table.set_cols_valign(['m', 'm'])
    instrument_table.header(["Instrument field", "Value"])
    instrument_table.add_row(["ID", instrument.id])
    instrument_table.add_row(["Name", instrument.name])
    instrument_table.add_row(["Facility", instrument.facility])
    return heading + instrument_table.draw() + "\n"


def render_instruments(instruments, render_format, display_heading=True):
    """
    Render instruments
    """
    if render_format == 'json':
        return render_instruments_as_json(instruments)
    else:
        return render_instruments_as_table(instruments, display_heading)


def render_instruments_as_json(instruments, indent=2, sort_keys=True):
    """
    Returns JSON representation of instruments.
    """
    return json.dumps(instruments.json, indent=indent, sort_keys=sort_keys)


def render_instruments_as_table(instruments, display_heading=True):
    """
    Returns ASCII table view of instruments..
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


def render_experiment(experiment, render_format, display_heading=True):
    """
    Render experiment
    """
    if render_format == 'json':
        return render_experiment_as_json(experiment)
    else:
        return render_experiment_as_table(experiment, display_heading)


def render_experiment_as_json(experiment, indent=2, sort_keys=True):
    """
    Returns JSON representation of experiment.
    """
    return json.dumps(experiment.json, indent=indent, sort_keys=sort_keys)


def render_experiment_as_table(experiment, display_heading=True):
    """
    Returns ASCII table view of experiment.
    """
    heading = "\nModel: Experiment\n\n" if display_heading else ""
    exp_and_param_sets = heading

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
        heading = "\nExperiment Parameter Set: %s\n\n" \
            % str(exp_param_set.schema) if display_heading else ""
        exp_and_param_sets += heading
        table = Texttable(max_width=0)
        table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l'])
        table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm'])
        table.header(["ID", "Parameter Name", "String Value",
                      "Numerical Value", "Datetime Value", "Link ID"])
        for exp_param in exp_param_set.parameters:
            table.add_row([exp_param.id, exp_param.name,
                           exp_param.string_value,
                           exp_param.numerical_value or '',
                           exp_param.datetime_value or '',
                           exp_param.link_id or ''])
        exp_and_param_sets += table.draw() + "\n"

    return exp_and_param_sets


def render_experiments(experiments, render_format, display_heading=True):
    """
    Render experiments
    """
    if render_format == 'json':
        return render_experiments_as_json(experiments)
    else:
        return render_experiments_as_table(experiments, display_heading)


def render_experiments_as_json(experiments, indent=2, sort_keys=True):
    """
    Returns JSON representation of experiments.
    """
    return json.dumps(experiments.json, indent=indent, sort_keys=sort_keys)


def render_experiments_as_table(experiments, display_heading=True):
    """
    Returns ASCII table view of experiments..
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


def render_dataset(dataset, render_format, display_heading=True):
    """
    Render dataset
    """
    if render_format == 'json':
        return render_dataset_as_json(dataset)
    else:
        return render_dataset_as_table(dataset, display_heading)


def render_dataset_as_json(dataset, indent=2, sort_keys=True):
    """
    Returns JSON representation of dataset.
    """
    return json.dumps(dataset.json, indent=indent, sort_keys=sort_keys)


def render_dataset_as_table(dataset, display_heading=True):
    """
    Returns ASCII table view of dataset.
    """
    heading = "\nModel: Dataset\n\n" if display_heading else ""

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Dataset field", "Value"])
    table.add_row(["ID", dataset.id])
    table.add_row(["Experiment(s)", "\n".join(dataset.experiments)])
    table.add_row(["Description", dataset.description])
    table.add_row(["Instrument", dataset.instrument])
    return heading + table.draw() + "\n"


def render_datasets(datasets, render_format, display_heading=True):
    """
    Render datasets
    """
    if render_format == 'json':
        return render_datasets_as_json(datasets)
    else:
        return render_datasets_as_table(datasets, display_heading)


def render_datasets_as_json(datasets, indent=2, sort_keys=True):
    """
    Returns JSON representation of datasets.
    """
    return json.dumps(datasets.json, indent=indent, sort_keys=sort_keys)


def render_datasets_as_table(datasets, display_heading=True):
    """
    Returns ASCII table view of datasets..
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


def render_datafile(datafile, render_format, display_heading=True):
    """
    Render datafile
    """
    if render_format == 'json':
        return render_datafile_as_json(datafile)
    else:
        return render_datafile_as_table(datafile, display_heading)


def render_datafile_as_json(datafile, indent=2, sort_keys=True):
    """
    Returns JSON representation of datafile.
    """
    return json.dumps(datafile.json, indent=indent, sort_keys=sort_keys)


def render_datafile_as_table(datafile, display_heading=True):
    """
    Returns ASCII table view of datafile.
    """
    heading = "\nModel: DataFile\n\n" if display_heading else ""

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["DataFile field", "Value"])
    table.add_row(["ID", datafile.id])
    table.add_row(["Dataset", datafile.dataset])
    table.add_row(["Filename", datafile.filename])
    uris = [replica.uri for replica in datafile.replicas]
    table.add_row(["URI", "\n".join(uris)])
    table.add_row(["Verified", str(datafile.verified)])
    table.add_row(["Size", human_readable_size_string(datafile.size)])
    table.add_row(["MD5 Sum", datafile.md5sum])
    return heading + table.draw() + "\n"


def render_datafiles(datafiles, render_format, display_heading=True):
    """
    Render datafiles
    """
    if render_format == 'json':
        return render_datafiles_as_json(datafiles)
    else:
        return render_datafiles_as_table(datafiles, display_heading)


def render_datafiles_as_json(datafiles, indent=2, sort_keys=True):
    """
    Returns JSON representation of datafiles.
    """
    return json.dumps(datafiles.json, indent=indent, sort_keys=sort_keys)


def render_datafiles_as_table(datafiles, display_heading=True):
    """
    Returns ASCII table view of datafiles..
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
    table.header(["ID", "Directory", "Filename", "URI", "Verified",
                  "Size", "MD5 Sum"])
    for datafile in datafiles:
        uris = [replica.uri for replica in datafile.replicas]
        table.add_row([datafile.id, datafile.directory, datafile.filename,
                       "\n".join(uris), str(datafile.verified),
                       human_readable_size_string(datafile.size),
                       datafile.md5sum])
    return heading + table.draw() + "\n"


def render_storage_box(storage_box, render_format, display_heading=True):
    """
    Render storage box
    """
    if render_format == 'json':
        return render_storage_box_as_json(storage_box)
    else:
        return render_storage_box_as_table(storage_box, display_heading)


def render_storage_box_as_json(storage_box, indent=2, sort_keys=True):
    """
    Returns JSON representation of storage_box.
    """
    return json.dumps(storage_box.json, indent=indent, sort_keys=sort_keys)


def render_storage_box_as_table(storage_box, display_heading=True):
    """
    Returns ASCII table view of storage_box.
    """
    storage_box_options_attributes = ""

    heading = "\nModel: StorageBox\n\n" if display_heading else ""
    storage_box_options_attributes += heading

    table = Texttable()
    table.set_cols_align(['l', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["StorageBox field", "Value"])
    table.add_row(["ID", storage_box.id])
    table.add_row(["Name", storage_box.name])
    storage_box_options_attributes += table.draw() + "\n"

    heading = "\nModel: StorageBoxOptions\n\n" if display_heading else ""
    storage_box_options_attributes += heading

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Key", "Value"])
    for option in storage_box.options:
        table.add_row([option.key, option.value])
    storage_box_options_attributes += table.draw() + "\n"

    heading = "\nModel: StorageBoxAttributes\n\n" if display_heading else ""
    storage_box_options_attributes += heading

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["Key", "Value"])
    for attribute in storage_box.attributes:
        table.add_row([attribute.key, attribute.value])
    storage_box_options_attributes += table.draw() + "\n"

    return storage_box_options_attributes


def render_storage_boxes(storage_boxes, render_format, display_heading=True):
    """
    Render storage_boxes
    """
    if render_format == 'json':
        return render_storage_boxes_as_json(storage_boxes)
    else:
        return render_storage_boxes_as_table(storage_boxes, display_heading)


def render_storage_boxes_as_json(storage_boxes, indent=2, sort_keys=True):
    """
    Returns JSON representation of storage_boxes.
    """
    return json.dumps(storage_boxes.json, indent=indent, sort_keys=sort_keys)


def render_storage_boxes_as_table(storage_boxes, display_heading=True):
    """
    Returns ASCII table view of storage_boxes..
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
    table.set_cols_align(["r", 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(["ID", "Name"])
    for storage_box in storage_boxes:
        table.add_row([storage_box.id, storage_box.name])
    return heading + table.draw() + "\n"


def render_schema(schema, render_format, display_heading=True):
    """
    Render schema
    """
    if render_format == 'json':
        return render_schema_as_json(schema)
    else:
        return render_schema_as_table(schema, display_heading)


def render_schema_as_json(schema, indent=2, sort_keys=True):
    """
    Returns JSON representation of schema.
    """
    return json.dumps(schema.json, indent=indent, sort_keys=sort_keys)


def render_schema_as_table(schema, display_heading=True):
    """
    Returns ASCII table view of schema.
    """
    heading = "\nModel: Schema\n\n" if display_heading else ""
    schema_parameter_names = heading

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

    heading = "\nModel: ParameterName\n\n" if display_heading else ""
    schema_parameter_names += heading

    table = Texttable(max_width=0)
    table.set_cols_align(["r", 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'])
    table.header(["ID", "Full Name", "Name", "Data Type",
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
    """
    if render_format == 'json':
        return render_schemas_as_json(schemas)
    else:
        return render_schemas_as_table(schemas, display_heading)


def render_schemas_as_json(schemas, indent=2, sort_keys=True):
    """
    Returns JSON representation of schemas.
    """
    return json.dumps(schemas.json, indent=indent, sort_keys=sort_keys)


def render_schemas_as_table(schemas, display_heading=True):
    """
    Returns ASCII table view of schemas..
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
                       schema.type, schema.subtype,
                       str(bool(schema.immutable)), str(bool(schema.hidden))])
    return heading + table.draw() + "\n"
