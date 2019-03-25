"""
Controller class for running commands (list, get, create, update)
on experiment records.
"""
from __future__ import print_function

from mtclient.models.dataset import Dataset
from mtclient.models.experiment import Experiment
from mtclient.utils import get_render_format
from mtclient.views import render


class ExperimentController(object):
    """
    Controller class for running commands (list, get, create, update)
    on experiment records.
    """
    def run_command(self, args):
        """
        Generic run command method.
        """
        command = args.command
        render_format = get_render_format(args)
        if command == "list":
            return self.list(args.filter, args.limit, args.offset,
                             args.order_by, render_format)
        if command == "get":
            return self.get(args.experiment_id, render_format)
        if command == "create":
            return self.create(args.title, args.description,
                               args.institution, args.params, render_format)
        if command == "update":
            return self.update(args.experiment_id, args.title,
                               args.description, render_format)
        raise Exception("Invalid command: %s" % args.command)

    def list(self, filters, limit, offset, order_by, render_format):
        """
        Display list of experiment records.
        """
        # pylint: disable=no-self-use
        # pylint: disable=too-many-arguments
        experiments = Experiment.list(filters, limit, offset, order_by)
        print(render(experiments, render_format))

    def get(self, experiment_id, render_format):
        """
        Display experiment record.
        """
        # pylint: disable=no-self-use
        experiment = Experiment.objects.get(id=experiment_id)
        print(render(experiment, render_format))
        if render_format == 'table':
            datasets = Dataset.list(experiment_id=experiment_id)
            print(render(datasets, render_format, display_heading=False))

    def create(self, title, description, institution, params, render_format):
        """
        Create experiment record.
        """
        # pylint: disable=no-self-use
        # pylint: disable=too-many-arguments
        experiment = Experiment.create(title, description, institution, params)
        print(render(experiment, render_format))
        print("Experiment created successfully.")

    def update(self, experiment_id, title, description, render_format):
        """
        Update experiment record.
        """
        # pylint: disable=no-self-use
        experiment = \
            Experiment.update(experiment_id, title, description)
        print(render(experiment, render_format))
        print("Experiment updated successfully.")
