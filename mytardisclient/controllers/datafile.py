"""
Controller class for running commands (list, download, upload, update)
on datafile records.
"""

# from mytardisclient.logs import logger
from mytardisclient.models.datafile import DataFile
from mytardisclient.views import render


class DataFileController(object):
    """
    Controller class for running commands (list, download, put, patch)
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
            return self.list(args.dataset, args.limit, render_format)
        elif command == "download":
            return self.download(args.datafile_id)
        elif command == "upload":
            return self.upload(args.dataset_id, args.file_path)
        elif command == "update":
            return self.update(args.datafile_id, args.md5sum, render_format)

    def list(self, dataset_id, limit, render_format):
        """
        Display list of datafile records.
        """
        datafiles = DataFile.list(self.config, dataset_id=dataset_id,
                                  limit=limit)
        print render(datafiles, render_format)

    def download(self, datafile_id):
        """
        Download datafile.
        """
        DataFile.download(self.config, datafile_id)

    def upload(self, dataset_id, file_path):
        """
        Upload datafile.
        """
        DataFile.upload(self.config, dataset_id, file_path)

    def update(self, datafile_id, md5sum, render_format):
        """
        Update datafile record.
        """
        datafile = DataFile.update(self.config, datafile_id, md5sum)
        print render(datafile, render_format)
        print "DataFile updated successfully."
