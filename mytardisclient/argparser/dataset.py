"""
argparser/dataset.py
"""
import textwrap


def build_dataset_parser(argument_parser):
    """
    Builds parsing rules for dataset-related command-line interface arguments.
    """
    # pylint: disable=too-many-locals
    dataset_help = \
        "Display a list of dataset records or a single dataset record."
    dataset_usage = "mytardis dataset [-h] {list,get,create,update} ..."
    dataset_parser = \
        argument_parser.model_parsers.add_parser("dataset",
                                                 help=dataset_help,
                                                 usage=dataset_usage)
    dataset_command_parsers = \
        dataset_parser.add_subparsers(help='available commands',
                                      dest='command')

    dataset_list_help = "Display a list of dataset records."
    dataset_list_usage = textwrap.dedent("""\
        mytardis dataset list
            [--exp EXP] [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]
            [--filter FILTER]

          EXAMPLE
       
          $ mytardis dataset list --exp 20

          Model: Dataset
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/dataset/?format=json&experiments__id=20
          Total Count: 4
          Limit: 20
          Offset: 0

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
    dataset_command_list_parser = \
        dataset_command_parsers.add_parser("list", help=dataset_list_help,
                                           usage=dataset_list_usage)
    dataset_command_list_parser.add_argument("--exp",
                                             help="The experiment ID.")
    dataset_command_list_parser.add_argument(
        "--limit", help="Maximum number of results to return.")
    dataset_command_list_parser.add_argument(
        "--offset",
        help="Skip this many records from the start of the result set.")
    dataset_command_list_parser.add_argument(
        "--order_by",
        help="Order by this field.")
    dataset_command_list_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")
    dataset_command_list_parser.add_argument(
        "--filter", help="Filter on these fields, e.g. \"description=Dataset Description\".")

    dataset_get_help = "Display a single dataset record."
    dataset_get_usage = textwrap.dedent("""\
        mytardis dataset get [-h] [--json] dataset_id

          EXAMPLE

          Suppose we want to retrieve a dataset record with dataset_id=35.
          The "mytardis dataset get 35" command will also display any
          dataset parameters associated with the dataset and any
          datafiles associated with it.  The datafile query could result
          in pagination.  If "Total Count" (below) is greater
          than "Limit", then there are additional pages of datafiles
          not shown in the dataset view below.

          $ mytardis dataset get 35
          +---------------+------------------------+
          | Dataset field |         Value          |
          +===============+========================+
          | ID            | 35                     |
          +---------------+------------------------+
          | Experiment(s) | /api/v1/experiment/24/ |
          +---------------+------------------------+
          | Description   | James Test Dataset 004 |
          +---------------+------------------------+
          | Instrument    | None                   |
          +---------------+------------------------+

          +---------------------+---------------------+------------------------+-------------------------+-----------------+----------------+---------+
          | DatasetParameter ID |       Schema        |     Parameter Name     |      String Value       | Numerical Value | Datetime Value | Link ID |
          +=====================+=====================+========================+=========================+=================+================+=========+
          |                   1 | Test dataset schema | Example Parameter Name | Example Parameter Value |                 |                |         |
          +---------------------+---------------------+------------------------+-------------------------+-----------------+----------------+---------+


          Model: DataFile
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/dataset_file/?format=json&dataset__id=35
          Total Count: 2
          Limit: 20
          Offset: 0

          +--------------+-----------+-----------+-------------------------------------+----------+-----------+----------------------------------+
          | DataFile ID  | Directory | Filename  |                 URI                 | Verified |   Size    |             MD5 Sum              |
          +==============+===========+===========+=====================================+==========+===========+==================================+
          |          120 |           | hello.txt | James Test Dataset 004-35/hello.txt | True     |  25 bytes | 214e52fcf7f98d9fb8588b42cfb7987f |
          +--------------+-----------+-----------+-------------------------------------+----------+-----------+----------------------------------+
          |          121 |           | test.txt  | James Test Dataset 004-35/test.txt  | False    |   8 bytes | 74119cb1c9568b96feb7fa392006e40f |
          +--------------+-----------+-----------+-------------------------------------+----------+-----------+----------------------------------+
        """)
    dataset_command_get_parser = \
        dataset_command_parsers.add_parser("get", help=dataset_get_help,
                                           usage=dataset_get_usage)
    dataset_command_get_parser.add_argument("dataset_id",
                                            help="The dataset ID.")
    dataset_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    dataset_create_help = "Create a dataset record."
    dataset_create_usage = textwrap.dedent("""\
        mytardis dataset create
            [--instrument INSTRUMENT] [--params PARAMS] experiment_id description

          EXAMPLE

          First let's look up a dataset schema we can use to add some
          metadata to the new experiment record.

          $ mytardis schema list

          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | ID |           Name            |                         Namespace                         |       Type        | Subtype | Immutable | Hidden |
          +====+===========================+===========================================================+===================+=========+===========+========+
           ...  ...                         ...                                                         ...                 ...       ...         ...
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+
          | 13 | Sample Dataset Schema     | https://mytardis.org/schemas/sample-dataset-schema        | Dataset schema    |         | False     | False  |
          +----+---------------------------+-----------------------------------------------------------+-------------------+---------+-----------+--------+

          "mytardis schema get <schema_id>" displays the parameters
          associated with this schema:

          $ mytardis schema get 13
          +--------------+----------------------------------------------------+
          | Schema field |                       Value                        |
          +==============+====================================================+
          | ID           | 13                                                 |
          +--------------+----------------------------------------------------+
          | Name         | Sample Dataset Schema                              |
          +--------------+----------------------------------------------------+
          | Namespace    | https://mytardis.org/schemas/sample-dataset-schema |
          +--------------+----------------------------------------------------+
          | Type         | Dataset schema                                     |
          +--------------+----------------------------------------------------+
          | Subtype      |                                                    |
          +--------------+----------------------------------------------------+
          | Immutable    | False                                              |
          +--------------+----------------------------------------------------+
          | Hidden       | False                                              |
          +--------------+----------------------------------------------------+

          +------------------+-----------------------+-----------------------+-----------+-------+-----------+---------------+-------+---------+-----------------+
          | ParameterName ID |       Full Name       |         Name          | Data Type | Units | Immutable | Is Searchable | Order | Choices | Comparison Type |
          +==================+=======================+=======================+===========+=======+===========+===============+=======+=========+=================+
          |               34 | Sample Parameter Name | sample_parameter_name | String    |       | False     | False         | 9999  |         | Exact value     |
          +------------------+-----------------------+-----------------------+-----------+-------+-----------+---------------+-------+---------+-----------------+

          Now that we know the schema's namespace, the parameter name(s) and
          their data type(s), we can create some dataset metadata.

          Below we use cat to create the metadata file, but you can use
          any text editor.

          $ cat << EOF > params.json
          [
              {
                  "schema": "https://mytardis.org/schemas/sample-dataset-schema",
                  "parameters": [
                      {
                          "name": "sample_parameter_name",
                          "value": "Sample Parameter Value"
                      }
                  ]
              }
          ]
          EOF

          Now we create the dataset record (and associate it with experiment
          ID 20) , using the metadata file we just created:

          $ mytardis dataset create --params params.json 20 "Dataset With Params"
          +---------------+------------------------+
          | Dataset field |         Value          |
          +===============+========================+
          | ID            | 39                     |
          +---------------+------------------------+
          | Experiment(s) | /api/v1/experiment/20/ |
          +---------------+------------------------+
          | Description   | Dataset With Params    |
          +---------------+------------------------+
          | Instrument    | None                   |
          +---------------+------------------------+

          +---------------------+-----------------------+-----------------------+------------------------+-----------------+----------------+---------+
          | DatasetParameter ID |        Schema         |    Parameter Name     |      String Value      | Numerical Value | Datetime Value | Link ID |
          +=====================+=======================+=======================+========================+=================+================+=========+
          |                   3 | Sample Dataset Schema | Sample Parameter Name | Sample Parameter Value |                 |                |         |
          +---------------------+-----------------------+-----------------------+------------------------+-----------------+----------------+---------+

          Dataset created successfully.
                """)
    dataset_command_create_parser = \
        dataset_command_parsers.add_parser("create",
                                           help=dataset_create_help,
                                           usage=dataset_create_usage)
    dataset_command_create_parser.add_argument(
        "experiment_id", help="The experiment ID.")
    dataset_command_create_parser.add_argument(
        "description", help="The dataset description.")
    dataset_command_create_parser.add_argument("--instrument",
                                               help="The instrument ID.")
    dataset_command_create_parser.add_argument(
        "--params", help="A JSON file containing dataset parameters.")

    dataset_update_help = "Update a dataset record."
    dataset_update_usage = textwrap.dedent("""\
        mytardis dataset update
            [--description DESCRIPTION] dataset_id

          EXAMPLE
          $ mytardis dataset update --description "Renamed Dataset" 39
          HTTP 401
          Traceback (most recent call last):
            ...
          Exception

          Dataset updates are not yet enabled in the MyTardis API.
          See the "update_detail" method in tardis/tardis_portal/api.py
        """)
    dataset_cmd_update_parser = \
        dataset_command_parsers.add_parser("update",
                                           help=dataset_update_help,
                                           usage=dataset_update_usage)
    dataset_cmd_update_parser.add_argument(
        "dataset_id", help="The ID of the dataset to update.")
    dataset_cmd_update_parser.add_argument(
        "--description", help="The new description of the dataset.")
