"""
argparser/uploader.py
"""
import textwrap


def build_uploader_parser(argument_parser):
    """
    Builds parsing rules for uploader-related
    command-line interface arguments.
    """
    uploader_help = \
        "Display a list of uploader records or a single uploader record."
    uploader_usage = "mytardis uploader [-h] {list,get} ..."
    uploader_parser = \
        argument_parser.model_parsers.add_parser("uploader",
                                                 help=uploader_help,
                                                 usage=uploader_usage)
    uploader_command_parsers = \
        uploader_parser.add_subparsers(help='available commands',
                                     dest='command')

    uploader_list_help = "Display a list of uploader records."
    uploader_list_usage = textwrap.dedent("""\
        mytardis uploader list
            [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]
        """)
    uploader_command_list_parser = \
        uploader_command_parsers.add_parser("list",
                                          help=uploader_list_help,
                                          usage=uploader_list_usage)
    uploader_command_list_parser.add_argument(
        "--limit", help="Maximum number of results to return.")
    uploader_command_list_parser.add_argument(
        "--offset",
        help="Skip this many records from the start of the result set.")
    uploader_command_list_parser.add_argument(
        "--order_by", help="Order by this field.")
    uploader_command_list_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    uploader_get_help = "Display a single uploader record."
    uploader_get_usage = textwrap.dedent("""\
        mytardis uploader get [-h] [--json] uploader_id
        """)
    uploader_command_get_parser = \
        uploader_command_parsers.add_parser("get",
                                          help=uploader_get_help,
                                          usage=uploader_get_usage)
    uploader_command_get_parser.add_argument("uploader_id", help="The uploader ID.")
    uploader_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
