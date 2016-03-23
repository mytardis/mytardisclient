"""
Controller class for running commands (list, get, create, update)
on facility records.
"""
from __future__ import print_function

from mytardisclient.models.facility import Facility
from mytardisclient.models.instrument import Instrument
from mytardisclient.views import render


class FacilityController(object):
    """
    Controller class for running commands (list, get, create, update)
    on facility records.
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
        if command == "get":
            return self.get(args.facility_id, render_format)

    def list(self, limit, offset, order_by, render_format):
        """
        Display list of facility records.
        """
        # pylint: disable=no-self-use
        facilities = Facility.list(limit, offset, order_by)
        print(render(facilities, render_format))

    def get(self, facility_id, render_format):
        """
        Display facility record.
        """
        # pylint: disable=no-self-use
        facility = Facility.get(facility_id)
        print(render(facility, render_format))
        if render_format == 'table':
            instruments = Instrument.list(facility_id)
            print(render(instruments, render_format))
