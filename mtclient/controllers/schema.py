"""
Controller class for running commands (list, get)
on schemas.
"""
from mtclient.models.schema import Schema

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
