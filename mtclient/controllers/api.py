"""
Controller class for listing API endpoints.
"""
from __future__ import print_function

from mtclient.models.api import ApiEndpoint
from mtclient.models.api import ApiSchema
from mtclient.utils import get_render_format
from mtclient.views import render


class ApiController(object):
    """
    Controller class for listing API endpoints.
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
            return self.list(render_format)
        if command == "get":
            return self.get(args.api_model, render_format)
        raise Exception("Invalid command: %s" % args.command)

    def list(self, render_format):
        """
        Display list of API endpoints.
        """
        # pylint: disable=no-self-use
        api_endpoints = ApiEndpoint.list()
        print(render(api_endpoints, render_format))

    def get(self, model, render_format):
        """
        Display schema for a model's API endpoint.
        """
        # pylint: disable=no-self-use
        api_schema = ApiSchema.get(model)
        print(render(api_schema, render_format))
