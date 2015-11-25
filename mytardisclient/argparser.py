"""
argparser.py
"""
from argparse import ArgumentParser
import textwrap


class ArgParser(object):
    """
    Defines parsing rules for command-line interface arguments.
    """
    def __init__(self):
        description = "Command-line interface for MyTardis REST API."
        self.parser = ArgumentParser(prog='mytardis', description=description)
        self.parser.add_argument(
            "--verbose", action='store_true', help="More verbose output.")
        self.model_parsers = \
            self.parser.add_subparsers(help='available models', dest='model')

    def get_args(self):
        """
        Builds argument parser and retrieves arguments.
        """
        self.build_parser()
        args = self.parser.parse_args()

        if args.model not in ('api', 'config', 'version',
                              'facility', 'instrument',
                              'experiment', 'dataset', 'datafile',
                              'storagebox', 'schema'):
            self.parser.error(
                "model should be one of 'api', 'config', 'version', "
                "'facility', 'instrument', "
                "'experiment', 'dataset', 'datafile', 'storagebox', "
                "'schema'.")

        return args

    def build_parser(self):
        """
        Builds parsing rules for command-line interface arguments.
        """
        self.build_api_parser()
        self.build_config_parser()
        self.build_version_parser()
        self.build_facility_parser()
        self.build_instrument_parser()
        self.build_experiment_parser()
        self.build_dataset_parser()
        self.build_datafile_parser()
        self.build_storagebox_parser()
        self.build_schema_parser()

        return self.parser

    def build_api_parser(self):
        """
        'mytardis api' allows the user to list API endpoints
        supported by the MyTardis API.
        """
        api_help = "List models accessible via MyTardis's REST API."
        api_parser = self.model_parsers.add_parser("api", help=api_help)
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

    def build_config_parser(self):
        """
        'mytardis config' prompts users for settings to write to
        mytardisclient.models.config.DEFAULT_CONFIG_PATH
        """
        config_help = "Set MyTardis URL, username and API key."
        config_usage = textwrap.dedent("""\
            mytardis config [-h]

              EXAMPLE

              $ mytardis config
              MyTardis URL? http://mytardisdemo.erc.monash.edu.au
              MyTardis Username? demofacility
              MyTardis API key? 644be179cc6773c30fc471bad61b50c90897146c

              Wrote settings to /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
            """)
        self.model_parsers.add_parser("config", help=config_help,
                                      usage=config_usage)

    def build_version_parser(self):
        """
        Displays the mytardisclient version
        """
        version_help = "Display the MyTardis Client version."
        version_usage = textwrap.dedent("""\
            mytardis version [-h]

            $ mytardis version
            MyTardis Client v0.0.1""")
        self.model_parsers.add_parser("version", help=version_help,
                                      usage=version_usage)

    def build_facility_parser(self):
        """
        Builds parsing rules for facility-related
        command-line interface arguments.
        """
        facility_help = \
            "Display a list of facility records or a single facility record."
        facility_usage = "mytardis facility [-h] {list,get} ..."
        facility_parser = \
            self.model_parsers.add_parser("facility", help=facility_help,
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

    def build_instrument_parser(self):
        """
        Builds parsing rules for instrument-related command-line interface arguments.
        """
        # pylint: disable=too-many-locals
        instrument_help = \
            "Display a list of instrument records or a single instrument record."
        instrument_usage = "mytardis instrument [-h] {list,get,create,update} ..."
        instrument_parser = \
            self.model_parsers.add_parser("instrument", help=instrument_help,
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

    def build_experiment_parser(self):
        """
        Builds parsing rules for experiment-related command-line interface arguments.
        """
        experiment_parser = self.model_parsers.add_parser("experiment")
        experiment_command_parsers = \
            experiment_parser.add_subparsers(help='available commands',
                                             dest='command')

        experiment_command_list_parser = experiment_command_parsers.add_parser("list")
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

        experiment_command_get_parser = \
            experiment_command_parsers.add_parser("get")
        experiment_command_get_parser.add_argument("experiment_id",
                                                   help="The experiment ID.")
        experiment_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")

        experiment_cmd_create_parser = \
            experiment_command_parsers.add_parser("create")
        experiment_cmd_create_parser.add_argument(
            "title", help="The experiment title to create.")
        experiment_cmd_create_parser.add_argument(
            "--description", help="A description of the experiment.")
        experiment_cmd_create_parser.add_argument(
            "--institution", help="The institution of the experiment.")
        experiment_cmd_create_parser.add_argument(
            "--params", help="A JSON file containing experiment parameters.")

        experiment_cmd_update_parser = \
            experiment_command_parsers.add_parser("update")
        experiment_cmd_update_parser.add_argument(
            "experiment_id", help="The ID of the experiment to update.")
        experiment_cmd_update_parser.add_argument(
            "--title", help="The new title of the experiment.")
        experiment_cmd_update_parser.add_argument(
            "--description", help="The new description of the experiment.")

    def build_dataset_parser(self):
        """
        Builds parsing rules for dataset-related command-line interface arguments.
        """
        dataset_parser = self.model_parsers.add_parser("dataset")
        dataset_command_parsers = \
            dataset_parser.add_subparsers(help='available commands',
                                          dest='command')

        dataset_command_list_parser = dataset_command_parsers.add_parser("list")
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

        dataset_command_get_parser = dataset_command_parsers.add_parser("get")
        dataset_command_get_parser.add_argument("dataset_id",
                                                help="The dataset ID.")
        dataset_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")

        dataset_command_create_parser = \
            dataset_command_parsers.add_parser("create")
        dataset_command_create_parser.add_argument(
            "experiment_id", help="The experiment ID.")
        dataset_command_create_parser.add_argument(
            "description", help="The dataset description.")
        dataset_command_create_parser.add_argument("--instrument",
                                                   help="The instrument ID.")
        dataset_command_create_parser.add_argument(
            "--params", help="A JSON file containing dataset parameters.")

        dataset_cmd_update_parser = \
            dataset_command_parsers.add_parser("update")
        dataset_cmd_update_parser.add_argument(
            "dataset_id", help="The ID of the dataset to update.")
        dataset_cmd_update_parser.add_argument(
            "--description", help="The new description of the dataset.")

    def build_datafile_parser(self):
        """
        Builds parsing rules for datafile-related command-line interface arguments.
        """
        datafile_parser = self.model_parsers.add_parser("datafile")
        datafile_command_parsers = \
            datafile_parser.add_subparsers(help='available commands',
                                           dest='command')

        datafile_command_list_parser = datafile_command_parsers.add_parser("list")
        datafile_command_list_parser.add_argument("--dataset",
                                                  help="The dataset ID.")
        datafile_command_list_parser.add_argument("--directory",
                                                  help="The subdirectory within the dataset.")
        datafile_command_list_parser.add_argument("--filename",
                                                  help="The datafile's name.")
        datafile_command_list_parser.add_argument(
            "--limit", help="Maximum number of results to return.")
        datafile_command_list_parser.add_argument(
            "--offset",
            help="Skip this many records from the start of the result set.")
        datafile_command_list_parser.add_argument(
            "--order_by",
            help="Order by this field.")
        datafile_command_list_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")

        datafile_command_get_parser = datafile_command_parsers.add_parser("get")
        datafile_command_get_parser.add_argument("datafile_id",
                                                 help="The datafile ID.")
        datafile_command_get_parser.add_argument(
            "--json", action='store_true', help="Display results in JSON format.")

        datafile_command_create_parser = \
            datafile_command_parsers.add_parser("create")
        datafile_command_create_parser.add_argument(
            "dataset_id", help="The dataset ID.")
        datafile_command_create_parser.add_argument(
            "--directory", help="The subdirectory within the dataset.")
        datafile_command_create_parser.add_argument(
            "--storagebox", help="The storage box containing the datafile.")
        datafile_command_create_parser.add_argument(
            "file_path", help="The file to be represented in the datafile record.")

        datafile_cmd_download_parser = datafile_command_parsers.add_parser("download")
        datafile_cmd_download_parser.add_argument("datafile_id",
                                                  help="The datafile ID.")

        datafile_cmd_upload_parser = datafile_command_parsers.add_parser("upload")
        datafile_cmd_upload_parser.add_argument("dataset_id",
                                                help="The dataset ID.")
        datafile_cmd_upload_parser.add_argument(
            "--directory",
            help="The datafile's subdirectory within the dataset.")
        datafile_cmd_upload_parser.add_argument("file_path",
                                                help="The file to upload.")

        datafile_cmd_update_parser = \
            datafile_command_parsers.add_parser("update")
        datafile_cmd_update_parser.add_argument(
            "datafile_id", help="The ID of the datafile to update.")
        datafile_cmd_update_parser.add_argument(
            "--md5sum", help="The new MD5 sum of the datafile.")

    def build_storagebox_parser(self):
        """
        Builds parsing rules for storagebox-related
        command-line interface arguments.
        """
        storagebox_parser = self.model_parsers.add_parser("storagebox")
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

    def build_schema_parser(self):
        """
        Builds parsing rules for schema-related
        command-line interface arguments.
        """
        schema_parser = self.model_parsers.add_parser("schema")
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


def get_parser():
    """
    Used by sphinx-argparse.
    """
    return ArgParser().build_parser()
