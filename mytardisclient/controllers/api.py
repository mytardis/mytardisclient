"""
Controller class for listing API endpoints.
"""
from __future__ import print_function

from mytardisclient.models.api import ApiEndpoint
from mytardisclient.models.api import ApiSchema
from mytardisclient.views import render


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
        if hasattr(args, 'json') and args.json:
            render_format = 'json'
        else:
            render_format = 'table'
        if command == "list":
            return self.list(render_format)
        elif command == "get":
            return self.get(args.api_model, render_format)

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
