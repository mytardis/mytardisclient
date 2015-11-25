"""
argparser/dataset.py
"""
import textwrap


def build_dataset_parser(argument_parser):
    """
    Builds parsing rules for dataset-related command-line interface arguments.
    """
    dataset_parser = argument_parser.model_parsers.add_parser("dataset")
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
    dataset_command_create_parser.add_argument(
        "--params", help="A JSON file containing dataset parameters.")

    dataset_cmd_update_parser = \
        dataset_command_parsers.add_parser("update")
    dataset_cmd_update_parser.add_argument(
        "dataset_id", help="The ID of the dataset to update.")
    dataset_cmd_update_parser.add_argument(
        "--description", help="The new description of the dataset.")
