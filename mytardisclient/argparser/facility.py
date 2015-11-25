"""
argparser/facility.py
"""
import textwrap


def build_facility_parser(argument_parser):
    """
    Builds parsing rules for facility-related
    command-line interface arguments.
    """
    facility_help = \
        "Display a list of facility records or a single facility record."
    facility_usage = "mytardis facility [-h] {list,get} ..."
    facility_parser = \
        argument_parser.model_parsers.add_parser("facility",
                                                 help=facility_help,
                                                 usage=facility_usage)
    facility_command_parsers = \
        facility_parser.add_subparsers(help='available commands',
                                       dest='command')

    facility_list_help = "Display a list of facility records."
    facility_list_usage = textwrap.dedent("""\
        mytardis facility list
            [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]

          EXAMPLE

          $ mytardis facility list

          Model: Facility
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/facility/?format=json
          Total Count: 2
          Limit: 20
          Offset: 0

          +----+---------------+------------------------+
          | ID |     Name      |     Manager Group      |
          +====+===============+========================+
          |  1 | Demo Facility | demo-facility-managers |
          +----+---------------+------------------------+
          |  2 | Test Facility | test-facility-managers |
          +----+---------------+------------------------+
        """)
    facility_command_list_parser = \
        facility_command_parsers.add_parser("list", help=facility_list_help,
                                            usage=facility_list_usage)
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

    facility_get_help = "Display a single facility record."
    facility_get_usage = textwrap.dedent("""\
        mytardis facility get [-h] [--json] facility_id

          EXAMPLE

          $ mytardis facility get 1

          Model: Facility

          +----------------+------------------------+
          | Facility field |         Value          |
          +================+========================+
          | ID             | 1                      |
          +----------------+------------------------+
          | Name           | Demo Facility          |
          +----------------+------------------------+
          | Manager Group  | demo-facility-managers |
          +----------------+------------------------+


          Model: Instrument
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/instrument/?format=json&facility__id=1
          Total Count: 3
          Limit: 20
          Offset: 0

          +----+-------------------------+---------------+
          | ID |          Name           |   Facility    |
          +====+=========================+===============+
          |  3 | Test Instrument         | Demo Facility |
          +----+-------------------------+---------------+
          |  4 | Beamline                | Demo Facility |
          +----+-------------------------+---------------+
          |  8 | James Test Instrument   | Demo Facility |
          +----+-------------------------+---------------+
        """)
    facility_command_get_parser = \
        facility_command_parsers.add_parser("get", help=facility_get_help,
                                            usage=facility_get_usage)
    facility_command_get_parser.add_argument("facility_id",
                                             help="The facility ID.")
    facility_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
