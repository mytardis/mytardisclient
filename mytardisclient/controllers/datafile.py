"""
Controller class for running commands (list, get, download, upload, update)
on datafile records.
"""

# from mytardisclient.logs import logger
from mytardisclient.models.datafile import DataFile
from mytardisclient.views import render


class DataFileController(object):
    """
    Controller class for running commands (list, get, download, upload, update)
    on datafile records.
    """
    def __init__(self, config):
        self.config = config

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
        datafiles = DataFile.list(self.config, dataset_id, directory, filename,
                                  limit, offset, order_by)
        print render(datafiles, render_format)

    def get(self, datafile_id, render_format):
        """
        Display datafile record.
        """
        datafile = DataFile.get(self.config, datafile_id)
        print render(datafile, render_format)

    def create(self, dataset_id, directory, storagebox, file_path,
               render_format):
        """
        Create datafile record for an existing datafile.
        """
        datafile = DataFile.create(self.config, dataset_id, directory,
                                   storagebox, file_path)
        print render(datafile, render_format)
        print "DataFile created successfully."

    def download(self, datafile_id):
        """
        Download datafile.
        """
        DataFile.download(self.config, datafile_id)

    def upload(self, dataset_id, directory, file_path):
        """
        Upload datafile.
        """
        DataFile.upload(self.config, dataset_id, directory, file_path)

    def update(self, datafile_id, md5sum, render_format):
        """
        Update datafile record.
        """
        datafile = DataFile.update(self.config, datafile_id, md5sum)
        print render(datafile, render_format)
        print "DataFile updated successfully."
