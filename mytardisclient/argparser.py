"""
argparser.py
"""
from argparse import ArgumentParser


class ArgParser(object):
    """
    Defines parsing rules for command-line interface arguments.
    """
    def __init__(self):
        self.parser = ArgumentParser(prog='mytardis', description="")
        self.model_parsers = \
            self.parser.add_subparsers(help='available models', dest='model')

    def get_args(self):
        """
        Builds argument parser and retrieves arguments.
        """
        self.build_parser()
        args = self.parser.parse_args()

        if args.model not in ('config', 'facility', 'instrument',
                              'experiment', 'dataset', 'datafile'):
            self.parser.error(
                "model should be one of 'config', 'facility', "
                "'instrument', 'experiment', 'dataset', 'datafile'.")

        return args

    def build_parser(self):
        """
        Builds parsing rules for command-line interface arguments.
        """
        self.build_config_parser()
        self.build_facility_parser()
        self.build_instrument_parser()
        self.build_experiment_parser()
        self.build_dataset_parser()
        self.build_datafile_parser()

        return self.parser

    def build_config_parser(self):
        """
        'mytardis config' prompts users for settings to write to
        ~/.config/mytardisclient/mytardisclient.cfg
        """
        self.model_parsers.add_parser("config")

    def build_facility_parser(self):
        """
        Builds parsing rules for facility-related command-line interface arguments.
        """
        facility_parser = self.model_parsers.add_parser("facility")
        facility_command_parsers = \
            facility_parser.add_subparsers(help='available commands',
                                           dest='command')
        facility_command_list_parser = facility_command_parsers.add_parser("list")
        facility_command_list_parser.add_argument(
            "--limit", help="Maximum number of results to return.")
        facility_command_list_parser.add_argument(
            "--offset",
            help="Skip this many records from the start of the result set.")
        facility_command_list_parser.add_argument(
            "--order_by",
            help="Order by this field.")
        facility_command_list_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        facility_command_get_parser = \
            facility_command_parsers.add_parser("get")
        facility_command_get_parser.add_argument("facility_id",
                                                 help="The facility ID.")
        facility_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")

    def build_instrument_parser(self):
        """
        Builds parsing rules for instrument-related command-line interface arguments.
        """
        instrument_parser = self.model_parsers.add_parser("instrument")
        instrument_command_parsers = \
            instrument_parser.add_subparsers(help='available commands',
                                             dest='command')
        instrument_command_list_parser = \
            instrument_command_parsers.add_parser("list")
        instrument_command_list_parser.add_argument("--facility",
                                                    help="The facility ID.")
        instrument_command_list_parser.add_argument(
            "--limit", help="Maximum number of results to return.")
        instrument_command_list_parser.add_argument(
            "--offset",
            help="Skip this many records from the start of the result set.")
        instrument_command_list_parser.add_argument(
            "--order_by",
            help="Order by this field.")
        instrument_command_list_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        instrument_command_get_parser = \
            instrument_command_parsers.add_parser("get")
        instrument_command_get_parser.add_argument("instrument_id",
                                                   help="The instrument ID.")
        instrument_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        instrument_cmd_create_parser = \
            instrument_command_parsers.add_parser("create")
        instrument_cmd_create_parser.add_argument(
            "facility_id", help="The ID of the new instrument's facility.")
        instrument_cmd_create_parser.add_argument(
            "name", help="The name of the instrument to create.")
        instrument_cmd_update_parser = \
            instrument_command_parsers.add_parser("update")
        instrument_cmd_update_parser.add_argument(
            "instrument_id", help="The ID of the instrument to update.")
        instrument_cmd_update_parser.add_argument(
            "--name", help="The new name of the instrument.")

    def build_experiment_parser(self):
        """
        Builds parsing rules for experiment-related command-line interface arguments.
        """
        experiment_parser = self.model_parsers.add_parser("experiment")
        experiment_command_parsers = \
            experiment_parser.add_subparsers(help='available commands',
                                             dest='command')
        experiment_command_list_parser = experiment_command_parsers.add_parser("list")
        experiment_command_list_parser.add_argument(
            "--limit", help="Maximum number of results to return.")
        experiment_command_list_parser.add_argument(
            "--offset",
            help="Skip this many records from the start of the result set.")
        experiment_command_list_parser.add_argument(
            "--order_by",
            help="Order by this field.")
        experiment_command_list_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        experiment_command_get_parser = \
            experiment_command_parsers.add_parser("get")
        experiment_command_get_parser.add_argument("experiment_id",
                                                   help="The experiment ID.")
        experiment_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        experiment_cmd_create_parser = \
            experiment_command_parsers.add_parser("create")
        experiment_cmd_create_parser.add_argument(
            "experiment_title", help="The experiment title to create.")
        experiment_cmd_update_parser = \
            experiment_command_parsers.add_parser("update")
        experiment_cmd_update_parser.add_argument(
            "experiment_id", help="The ID of the experiment to update.")
        experiment_cmd_update_parser.add_argument(
            "--title", help="The new title of the experiment.")
        experiment_cmd_update_parser.add_argument(
            "--description", help="The new description of the experiment.")

    def build_dataset_parser(self):
        """
        Builds parsing rules for dataset-related command-line interface arguments.
        """
        dataset_parser = self.model_parsers.add_parser("dataset")
        dataset_command_parsers = \
            dataset_parser.add_subparsers(help='available commands',
                                          dest='command')
        dataset_command_list_parser = dataset_command_parsers.add_parser("list")
        dataset_command_list_parser.add_argument("--exp",
                                                 help="The experiment ID.")
        dataset_command_list_parser.add_argument(
            "--limit", help="Maximum number of results to return.")
        dataset_command_list_parser.add_argument(
            "--offset",
            help="Skip this many records from the start of the result set.")
        dataset_command_list_parser.add_argument(
            "--order_by",
            help="Order by this field.")
        dataset_command_list_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        dataset_command_get_parser = dataset_command_parsers.add_parser("get")
        dataset_command_get_parser.add_argument("dataset_id",
                                                help="The dataset ID.")
        dataset_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        dataset_command_create_parser = \
            dataset_command_parsers.add_parser("create")
        dataset_command_create_parser.add_argument(
            "experiment_id", help="The experiment ID.")
        dataset_command_create_parser.add_argument(
            "description", help="The dataset description.")
        dataset_command_create_parser.add_argument("--instrument",
                                                   help="The instrument ID.")
        dataset_cmd_update_parser = \
            dataset_command_parsers.add_parser("update")
        dataset_cmd_update_parser.add_argument(
            "dataset_id", help="The ID of the dataset to update.")
        dataset_cmd_update_parser.add_argument(
            "--description", help="The new description of the dataset.")

    def build_datafile_parser(self):
        """
        Builds parsing rules for datafile-related command-line interface arguments.
        """
        datafile_parser = self.model_parsers.add_parser("datafile")
        datafile_command_parsers = \
            datafile_parser.add_subparsers(help='available commands',
                                           dest='command')
        datafile_command_list_parser = datafile_command_parsers.add_parser("list")
        datafile_command_list_parser.add_argument("--dataset",
                                                  help="The dataset ID.")
        datafile_command_list_parser.add_argument(
            "--limit", help="Maximum number of results to return.")
        datafile_command_list_parser.add_argument(
            "--offset",
            help="Skip this many records from the start of the result set.")
        datafile_command_list_parser.add_argument(
            "--order_by",
            help="Order by this field.")
        datafile_command_list_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        datafile_command_get_parser = datafile_command_parsers.add_parser("get")
        datafile_command_get_parser.add_argument("dataset_id",
                                                 help="The dataset ID.")
        datafile_command_get_parser.add_argument("--directory",
                                                 help="The subdirectory within the dataset.")
        datafile_command_get_parser.add_argument("filename",
                                                 help="The datafile's name.")
        datafile_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")
        datafile_command_create_parser = \
            datafile_command_parsers.add_parser("create")
        datafile_command_create_parser.add_argument(
            "dataset_id", help="The dataset ID.")
        datafile_command_create_parser.add_argument(
            "--directory", help="The subdirectory within the dataset.")
        datafile_command_create_parser.add_argument(
            "--storagebox", help="The storage box containing the datafile.")
        datafile_command_create_parser.add_argument(
            "file_path", help="The file to be represented in the datafile record.")
        datafile_cmd_download_parser = datafile_command_parsers.add_parser("download")
        datafile_cmd_download_parser.add_argument("datafile_id",
                                                  help="The datafile ID.")
        datafile_cmd_upload_parser = datafile_command_parsers.add_parser("upload")
        datafile_cmd_upload_parser.add_argument("dataset_id",
                                                help="The dataset ID.")
        datafile_cmd_upload_parser.add_argument(
            "--directory",
            help="The datafile's subdirectory within the dataset.")
        datafile_cmd_upload_parser.add_argument("file_path",
                                                help="The file to upload.")
        datafile_cmd_update_parser = \
            datafile_command_parsers.add_parser("update")
        datafile_cmd_update_parser.add_argument(
            "datafile_id", help="The ID of the datafile to update.")
        datafile_cmd_update_parser.add_argument(
            "--md5sum", help="The new MD5 sum of the datafile.")
