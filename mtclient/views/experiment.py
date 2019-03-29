"""
Views for MyTardis experiment records
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_experiment(experiment, render_format):
    """
    Render experiment

    :param experiment: The experiment to be rendered.
    :type experiment: :class:`mtclient.models.experiment.Experiment`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_experiment_as_json(experiment)
    return render_experiment_as_table(experiment)


def render_experiment_as_json(experiment, indent=2, sort_keys=True):
    """
    Returns JSON representation of experiment.

    :param experiment: The experiment to be rendered.
    :type experiment: :class:`mtclient.models.experiment.Experiment`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        experiment.response_dict, indent=indent, sort_keys=sort_keys)


def render_experiment_as_table(experiment):
    """
    Returns ASCII table view of experiment.

    :param experiment: The experiment to be rendered.
    :type experiment: :class:`mtclient.models.experiment.Experiment`
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
                           exp_param.name.schema.name,
                           exp_param.name.name,
                           exp_param.string_value or '',
                           exp_param.numerical_value or '',
                           exp_param.datetime_value or '',
                           exp_param.link_id or ''])
        exp_and_param_sets += table.draw() + "\n"

    return exp_and_param_sets


def render_experiments(experiments, render_format, display_heading=True):
    """
    Render experiments

    :param experiments: The `ResultSet` of experiments to be rendered.
    :type experiments: :class:`mtclient.models.resultset.ResultSet`
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
    return render_experiments_as_table(experiments, display_heading)


def render_experiments_as_json(experiments, indent=2, sort_keys=True):
    """
    Returns JSON representation of experiments.

    :param experiments: The result set of experiments to be displayed.
    :type experiments: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        experiments.response_dict, indent=indent, sort_keys=sort_keys)


def render_experiments_as_table(experiments, display_heading=True):
    """
    Returns ASCII table view of experiments.

    :param experiments: The experiments to be rendered.
    :type experiments: :class:`mtclient.models.resultset.ResultSet`
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
