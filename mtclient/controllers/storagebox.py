"""
Controller class for running commands (list)
on storage boxes.
"""
from ..models.storagebox import StorageBox
from .cli import ModelCliController


class StorageBoxController(ModelCliController):
    """
    Controller class for running commands (list, get) on storage box records
    """
    def __init__(self):
        super(StorageBoxController, self).__init__()
        self.allowed_commands = ["list", "get"]
        self.primary_key_arg = "storage_box_id"
        self.model = StorageBox
