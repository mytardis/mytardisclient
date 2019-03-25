"""
Controller class for running commands (list, get, create, update)
on facility records.
"""
from __future__ import print_function

from mtclient.models.facility import Facility
from mtclient.models.instrument import Instrument
from mtclient.views import render

from .cli import ModelCliController


class FacilityController(ModelCliController):
    """
    Controller class for running commands (list, get, create, update)
    on facility records.
    """
    def __init__(self):
        super(FacilityController, self).__init__()
        self.allowed_commands = ["list", "get"]
        self.primary_key_arg = "facility_id"
        self.model = Facility

    def get(self, args, render_format):
        """
        Display facility record
        """
        super(FacilityController, self).get(args, render_format)
        if render_format == 'table':
            instruments = Instrument.list(args.facility_id)
            print(render(instruments, render_format))
