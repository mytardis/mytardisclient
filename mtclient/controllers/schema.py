"""
Controller class for running commands (list, get)
on schemas.
"""
from __future__ import print_function

from ..models.schema import Schema
from ..views import render

from .cli import ModelCliController


class SchemaController(ModelCliController):
    """
    Controller class for running commands (list, get) on schema records.
    """
    def __init__(self):
        super(SchemaController, self).__init__()
        self.allowed_commands = ["list", "get"]
        self.primary_key_arg = "schema_id"
        self.model = Schema

    def get(self, args, render_format):
        """
        Display a single record
        """
        primary_key = getattr(args, "schema_id")
        instance = Schema.objects.get(id=primary_key, param_names=args.params)
        print(render(instance, render_format))
