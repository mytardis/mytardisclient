"""
argparser/schema.py
"""
import textwrap


def build_schema_parser(argument_parser):
    """
    Builds parsing rules for schema-related
    command-line interface arguments.
    """
    schema_help = \
        "Display a list of schema records or a single schema record."
    schema_usage = "mytardis schema [-h] {list,get} ..."
    schema_parser = \
        argument_parser.model_parsers.add_parser("schema",
                                                 help=schema_help,
                                                 usage=schema_usage)
    schema_command_parsers = \
        schema_parser.add_subparsers(help='available commands',
                                     dest='command')

    schema_list_help = "Display a list of schema records."
    schema_list_usage = textwrap.dedent("""\
        mytardis schema list
            [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]

          EXAMPLE

          $ mytardis schema list

          Model: Schema
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/schema/?format=json
          Total Count: 13
          Limit: 20
          Offset: 0

          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | ID |           Name            |                         Namespace                         |       Type        | Subtype | Immutable | Hidden |
          +====+===========================+===========================================================+===================+=========+===========+========+
          |  1 | Publication               | http://www.tardis.edu.au/schemas/publication/             | Experiment schema |         | True      | True   |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          |  2 | Draft Publication         | http://www.tardis.edu.au/schemas/publication/draft/       | Experiment schema |         | True      | True   |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          |  3 | Publication Details       | http://www.tardis.edu.au/schemas/publication/details/     | Experiment schema |         | True      | False  |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          |  8 | MyData Default Experiment | http://mytardis.org/schemas/mydata/defaultexperiment      | Experiment schema |         | True      | True   |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | 13 | Sample Dataset Schema     | https://mytardis.org/schemas/sample-dataset-schema        | Dataset schema    |         | False     | False  |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | 12 | Sample Experiment Schema  | https://mytardis.org/schemas/sample-experiment-schema     | Experiment schema |         | False     | False  |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
        """)
    schema_command_list_parser = \
        schema_command_parsers.add_parser("list",
                                          help=schema_list_help,
                                          usage=schema_list_usage)
    schema_command_list_parser.add_argument(
        "--limit", help="Maximum number of results to return.")
    schema_command_list_parser.add_argument(
        "--offset",
        help="Skip this many records from the start of the result set.")
    schema_command_list_parser.add_argument(
        "--order_by", help="Order by this field.")
    schema_command_list_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    schema_get_help = "Display a single schema record."
    schema_get_usage = textwrap.dedent("""\
        mytardis schema get [-h] [--json] schema_id

          EXAMPLE

          $ mytardis schema get 12
          +--------------+-------------------------------------------------------+
          | Schema field |                         Value                         |
          +==============+=======================================================+
          | ID           | 12                                                    |
          +--------------+-------------------------------------------------------+
          | Name         | Sample Experiment Schema                              |
          +--------------+-------------------------------------------------------+
          | Namespace    | https://mytardis.org/schemas/sample-experiment-schema |
          +--------------+-------------------------------------------------------+
          | Type         | Experiment schema                                     |
          +--------------+-------------------------------------------------------+
          | Subtype      |                                                       |
          +--------------+-------------------------------------------------------+
          | Immutable    | False                                                 |
          +--------------+-------------------------------------------------------+
          | Hidden       | False                                                 |
          +--------------+-------------------------------------------------------+

          +------------------+-----------------------+-----------------------+-----------+-------+-----------+---------------+-------+---------+-----------------+
          | ParameterName ID |       Full Name       |         Name          | Data Type | Units | Immutable | Is Searchable | Order | Choices | Comparison Type |
          +==================+=======================+=======================+===========+=======+===========+===============+=======+=========+=================+
          |               33 | Sample Parameter Name | sample_parameter_name | String    |       | False     | False         | 9999  |         | Exact value     |
          +------------------+-----------------------+-----------------------+-----------+-------+-----------+---------------+-------+---------+-----------------+
        """)
    schema_command_get_parser = \
        schema_command_parsers.add_parser("get",
                                          help=schema_get_help,
                                          usage=schema_get_usage)
    schema_command_get_parser.add_argument("schema_id", help="The schema ID.")
    schema_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
