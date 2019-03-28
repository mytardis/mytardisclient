"""
Views for MyTardis records.
"""
from __future__ import print_function

import json
from texttable import Texttable

from ..utils import human_readable_size_string


def render_datafile(datafile, render_format):
    """
    Render datafile

    :param datafile: The datafile to be rendered.
    :type datafile: :class:`mtclient.models.datafile.DataFile`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_datafile_as_json(datafile)
    return render_datafile_as_table(datafile)


def render_datafile_as_json(datafile, indent=2, sort_keys=True):
    """
    Returns JSON representation of datafile.

    :param datafile: The datafile to be rendered.
    :type datafile: :class:`mtclient.models.datafile.DataFile`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        datafile.response_dict, indent=indent, sort_keys=sort_keys)


def render_datafile_as_table(datafile):
    """
    Returns ASCII table view of datafile.

    :param datafile: The datafile to be rendered.
    :type datafile: :class:`mtclient.models.datafile.DataFile`
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
    :type datafiles: :class:`mtclient.models.resultset.ResultSet`
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
    return render_datafiles_as_table(datafiles, display_heading)


def render_datafiles_as_json(datafiles, indent=2, sort_keys=True):
    """
    Returns JSON representation of datafiles.

    :param datafiles: The result set of datafiles to be displayed.
    :type datafiles: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        datafiles.response_dict, indent=indent, sort_keys=sort_keys)


def render_datafiles_as_table(datafiles, display_heading=True):
    """
    Returns ASCII table view of datafiles.

    :param datafiles: The datafiles to be rendered.
    :type datafiles: :class:`mtclient.models.resultset.ResultSet`
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
