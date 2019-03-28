"""
Views for MyTardis api endpoints.
"""
from __future__ import print_function

import json
from texttable import Texttable


def render_api_schema(api_schema, render_format):
    """
    Render API schema

    :param api_schema: The API schema model to be displayed.
    :type api_schema: :class:`mtclient.models.api.ApiSchema`
    :param render_format: The format to display the data in ('table' or
        'json').
    """
    if render_format == 'json':
        return render_api_schema_as_json(api_schema)
    return render_api_schema_as_table(api_schema)


def render_api_schema_as_json(api_schema, indent=2, sort_keys=True):
    """
    Returns JSON representation of API schema.

    :param api_schema: The API schema model to be displayed.
    :type api_schema: :class:`mtclient.models.api.ApiSchema`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        api_schema.response_dict, indent=indent, sort_keys=sort_keys)


def render_api_schema_as_table(api_schema):
    """
    Returns ASCII table view of API schema.

    :param api_schema: The API schema model to be displayed.
    :type api_schema: :class:`mtclient.models.api.ApiSchema`
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
    :type api_endpoints: :class:`mtclient.models.api.ApiEndpoints`
    :param render_format: The format to display the data in ('table' or
        'json').
    :param display_heading: When using the 'table' render format for
        an `ApiEndpoints` set, setting `display_heading` to True
        ensures that a heading is displayed before the results table.
        The heading includes the URL resolved to perform the query.
    """
    if render_format == 'json':
        return render_api_endpoints_as_json(api_endpoints)
    return render_api_endpoints_as_table(api_endpoints, display_heading)


def render_api_endpoints_as_json(api_endpoints, indent=2, sort_keys=True):
    """
    Returns JSON representation of api_endpoints.

    :param api_endpoints: The API endpoints to be rendered.
    :type api_endpoints: :class:`mtclient.models.api.ApiEndpoints`
    :param indent: If indent is a non-negative integer or string, then JSON
        array elements and object members will be pretty-printed with that
        indent level.
    :param sort_keys: If sort_keys is `True` (default: `False`), then the
        rendered JSON will be sorted by key.
    """
    return json.dumps(
        api_endpoints.response_dict, indent=indent, sort_keys=sort_keys)


def render_api_endpoints_as_table(api_endpoints, display_heading=True):
    """
    Returns ASCII table view of api_endpoints.

    :param api_endpoints: The API endpoints to be rendered.
    :type api_endpoints: :class:`mtclient.models.api.ApiEndpoints`
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
