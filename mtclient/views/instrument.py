"""
Views for MyTardis instrument records
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_instrument(instrument, render_format):
    """
    Render instrument

    :param instrument: The instrument to be rendered.
    :type instrument: :class:`mtclient.models.instrument.Instrument`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_instrument_as_json(instrument)
    return render_instrument_as_table(instrument)


def render_instrument_as_json(instrument, indent=2, sort_keys=True):
    """
    Returns JSON representation of instrument.

    :param instrument: The instrument to be rendered.
    :type instrument: :class:`mtclient.models.instrument.Instrument`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        instrument.response_dict, indent=indent, sort_keys=sort_keys)


def render_instrument_as_table(instrument):
    """
    Returns ASCII table view of instrument.

    :param instrument: The instrument to be rendered.
    :type instrument: :class:`mtclient.models.instrument.Instrument`
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
    :type instruments: :class:`mtclient.models.resultset.ResultSet`
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
    return render_instruments_as_table(instruments, display_heading)


def render_instruments_as_json(instruments, indent=2, sort_keys=True):
    """
    Returns JSON representation of instruments.

    :param instruments: The result set of instruments to be displayed.
    :type instruments: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        instruments.response_dict, indent=indent, sort_keys=sort_keys)


def render_instruments_as_table(instruments, display_heading=True):
    """
    Returns ASCII table view of instruments.

    :param instruments: The instruments to be rendered.
    :type instruments: :class:`mtclient.models.resultset.ResultSet`
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
