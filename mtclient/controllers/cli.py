"""
Controller base class for running commands (list, get, create, update)
"""
from ..utils import get_render_format
from ..views import render


class ModelCliController(object):
    """
    Controller base class for running commands (list, get, create, update)
    on model records

    Cli is an abbreviation for Command Line Interface
    """
    def __init__(self):
        self.allowed_commands = ["list", "get"]
        self.primary_key_arg = "id"
        self.model = None

    def run_command(self, args):
        """
        Generic run command method.
        """
        if args.command not in self.allowed_commands:
            raise NotImplementedError("Invalid command: %s" % args.command)
        render_format = get_render_format(args)
        getattr(self, args.command)(args, render_format)

    def list(self, args, render_format):
        """
        Display a list of records
        """
        if not self.model:
            return
        result_set = self.model.list(
            args.limit, args.offset, args.order_by)
        print(render(result_set, render_format))

    def get(self, args, render_format):
        """
        Display a single record
        """
        if not self.model:
            return
        primary_key = getattr(args, self.primary_key_arg)
        instance = self.model.objects.get(id=primary_key)
        print(render(instance, render_format))
