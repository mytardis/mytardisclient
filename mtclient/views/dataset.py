"""
Views for MyTardis dataset records
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_dataset(dataset, render_format):
    """
    Render dataset

    :param dataset: The dataset to be rendered.
    :type dataset: :class:`mtclient.models.dataset.Dataset`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_dataset_as_json(dataset)
    return render_dataset_as_table(dataset)


def render_dataset_as_json(dataset, indent=2, sort_keys=True):
    """
    Returns JSON representation of dataset.

    :param dataset: The dataset to be rendered.
    :type dataset: :class:`mtclient.models.dataset.Dataset`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        dataset.response_dict, indent=indent, sort_keys=sort_keys)


def render_dataset_as_table(dataset):
    """
    Returns ASCII table view of dataset.

    :param dataset: The dataset to be rendered.
    :type dataset: :class:`mtclient.models.dataset.Dataset`
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
                           dataset_param.name.schema.name,
                           dataset_param.name.name,
                           dataset_param.string_value or "",
                           dataset_param.numerical_value or '',
                           dataset_param.datetime_value or '',
                           dataset_param.link_id or ''])
        dataset_and_param_sets += table.draw() + "\n"

    return dataset_and_param_sets


def render_datasets(datasets, render_format, display_heading=True):
    """
    Render datasets

    :param datasets: The `ResultSet` of datasets to be rendered.
    :type datasets: :class:`mtclient.models.resultset.ResultSet`
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
    return render_datasets_as_table(datasets, display_heading)


def render_datasets_as_json(datasets, indent=2, sort_keys=True):
    """
    Returns JSON representation of datasets.

    :param datasets: The result set of datasets to be displayed.
    :type datasets: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        datasets.response_dict, indent=indent, sort_keys=sort_keys)


def render_datasets_as_table(datasets, display_heading=True):
    """
    Returns ASCII table view of datasets.

    :param datasets: The datasets to be rendered.
    :type datasets: :class:`mtclient.models.resultset.ResultSet`
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
