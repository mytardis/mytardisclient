"""
argparser/api.py
"""
import textwrap


def build_api_parser(argument_parser):
    """
    'mytardis api' allows the user to list API endpoints
    supported by the MyTardis API.
    """
    api_help = "List models accessible via MyTardis's REST API."
    api_parser = argument_parser.model_parsers.add_parser("api", help=api_help)
    api_command_parsers = \
        api_parser.add_subparsers(help='available commands',
                                  dest='command')

    api_list_help = "List models accessible via MyTardis's REST API."
    api_list_usage = textwrap.dedent("""\
        mytardis api list [-h] [--json]

          EXAMPLE

          $ mytardis api list

          API Endpoints
          +------------+---------------------+----------------------------+
          | Model      | List Endpoint       | Schema                     |
          +============+=====================+============================+
          | facility   | /api/v1/facility/   | /api/v1/facility/schema/   |
          +------------+---------------------+----------------------------+
          | instrument | /api/v1/instrument/ | /api/v1/instrument/schema/ |
          +------------+---------------------+----------------------------+
          | experiment | /api/v1/experiment/ | /api/v1/experiment/schema/ |
          +------------+---------------------+----------------------------+
          | dataset    | /api/v1/dataset/    | /api/v1/dataset/schema/    |
          +------------+---------------------+----------------------------+
           ...          ...                   ...
          +------------+---------------------+----------------------------+
        """)
    api_command_list_parser = \
        api_command_parsers.add_parser("list", help=api_list_help,
                                       usage=api_list_usage)
    api_command_list_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    api_get_help = (
        "Display the schema for a particular MyTardis API model, "
        "showing which fields are accesible via the API, which fields "
        "support filtering, and which fields support ordering.")
    api_get_usage = textwrap.dedent("""\
        mytardis api get [-h] [--json] api_model

          EXAMPLE

          $ mytardis api get facility
          +------------------+------------------------------------------+
          | API Schema field |                   Value                  |
          +==================+==========================================+
          | Model            | facility                                 |
          +------------------+------------------------------------------+
          | Fields           | id                                       |
          |                  | manager_group                            |
          |                  | name                                     |
          |                  | resource_uri                             |
          +------------------+------------------------------------------+
          | Filtering        | {                                        |
          |                  |   "id": [                                |
          |                  |     "exact"                              |
          |                  |   ],                                     |
          |                  |   "manager_group": "ALL_WITH_RELATIONS", |
          |                  |   "name": [                              |
          |                  |     "exact"                              |
          |                  |   ]                                      |
          |                  | }                                        |
          +------------------+------------------------------------------+
          | Ordering         | {}                                       |
          +------------------+------------------------------------------+
        """)
    api_command_get_parser = \
        api_command_parsers.add_parser("get", help=api_get_help,
                                       usage=api_get_usage)
    api_command_get_parser.add_argument("api_model", help="The model name.")
    api_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
