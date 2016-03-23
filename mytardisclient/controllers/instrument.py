"""
Controller class for running commands (list, get, create, update)
on instrument records.
"""
from __future__ import print_function

from mytardisclient.models.instrument import Instrument
from mytardisclient.views import render


class InstrumentController(object):
    """
    Controller class for running commands (list, get, create, update)
    on instrument records.
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
            return self.list(args.facility, args.limit,
                             args.offset, args.order_by,
                             render_format)
        elif command == "get":
            return self.get(args.instrument_id, render_format)
        elif command == "create":
            return self.create(args.facility_id, args.name, render_format)
        elif command == "update":
            return self.update(args.instrument_id, args.name, render_format)

    def list(self, facility_id, limit, offset, order_by, render_format):
        """
        Display list of instrument records.
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        instruments = Instrument.list(facility_id,
                                      limit, offset, order_by)
        print(render(instruments, render_format))

    def get(self, instrument_id, render_format):
        """
        Display instrument record.
        """
        # pylint: disable=no-self-use
        instrument = Instrument.get(instrument_id)
        print(render(instrument, render_format))

    def create(self, facility_id, name, render_format):
        """
        Create instrument record.
        """
        # pylint: disable=no-self-use
        instrument = Instrument.create(facility_id, name)
        print(render(instrument, render_format))
        print("Instrument created successfully.")

    def update(self, instrument_id, name, render_format):
        """
        Update instrument record.
        """
        # pylint: disable=no-self-use
        instrument = Instrument.update(instrument_id, name)
        print(render(instrument, render_format))
        print("Instrument updated successfully.")
