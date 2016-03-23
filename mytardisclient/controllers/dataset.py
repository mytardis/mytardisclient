"""
Controller class for running commands (list, get, create, update)
on dataset records.
"""
from __future__ import print_function

from mytardisclient.models.dataset import Dataset
from mytardisclient.models.datafile import DataFile
from mytardisclient.views import render


class DatasetController(object):
    """
    Controller class for running commands (list, get, create, update)
    on dataset records.
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
            return self.list(args.exp, args.filter,
                             args.limit, args.offset,
                             args.order_by, render_format)
        elif command == "get":
            return self.get(args.dataset_id, render_format)
        elif command == "create":
            return self.create(args.experiment_id, args.description,
                               args.instrument, args.params, render_format)
        elif command == "update":
            return self.update(args.dataset_id, args.description,
                               render_format)

    def list(self, experiment_id, filters, limit, offset, order_by,
             render_format):
        """
        Display list of dataset records.
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        datasets = Dataset.list(experiment_id, filters,
                                limit, offset, order_by)
        print(render(datasets, render_format))

    def get(self, dataset_id, render_format):
        """
        Display dataset record.
        """
        # pylint: disable=no-self-use
        dataset = Dataset.get(dataset_id)
        print(render(dataset, render_format))
        if render_format == 'table':
            datafiles = DataFile.list(dataset_id)
            print(render(datafiles, render_format))

    def create(self, experiment_id, description, instrument_id, params,
               render_format):
        """
        Create dataset record.
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        dataset = Dataset.create(experiment_id, description, instrument_id,
                                 params)
        print(render(dataset, render_format))
        print("Dataset created successfully.")

    def update(self, dataset_id, description, render_format):
        """
        Update dataset record.
        """
        # pylint: disable=no-self-use
        dataset = Dataset.update(dataset_id, description)
        print(render(dataset, render_format))
        print("Dataset updated successfully.")
