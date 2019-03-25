"""
mytardisclient utils
"""
from six.moves import urllib


def human_readable_size_string(num):
    """
    Returns human-readable string.
    """
    num = float(num)
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if -1024.0 < num < 1024.0:
            return "%3.0f %s" % (num, unit)
        num /= 1024.0
    return "%3.0f %s" % (num, 'TB')


def extend_url(url, limit=None, offset=None, order_by=None):
    """
    Add the limit, offset and order_by to the API request URL
    """
    if limit:
        url += "&limit=%s" % limit
    if offset:
        url += "&offset=%s" % offset
    if order_by:
        url += "&order_by=%s" % order_by
    return url


def add_filters(url, filters):
    """
    Add filters to an API request URL
    """
    if filters:
        filter_components = filters.split('&')
        for filter_component in filter_components:
            field, value = filter_component.split('=')
            url += "&%s=%s" % (field, urllib.parse.quote(value))
    return url


def get_render_format(args):
    """
    Determine how to render the output (ASCII table or JSON)
    depending on whether --json was supplied as a command-line arg
    """
    if hasattr(args, 'json') and args.json:
        return 'json'
    return 'table'
