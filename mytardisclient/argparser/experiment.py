"""
argparser/experiment.py
"""
import textwrap


def build_experiment_parser(argument_parser):
    """
    Builds parsing rules for experiment-related command-line interface arguments.
    """
    # pylint: disable=too-many-locals
    experiment_help = \
        "Display a list of experiment records or a single experiment record."
    experiment_usage = "mytardis experiment [-h] {list,get,create,update} ..."
    experiment_parser = \
        argument_parser.model_parsers.add_parser("experiment",
                                                 help=experiment_help,
                                                 usage=experiment_usage)
    experiment_command_parsers = \
        experiment_parser.add_subparsers(help='available commands',
                                         dest='command')

    experiment_list_help = "Display a list of experiment records."
    experiment_list_usage = textwrap.dedent("""\
        mytardis experiment list
            [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]
            [--filter FILTER]

          EXAMPLE
       
          $ mytardis experiment list

          Model: Experiment
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/experiment/?format=json
          Total Count: 4
          Limit: 20
          Offset: 0

          +----+-------------------+-----------------------------------+
          | ID |    Institution    |               Title               |
          +====+===================+===================================+
          | 20 | Monash University | James Exp 001                     |
          +----+-------------------+-----------------------------------+
          | 13 | Monash University | A's Test Instrument - Test User1  |
          +----+-------------------+-----------------------------------+
          | 22 | Monash University | James Test Exp 003                |
          +----+-------------------+-----------------------------------+
          | 14 | Monash University | A's Test Instrument - Test User2  |
          +----+-------------------+-----------------------------------+
        """)
    experiment_command_list_parser = \
        experiment_command_parsers.add_parser("list",
                                              help=experiment_list_help,
                                              usage=experiment_list_usage)
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
    experiment_command_list_parser.add_argument(
        "--filter", help="Filter on these fields, e.g. \"title=Exp Title\".")

    experiment_get_help = "Display a single experiment record."
    experiment_get_usage = textwrap.dedent("""\
        mytardis experiment get [-h] [--json] experiment_id

          EXAMPLE

          $ mytardis experiment get 20

          +------------------+-------------------+
          | Experiment field |       Value       |
          +==================+===================+
          | ID               | 20                |
          +------------------+-------------------+
          | Institution      | Monash University |
          +------------------+-------------------+
          | Title            | James Exp 001     |
          +------------------+-------------------+
          | Description      |                   |
          +------------------+-------------------+

          +------------+------------------------+------------------------+------------+
          | Dataset ID |     Experiment(s)      |      Description       | Instrument |
          +============+========================+========================+============+
          |         34 | /api/v1/experiment/20/ | James Test Dataset 001 | None       |
          +------------+------------------------+------------------------+------------+
          |         33 | /api/v1/experiment/20/ | James Test Dataset 003 | None       |
          +------------+------------------------+------------------------+------------+
          |         32 | /api/v1/experiment/20/ | James Test Dataset 002 | None       |
          +------------+------------------------+------------------------+------------+
          |         31 | /api/v1/experiment/20/ | James Test Dataset 001 | None       |
          +------------+------------------------+------------------------+------------+
        """)
    experiment_command_get_parser = \
        experiment_command_parsers.add_parser("get",
                                              help=experiment_get_help,
                                              usage=experiment_get_usage)
    experiment_command_get_parser.add_argument("experiment_id",
                                               help="The experiment ID.")
    experiment_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    experiment_create_help = "Create an experiment record."
    experiment_create_usage = textwrap.dedent("""\
        mytardis experiment create
            [--description DESCRIPTION] [--institution INSTITUTION] [--params PARAMS] title

          EXAMPLE

          First let's look up an experiment schema we can use to add some
          metadata to the new experiment record.

          $ mytardis schema list

          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | ID |           Name            |                         Namespace                         |       Type        | Subtype | Immutable | Hidden |
          +====+===========================+===========================================================+===================+=========+===========+========+
           ...  ...                         ...                                                         ...                 ...       ...         ...
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | 12 | Sample Experiment Schema  | https://mytardis.org/schemas/sample-experiment-schema     | Experiment schema |         | False     | False  |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+

          "mytardis schema get <schema_id>" displays the parameters
          associated with this schema:

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

          Now that we know the schema's namespace, the parameter name(s) and
          their data type(s), we can create some experiment metadata.

          Below we use cat to create the metadata file, but you can use
          any text editor.

          $ cat << EOF > params.json
          [
              {
                  "schema": "https://mytardis.org/schemas/sample-experiment-schema",
                  "parameters": [
                      {
                          "name": "sample_parameter_name",
                          "value": "Sample Parameter Value"
                      }
                  ]
              }
          ]
          EOF

          Now we create the experiment record, using the metadata file
          we just created:

          $ mytardis experiment create --params params.json "Exp With Params"
          +------------------+-------------------+
          | Experiment field |       Value       |
          +==================+===================+
          | ID               | 28                |
          +------------------+-------------------+
          | Institution      | Monash University |
          +------------------+-------------------+
          | Title            | Exp With Params   |
          +------------------+-------------------+
          | Description      |                   |
          +------------------+-------------------+

          +------------------------+--------------------------+-----------------------+------------------------+-----------------+----------------+---------+
          | ExperimentParameter ID |          Schema          |    Parameter Name     |      String Value      | Numerical Value | Datetime Value | Link ID |
          +========================+==========================+=======================+========================+=================+================+=========+
          |                     35 | Sample Experiment Schema | Sample Parameter Name | Sample Parameter Value |                 |                |         |
          +------------------------+--------------------------+-----------------------+------------------------+-----------------+----------------+---------+

          Experiment created successfully.
        """)
    experiment_cmd_create_parser = \
        experiment_command_parsers.add_parser("create",
                                              help=experiment_create_help,
                                              usage=experiment_create_usage)
    experiment_cmd_create_parser.add_argument(
        "title", help="The experiment title to create.")
    experiment_cmd_create_parser.add_argument(
        "--description", help="A description of the experiment.")
    experiment_cmd_create_parser.add_argument(
        "--institution", help="The institution of the experiment.")
    experiment_cmd_create_parser.add_argument(
        "--params", help="A JSON file containing experiment parameters.")

    experiment_update_help = "Update an experiment record."
    experiment_update_usage = textwrap.dedent("""\
        mytardis experiment update
            [--title TITLE] [--description DESCRIPTION] experiment_id

          EXAMPLE
          $ mytardis experiment update --title "Renamed Exp" 20
          +------------------+-------------------+
          | Experiment field |       Value       |
          +==================+===================+
          | ID               | 20                |
          +------------------+-------------------+
          | Institution      | Monash University |
          +------------------+-------------------+
          | Title            | Renamed Exp       |
          +------------------+-------------------+
          | Description      |                   |
          +------------------+-------------------+

          Experiment updated successfully.
        """)
    experiment_cmd_update_parser = \
        experiment_command_parsers.add_parser("update",
                                              help=experiment_update_help,
                                              usage=experiment_update_usage)
    experiment_cmd_update_parser.add_argument(
        "experiment_id", help="The ID of the experiment to update.")
    experiment_cmd_update_parser.add_argument(
        "--title", help="The new title of the experiment.")
    experiment_cmd_update_parser.add_argument(
        "--description", help="The new description of the experiment.")
