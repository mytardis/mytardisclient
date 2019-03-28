"""
Views for MyTardis facility records
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_facility(facility, render_format, display_heading=True):
    """
    Render facility

    :param facility: The facility to be rendered.
    :type facility: :class:`mtclient.models.facility.Facility`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for
        an `ApiEndpoints` set, setting `display_heading` to True
        ensures that a heading is displayed before the results table.
        The heading includes the URL resolved to perform the query.
    """
    if render_format == 'json':
        return render_facility_as_json(facility)
    return render_facility_as_table(facility, display_heading)


def render_facility_as_json(facility, indent=2, sort_keys=True):
    """
    Returns JSON representation of facility.

    :param facility: The facility to be rendered.
    :type facility: :class:`mtclient.models.facility.Facility`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        facility.response_dict, indent=indent, sort_keys=sort_keys)


def render_facility_as_table(facility, display_heading=True):
    """
    Returns ASCII table view of facility.

    :param facility: The facility to be rendered.
    :type facility: :class:`mtclient.models.facility.Facility`
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
    :type facilities: :class:`mtclient.models.resultset.ResultSet`
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
    return render_facilities_as_table(facilities, display_heading)


def render_facilities_as_json(facilities, indent=2, sort_keys=True):
    """
    Returns JSON representation of facilities.

    :param facilities: The result set of facilities to be displayed.
    :type facilities: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        facilities.response_dict, indent=indent, sort_keys=sort_keys)


def render_facilities_as_table(facilities, display_heading=True):
    """
    Returns ASCII table view of facilities.

    :param facilities: The facilities to be rendered.
    :type facilities: :class:`mtclient.models.resultset.ResultSet`
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
