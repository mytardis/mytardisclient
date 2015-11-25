"""
argparser/schema.py
"""
import textwrap


def build_schema_parser(argument_parser):
    """
    Builds parsing rules for schema-related
    command-line interface arguments.
    """
    schema_parser = argument_parser.model_parsers.add_parser("schema")
    schema_command_parsers = \
        schema_parser.add_subparsers(help='available commands',
                                     dest='command')

    schema_command_list_parser = schema_command_parsers.add_parser("list")
    schema_command_list_parser.add_argument(
        "--limit", help="Maximum number of results to return.")
    schema_command_list_parser.add_argument(
        "--offset",
        help="Skip this many records from the start of the result set.")
    schema_command_list_parser.add_argument(
        "--order_by", help="Order by this field.")
    schema_command_list_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    schema_command_get_parser = \
        schema_command_parsers.add_parser("get")
    schema_command_get_parser.add_argument("schema_id", help="The schema ID.")
    schema_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
