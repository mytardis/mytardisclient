"""
Controller class for running commands (list, get)
on uploaders.
"""

from mytardisclient.models.uploader import Uploader
from mytardisclient.views import render


class UploaderController(object):
    """
    Controller class for running commands (list, get)
    on uploaders.
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
            return self.list(args.limit, args.offset, args.order_by,
                             render_format)
        elif command == "get":
            return self.get(args.uploader_id, render_format)

    def list(self, limit, offset, order_by, render_format):
        """
        Display list of uploaders.
        """
        # pylint: disable=no-self-use
        uploaders = Uploader.list(limit, offset, order_by)
        print render(uploaders, render_format)

    def get(self, uploader_id, render_format):
        """
        Display uploader record.
        """
        # pylint: disable=no-self-use
        uploader = Uploader.get(uploader_id)
        print render(uploader, render_format)
