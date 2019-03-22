"""
argparser/instrument.py
"""
import textwrap


def build_instrument_parser(argument_parser):
    """
    Builds parsing rules for instrument-related command-line interface arguments.
    """
    # pylint: disable=too-many-locals
    instrument_help = \
        "Display a list of instrument records or a single instrument record."
    instrument_usage = "mytardis instrument [-h] {list,get,create,update} ..."
    instrument_parser = \
        argument_parser.model_parsers.add_parser("instrument",
                                                 help=instrument_help,
                                                 usage=instrument_usage)
    instrument_command_parsers = \
        instrument_parser.add_subparsers(help='available commands',
                                         dest='command')

    instrument_list_help = "Display a list of instrument records."
    instrument_list_usage = textwrap.dedent("""\
        mytardis instrument list
            [--facility FACILITY] [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]

          EXAMPLE
       
          $ mytardis instrument list --facility 1

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
    instrument_command_list_parser = \
        instrument_command_parsers.add_parser("list",
                                              help=instrument_list_help,
                                              usage=instrument_list_usage)
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

    instrument_get_help = "Display a single instrument record."
    instrument_get_usage = textwrap.dedent("""\
        mytardis instrument get [-h] [--json] instrument_id

          EXAMPLE

          $ mytardis instrument get 3

          +------------------+-----------------+
          | Instrument field |      Value      |
          +==================+=================+
          | ID               | 3               |
          +------------------+-----------------+
          | Name             | Test Instrument |
          +------------------+-----------------+
          | Facility         | Demo Facility   |
          +------------------+-----------------+
        """)
    instrument_command_get_parser = \
        instrument_command_parsers.add_parser("get",
                                              help=instrument_get_help,
                                              usage=instrument_get_usage)
    instrument_command_get_parser.add_argument("instrument_id",
                                               help="The instrument ID.")
    instrument_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    instrument_create_help = "Create an instrument record."
    instrument_create_usage = textwrap.dedent("""\
        mytardis instrument create [-h] facility_id name

          EXAMPLE

          $ mytardis instrument create 1 "New Instrument"
          +------------------+----------------+
          | Instrument field |     Value      |
          +==================+================+
          | ID               | 9              |
          +------------------+----------------+
          | Name             | New Instrument |
          +------------------+----------------+
          | Facility         | Demo Facility  |
          +------------------+----------------+

          Instrument created successfully.
        """)
    instrument_cmd_create_parser = \
        instrument_command_parsers.add_parser("create",
                                              help=instrument_create_help,
                                              usage=instrument_create_usage)
    instrument_cmd_create_parser.add_argument(
        "facility_id", help="The ID of the new instrument's facility.")
    instrument_cmd_create_parser.add_argument(
        "name", help="The name of the instrument to create.")

    instrument_update_help = "Update/rename an existing instrument record."
    instrument_update_usage = textwrap.dedent("""\
        mytardis instrument update [-h] [--name NAME] instrument_id

          EXAMPLE

          $ mytardis instrument update --name "Renamed New Instrument" 9

          +------------------+------------------------+
          | Instrument field |         Value          |
          +==================+========================+
          | ID               | 9                      |
          +------------------+------------------------+
          | Name             | Renamed New Instrument |
          +------------------+------------------------+
          | Facility         | Demo Facility          |
          +------------------+------------------------+

          Instrument updated successfully.
        """)
    instrument_cmd_update_parser = \
        instrument_command_parsers.add_parser("update",
                                              help=instrument_update_help,
                                              usage=instrument_update_usage)
    instrument_cmd_update_parser.add_argument(
        "instrument_id", help="The ID of the instrument to update.")
    instrument_cmd_update_parser.add_argument(
        "--name", help="The new name of the instrument.")
