"""
Controller class for listing API endpoints.
"""

from mytardisclient.models.api import ApiEndpoint
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

    def list(self, render_format):
        """
        Display list of API endpoints.
        """
        # pylint: disable=no-self-use
        api_endpoints = ApiEndpoint.list()
        print render(api_endpoints, render_format)
