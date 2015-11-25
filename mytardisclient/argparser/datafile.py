"""
argparser/datafile.py
"""
import textwrap


def build_datafile_parser(argument_parser):
    """
    Builds parsing rules for datafile-related command-line interface arguments.
    """
    datafile_parser = argument_parser.model_parsers.add_parser("datafile")
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
