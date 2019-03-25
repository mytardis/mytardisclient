"""
Controller class for running commands (list, get)
on schemas.
"""
from __future__ import print_function

from mtclient.models.schema import Schema
from mtclient.utils import get_render_format
from mtclient.views import render


class SchemaController(object):
    """
    Controller class for running commands (list, get)
    on schemas.
    """
    def __init__(self):
        pass

    def run_command(self, args):
        """
        Generic run command method.
        """
        command = args.command
        render_format = get_render_format(args)
        if command == "list":
            return self.list(args.limit, args.offset, args.order_by,
                             render_format)
        if command == "get":
            return self.get(args.schema_id, render_format)
        raise Exception("Invalid command: %s" % args.command)

    def list(self, limit, offset, order_by, render_format):
        """
        Display list of schemas.
        """
        # pylint: disable=no-self-use
        schemas = Schema.list(limit, offset, order_by)
        print(render(schemas, render_format))

    def get(self, schema_id, render_format):
        """
        Display schema record.
        """
        # pylint: disable=no-self-use
        schema = Schema.objects.get(id=schema_id)
        print(render(schema, render_format))
