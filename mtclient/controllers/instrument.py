"""
Controller class for running commands (list, get, create, update)
on instrument records.
"""
from __future__ import print_function

from mtclient.models.instrument import Instrument
from mtclient.views import render

from .cli import ModelCliController


class InstrumentController(ModelCliController):
    """
    Controller class for running commands (list, get, create, update)
    on instrument records.
    """
    def __init__(self):
        super(InstrumentController, self).__init__()
        self.allowed_commands = ["list", "get", "create", "update"]
        self.primary_key_arg = "instrument_id"
        self.model = Instrument

    def list(self, args, render_format):
        """
        Display list of instrument records.
        """
        # pylint: disable=no-self-use
        facility_id = getattr(args, "facility_id", getattr(args, "facility", None))
        filters = ""
        if facility_id:
            filters = "facility__id=%s" % facility_id
        instruments = Instrument.list(
            filters, args.limit, args.offset, args.order_by)
        print(render(instruments, render_format))

    def get(self, args, render_format):
        """
        Display instrument record.
        """
        # pylint: disable=no-self-use
        instrument = Instrument.objects.get(id=args.instrument_id)
        print(render(instrument, render_format))

    def create(self, args, render_format):
        """
        Create instrument record.
        """
        # pylint: disable=no-self-use
        facility_id = getattr(args, "facility_id", getattr(args, "facility", None))
        instrument = Instrument.create(facility_id, args.name)
        print(render(instrument, render_format))
        print("Instrument created successfully.")

    def update(self, args, render_format):
        """
        Update instrument record.
        """
        # pylint: disable=no-self-use
        instrument = Instrument.update(args.instrument_id, args.name)
        print(render(instrument, render_format))
        print("Instrument updated successfully.")
