"""
Controller class for running commands (list, get, create, update)
on experiment records.
"""

# from mytardisclient.logs import logger
from mytardisclient.models.dataset import Dataset
from mytardisclient.models.experiment import Experiment
from mytardisclient.views import render


class ExperimentController(object):
    """
    Controller class for running commands (list, get, put, patch)
    on experiment records.
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
            return self.list(args.limit, render_format)
        elif command == "get":
            return self.get(args.experiment_id, render_format)
        elif command == "create":
            return self.create(args.experiment_title, render_format)
        elif command == "update":
            return self.update(args.experiment_id, args.title,
                               args.description, render_format)

    def list(self, limit, render_format):
        """
        Display list of experiment records.
        """
        experiments = Experiment.list(self.config, limit=limit)
        print render(experiments, render_format)

    def get(self, experiment_id, render_format):
        """
        Display experiment record.
        """
        experiment = Experiment.get(self.config, experiment_id)
        print render(experiment, render_format)
        if render_format == 'table':
            datasets = Dataset.list(self.config, experiment_id=experiment_id)
            print render(datasets, render_format)

    def create(self, experiment_title, render_format):
        """
        Create experiment record.
        """
        experiment = Experiment.create(self.config, experiment_title)
        print render(experiment, render_format)
        print "Experiment created successfully."

    def update(self, experiment_id, experiment_title,
               experiment_description, render_format):
        """
        Update experiment record.
        """
        experiment = \
            Experiment.update(self.config, experiment_id,
                              experiment_title, experiment_description)
        print render(experiment, render_format)
        print "Experiment updated successfully."
