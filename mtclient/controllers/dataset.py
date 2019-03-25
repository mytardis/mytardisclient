"""
Controller class for running commands (list, get, create, update)
on dataset records.
"""
from __future__ import print_function

from mtclient.models.dataset import Dataset
from mtclient.views import render

from .cli import ModelCliController


class DatasetController(ModelCliController):
    """
    Controller class for running commands (list, get, create, update)
    on dataset records.
    """
    def __init__(self):
        super(DatasetController, self).__init__()
        self.allowed_commands = ["list", "get", "create", "update", "download"]
        self.primary_key_arg = "dataset_id"
        self.model = Dataset

    def list(self, args, render_format):
        """
        Display list of dataset records.
        """
        # pylint: disable=no-self-use
        datasets = Dataset.list(
            args.exp, args.filter, args.limit, args.offset, args.order_by)
        print(render(datasets, render_format))

    def get(self, args, render_format):
        """
        Display dataset record.
        """
        # pylint: disable=no-self-use
        dataset = Dataset.objects.get(id=args.dataset_id)
        print(render(dataset, render_format))
        if render_format == 'table':
            from mtclient.models.datafile import DataFile
            datafiles = DataFile.list(args.dataset_id)
            print(render(datafiles, render_format))

    def create(self, args, render_format):
        """
        Create dataset record.
        """
        # pylint: disable=no-self-use
        dataset = Dataset.create(
            args.experiment_id, args.description, args.instrument, args.params)
        print(render(dataset, render_format))
        print("Dataset created successfully.")

    def update(self, args, render_format):
        """
        Update dataset record.
        """
        # pylint: disable=no-self-use
        dataset = Dataset.update(args.dataset_id, args.description)
        print(render(dataset, render_format))
        print("Dataset updated successfully.")

    def download(self, args, _render_format):
        """
        Download dataset.
        """
        # pylint: disable=no-self-use
        Dataset.download(args.dataset_id)
