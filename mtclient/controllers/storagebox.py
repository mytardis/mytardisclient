"""
Controller class for running commands (list)
on storage boxes.
"""
from __future__ import print_function

from mtclient.models.storagebox import StorageBox
from mtclient.utils import get_render_format
from mtclient.views import render


class StorageBoxController(object):
    """
    Controller class for running commands (list)
    on storage boxes.
    """
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
            return self.get(args.storage_box_id, render_format)
        raise Exception("Invalid command: %s" % args.command)

    def list(self, limit, offset, order_by, render_format):
        """
        Display list of storage boxes.
        """
        # pylint: disable=no-self-use
        storage_boxes = StorageBox.list(limit, offset, order_by)
        print(render(storage_boxes, render_format))

    def get(self, storage_box_id, render_format):
        """
        Display storage box record.
        """
        # pylint: disable=no-self-use
        storage_box = StorageBox.objects.get(id=storage_box_id)
        print(render(storage_box, render_format))
