"""
Controller class for running commands (list, get, download, upload, update)
on datafile records.
"""

from mytardisclient.models.datafile import DataFile
from mytardisclient.views import render


class DataFileController(object):
    """
    Controller class for running commands (list, get, download, upload, update)
    on datafile records.
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
            return self.list(args.dataset, args.directory, args.filename,
                             args.limit, args.offset, args.order_by,
                             render_format)
        elif command == "get":
            return self.get(args.datafile_id, render_format)
        elif command == "create":
            return self.create(args.dataset_id, args.directory,
                               args.storagebox, args.file_path,
                               render_format)
        elif command == "download":
            return self.download(args.datafile_id)
        elif command == "upload":
            return self.upload(args.dataset_id, args.directory, args.file_path)
        elif command == "update":
            return self.update(args.datafile_id, args.md5sum, render_format)

    def list(self, dataset_id, directory, filename,
             limit, offset, order_by, render_format):
        """
        Display list of datafile records.
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        datafiles = DataFile.list(dataset_id, directory, filename,
                                  limit, offset, order_by)
        print render(datafiles, render_format)

    def get(self, datafile_id, render_format):
        """
        Display datafile record.
        """
        # pylint: disable=no-self-use
        datafile = DataFile.get(datafile_id)
        print render(datafile, render_format)

    def create(self, dataset_id, directory, storagebox, file_path,
               render_format):
        """
        Create datafile record for an existing datafile.
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        datafile = DataFile.create(dataset_id, directory,
                                   storagebox, file_path)
        print render(datafile, render_format)
        print "DataFile created successfully."

    def download(self, datafile_id):
        """
        Download datafile.
        """
        # pylint: disable=no-self-use
        DataFile.download(datafile_id)

    def upload(self, dataset_id, directory, file_path):
        """
        Upload datafile.
        """
        # pylint: disable=no-self-use
        DataFile.upload(dataset_id, directory, file_path)

    def update(self, datafile_id, md5sum, render_format):
        """
        Update datafile record.
        """
        # pylint: disable=no-self-use
        datafile = DataFile.update(datafile_id, md5sum)
        print render(datafile, render_format)
        print "DataFile updated successfully."
