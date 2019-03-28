"""
Views for MyTardis storage box records
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_storage_box(storage_box, render_format):
    """
    Render storage box

    :param storage_box: The storage box to be rendered.
    :type storage_box: :class:`mtclient.models.storagebox.StorageBox`
    """
    if render_format == 'json':
        return render_storage_box_as_json(storage_box)
    return render_storage_box_as_table(storage_box)


def render_storage_box_as_json(storage_box, indent=2, sort_keys=True):
    """
    Returns JSON representation of storage_box.

    :param storage_box: The storage box to be rendered.
    :type storage_box: :class:`mtclient.models.storagebox.StorageBox`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        storage_box.response_dict, indent=indent, sort_keys=sort_keys)


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

    if storage_box.options:
        storage_box_options_attributes += "\n"
        table = Texttable(max_width=0)
        table.set_cols_align(["r", 'l'])
        table.set_cols_valign(['m', 'm'])
        table.header(["StorageBoxOption Key", "StorageBoxOption Value"])
        for option in storage_box.options:
            table.add_row([option.key, option.value])
        storage_box_options_attributes += table.draw() + "\n"

    if storage_box.attributes:
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
    :type storage_boxes: :class:`mtclient.models.resultset.ResultSet`
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
    return render_storage_boxes_as_table(storage_boxes, display_heading)


def render_storage_boxes_as_json(storage_boxes, indent=2, sort_keys=True):
    """
    Returns JSON representation of storage_boxes.

    :param storage_boxes: The result set of storage boxes to be displayed.
    :type storage_boxes: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        storage_boxes.response_dict, indent=indent, sort_keys=sort_keys)


def render_storage_boxes_as_table(storage_boxes, display_heading=True):
    """
    Returns ASCII table view of storage_boxes.

    :param storage_boxes: The storage boxes to be rendered.
    :type storage_boxes: :class:`mtclient.models.resultset.ResultSet`
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
