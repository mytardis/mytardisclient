"""
Controller class for running commands (list, get, create, update)
on facility records.
"""
from __future__ import print_function

from mtclient.models.facility import Facility
from mtclient.models.instrument import Instrument
from mtclient.utils import get_render_format
from mtclient.views import render


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
        render_format = get_render_format(args)
        if command == "list":
            return self.list(args.limit, args.offset, args.order_by,
                             render_format)
        if command == "get":
            return self.get(args.facility_id, render_format)
        raise Exception("Invalid command: %s" % args.command)

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
        facility = Facility.objects.get(id=facility_id)
        print(render(facility, render_format))
        if render_format == 'table':
            instruments = Instrument.list(facility_id)
            print(render(instruments, render_format))
