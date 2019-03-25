"""
Controller class for running commands (list, get, create, update)
on instrument records.
"""
from __future__ import print_function

from mtclient.models.instrument import Instrument
from mtclient.utils import get_render_format
from mtclient.views import render


class InstrumentController(object):
    """
    Controller class for running commands (list, get, create, update)
    on instrument records.
    """
    def run_command(self, args):
        """
        Generic run command method.
        """
        command = args.command
        render_format = get_render_format(args)
        if command == "list":
            return self.list(args.facility, args.limit,
                             args.offset, args.order_by,
                             render_format)
        if command == "get":
            return self.get(args.instrument_id, render_format)
        if command == "create":
            return self.create(args.facility_id, args.name, render_format)
        if command == "update":
            return self.update(args.instrument_id, args.name, render_format)
        raise Exception("Invalid command: %s" % args.command)

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
        instrument = Instrument.objects.get(id=instrument_id)
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
