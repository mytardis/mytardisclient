"""
argparser/experiment.py
"""
import textwrap


def build_experiment_parser(argument_parser):
    """
    Builds parsing rules for experiment-related command-line interface arguments.
    """
    experiment_parser = argument_parser.model_parsers.add_parser("experiment")
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
        "title", help="The experiment title to create.")
    experiment_cmd_create_parser.add_argument(
        "--description", help="A description of the experiment.")
    experiment_cmd_create_parser.add_argument(
        "--institution", help="The institution of the experiment.")
    experiment_cmd_create_parser.add_argument(
        "--params", help="A JSON file containing experiment parameters.")

    experiment_cmd_update_parser = \
        experiment_command_parsers.add_parser("update")
    experiment_cmd_update_parser.add_argument(
        "experiment_id", help="The ID of the experiment to update.")
    experiment_cmd_update_parser.add_argument(
        "--title", help="The new title of the experiment.")
    experiment_cmd_update_parser.add_argument(
        "--description", help="The new description of the experiment.")
