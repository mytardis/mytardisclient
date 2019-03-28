"""
Views for MyTardis schema records
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_schema(schema, render_format):
    """
    Render schema

    :param schema: The schema to be rendered.
    :type schema: :class:`mtclient.models.schema.Schema`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_schema_as_json(schema)
    return render_schema_as_table(schema)


def render_schema_as_json(schema, indent=2, sort_keys=True):
    """
    Returns JSON representation of schema.

    :param schema: The schema to be rendered.
    :type schema: :class:`mtclient.models.schema.Schema`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        schema.response_dict, indent=indent, sort_keys=sort_keys)


def render_schema_as_table(schema):
    """
    Returns ASCII table view of schema.

    :param schema: The schema to be rendered.
    :type schema: :class:`mtclient.models.schema.Schema`
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

    if not schema.parameter_names:
        return schema_parameter_names

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
    :type schemas: :class:`mtclient.models.resultset.ResultSet`
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
    return render_schemas_as_table(schemas, display_heading)


def render_schemas_as_json(schemas, indent=2, sort_keys=True):
    """
    Returns JSON representation of schemas.

    :param schemas: The result set of schemas boxes to be displayed.
    :type schemas: :class:`mtclient.models.resultset.ResultSet`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        schemas.response_dict, indent=indent, sort_keys=sort_keys)


def render_schemas_as_table(schemas, display_heading=True):
    """
    Returns ASCII table view of schemas.

    :param schemas: The schemas to be rendered.
    :type schemas: :class:`mtclient.models.resultset.ResultSet`
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
