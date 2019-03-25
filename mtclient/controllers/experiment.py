"""
Controller class for running commands (list, get, create, update)
on experiment records.
"""
from __future__ import print_function

from mtclient.models.dataset import Dataset
from mtclient.models.experiment import Experiment
from mtclient.views import render

from .cli import ModelCliController


class ExperimentController(ModelCliController):
    """
    Controller class for running commands (list, get, create, update)
    on experiment records.
    """
    def __init__(self):
        super(ExperimentController, self).__init__()
        self.allowed_commands = ["list", "get", "create", "update"]
        self.primary_key_arg = "experiment_id"
        self.model = Experiment

    def list(self, args, render_format):
        """
        Display list of experiment records.
        """
        # pylint: disable=no-self-use
        experiments = Experiment.list(
            args.filter, args.limit, args.offset, args.order_by)
        print(render(experiments, render_format))

    def get(self, args, render_format):
        """
        Display experiment record.
        """
        # pylint: disable=no-self-use
        experiment = Experiment.objects.get(id=args.experiment_id)
        print(render(experiment, render_format))
        if render_format == 'table':
            datasets = Dataset.list(experiment_id=args.experiment_id)
            print(render(datasets, render_format, display_heading=False))

    def create(self, args, render_format):
        """
        Create experiment record.
        """
        # pylint: disable=no-self-use
        experiment = Experiment.create(
            args.title, args.description, args.institution, args.params)
        print(render(experiment, render_format))
        print("Experiment created successfully.")

    def update(self, args, render_format):
        """
        Update experiment record.
        """
        # pylint: disable=no-self-use
        experiment = Experiment.update(
            args.experiment_id, args.title, args.description)
        print(render(experiment, render_format))
        print("Experiment updated successfully.")
