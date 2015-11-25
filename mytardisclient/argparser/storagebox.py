"""
argparser/storagebox.py
"""
import textwrap


def build_storagebox_parser(argument_parser):
    """
    Builds parsing rules for storagebox-related
    command-line interface arguments.
    """
    storagebox_parser = argument_parser.model_parsers.add_parser("storagebox")
    storagebox_command_parsers = \
        storagebox_parser.add_subparsers(help='available commands',
                                         dest='command')

    storagebox_command_list_parser = storagebox_command_parsers.add_parser("list")
    storagebox_command_list_parser.add_argument(
        "--limit", help="Maximum number of results to return.")
    storagebox_command_list_parser.add_argument(
        "--offset",
        help="Skip this many records from the start of the result set.")
    storagebox_command_list_parser.add_argument(
        "--order_by",
        help="Order by this field.")
    storagebox_command_list_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    storagebox_command_get_parser = \
        storagebox_command_parsers.add_parser("get")
    storagebox_command_get_parser.add_argument("storage_box_id",
                                               help="The storage box ID.")
    storagebox_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
