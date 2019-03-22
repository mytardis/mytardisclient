"""
argparser/storagebox.py
"""
import textwrap


def build_storagebox_parser(argument_parser):
    """
    Builds parsing rules for storagebox-related
    command-line interface arguments.
    """
    storagebox_help = \
        "Display a list of storage box records or a single storage box record."
    storagebox_usage = "mytardis storagebox [-h] {list,get} ..."
    storagebox_parser = \
        argument_parser.model_parsers.add_parser("storagebox",
                                                 help=storagebox_help,
                                                 usage=storagebox_usage)
    storagebox_command_parsers = \
        storagebox_parser.add_subparsers(help='available commands',
                                         dest='command')

    storagebox_list_help = "Display a list of storage box records."
    storagebox_list_usage = textwrap.dedent("""\
        mytardis storagebox list
            [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]

          EXAMPLE

          $ mytardis storagebox list

          Model: StorageBox
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/storagebox/?format=json
          Total Count: 2
          Limit: 20
          Offset: 0

          +----+------------------------------------------------+-----------------+
          | ID |                      Name                      |   Description   |
          +====+================================================+=================+
          |  1 | local box at /opt/mytardis/develop/var/store   | Default Storage |
          +----+------------------------------------------------+-----------------+
          |  2 | local box at /opt/mytardis/develop/var/staging | Default Staging |
          +----+------------------------------------------------+-----------------+
        """)
    storagebox_command_list_parser = \
        storagebox_command_parsers.add_parser("list",
                                              help=storagebox_list_help,
                                              usage=storagebox_list_usage)
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

    storagebox_get_help = "Display a single storage box record."
    storagebox_get_usage = textwrap.dedent("""\
        mytardis storagebox get [-h] [--json] storage_box_id

          EXAMPLE

          $ mytardis storagebox get 2
          +----------------------+-------------------------------------------------------------+
          |   StorageBox field   |                            Value                            |
          +======================+=============================================================+
          | ID                   | 2                                                           |
          +----------------------+-------------------------------------------------------------+
          | Name                 | local box at /opt/mytardis/develop/var/staging              |
          +----------------------+-------------------------------------------------------------+
          | Description          | Default Staging                                             |
          +----------------------+-------------------------------------------------------------+
          | Django Storage Class | tardis.tardis_portal.storage.MyTardisLocalFileSystemStorage |
          +----------------------+-------------------------------------------------------------+
          | Max Size             | 2.842e+10                                                   |
          +----------------------+-------------------------------------------------------------+
          | Status               | dirty                                                       |
          +----------------------+-------------------------------------------------------------+

          +----------------------+-----------------------------------+
          | StorageBoxOption Key |      StorageBoxOption Value       |
          +======================+===================================+
          |             location | /opt/mytardis/develop/var/staging |
          +----------------------+-----------------------------------+

          +-------------------------+--------------------------------+
          | StorageBoxAttribute Key |   StorageBoxAttribute Value    |
          +=========================+================================+
          |            scp_username | mydata                         |
          +-------------------------+--------------------------------+
          |            scp_hostname | mytardisdemo.erc.monash.edu.au |
          +-------------------------+--------------------------------+
        """)
    storagebox_command_get_parser = \
        storagebox_command_parsers.add_parser("get",
                                              help=storagebox_get_help,
                                              usage=storagebox_get_usage)
    storagebox_command_get_parser.add_argument("storage_box_id",
                                               help="The storage box ID.")
    storagebox_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
