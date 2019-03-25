"""
Controller class for running commands (list, get, download, upload, update,
                                       verify)
on datafile records.
"""
from __future__ import print_function

import os

from mtclient.models.datafile import DataFile
from mtclient.views import render

from .cli import ModelCliController


class DataFileController(ModelCliController):
    """
    Controller class for running commands (list, get, download, upload, update,
                                           verify))
    on datafile records.
    """
    def __init__(self):
        super(DataFileController, self).__init__()
        self.allowed_commands = [
            "list", "get", "create", "update", "download", "upload", "verify"]
        self.primary_key_arg = "datafile_id"
        self.model = DataFile

    def list(self, args, render_format):
        """
        Display list of datafile records.
        """
        # pylint: disable=no-self-use
        datafiles = DataFile.list(
            args.dataset, args.directory, args.filename, args.filter,
            args.limit, args.offset, args.order_by)
        print(render(datafiles, render_format))

    def get(self, args, render_format):
        """
        Display datafile record.
        """
        # pylint: disable=no-self-use
        datafile = DataFile.objects.get(id=args.datafile_id)
        print(render(datafile, render_format))

    def create(self, args, render_format):
        """
        Create datafile record(s) for an existing file or for all files
        within a directory.
        """
        # pylint: disable=no-self-use
        if os.path.isdir(args.path):
            num_created = DataFile.create_datafiles(
                args.dataset_id, args.storagebox, args.dataset_path, args.path)
            print("%s datafiles created." % num_created)
        else:
            datafile = DataFile.create_datafile(
                args.dataset_id, args.storagebox, args.dataset_path, args.path)
            print(render(datafile, render_format))
            print("DataFile created successfully.")

    def download(self, args, _render_format):
        """
        Download datafile.
        """
        # pylint: disable=no-self-use
        DataFile.download(args.datafile_id)

    def upload(self, args, _render_format):
        """
        Upload datafile.
        """
        # pylint: disable=no-self-use
        DataFile.upload(
            args.dataset_id, args.storagebox, args.dataset_path,
            args.file_path)

    def update(self, args, render_format):
        """
        Update datafile record.
        """
        # pylint: disable=no-self-use
        datafile = DataFile.update(args.datafile_id, args.md5sum)
        print(render(datafile, render_format))
        print("DataFile updated successfully.")

    def verify(self, args, _render_format):
        """
        Ask MyTardis to verify a datafile.
        """
        # pylint: disable=no-self-use
        DataFile.verify(args.datafile_id)
