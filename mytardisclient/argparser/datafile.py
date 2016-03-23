"""
argparser/datafile.py
"""
import textwrap


def build_datafile_parser(argument_parser):
    """
    Builds parsing rules for datafile-related command-line interface arguments.
    """
    # pylint: disable=too-many-locals
    datafile_help = \
        "Display a list of datafile records or a single datafile record."
    datafile_usage = \
        "mytardis datafile [-h] {list,get,create,update,download,upload} ..."
    datafile_parser = \
        argument_parser.model_parsers.add_parser("datafile",
                                                 help=datafile_help,
                                                 usage=datafile_usage)
    datafile_command_parsers = \
        datafile_parser.add_subparsers(help='available commands',
                                       dest='command')

    datafile_list_help = "Display a list of datafile records."
    datafile_list_usage = textwrap.dedent("""\
        mytardis datafile list
            [--dataset DATASET] [--directory DIRECTORY] [--filename FILENAME]
            [--limit LIMIT] [--offset OFFSET] [--order_by ORDER_BY] [--json]
            [--filter FILTER]

          EXAMPLE
       
          $ mytardis datafile list --dataset 35

          Model: DataFile
          Query: http://mytardisdemo.erc.monash.edu.au/api/v1/dataset_file/?format=json&dataset__id=35
          Total Count: 2
          Limit: 20
          Offset: 0

          +-------------+-----------+-----------+-------------------------------------+----------+-----------+----------------------------------+
          | DataFile ID | Directory | Filename  |                 URI                 | Verified |   Size    |             MD5 Sum              |
          +=============+===========+===========+=====================================+==========+===========+==================================+
          |         120 |           | hello.txt | James Test Dataset 004-35/hello.txt | True     |  25 bytes | 214e52fcf7f98d9fb8588b42cfb7987f |
          +-------------+-----------+-----------+-------------------------------------+----------+-----------+----------------------------------+
          |         121 |           | test.txt  | James Test Dataset 004-35/test.txt  | False    |   8 bytes | 74119cb1c9568b96feb7fa392006e40f |
          +-------------+-----------+-----------+-------------------------------------+----------+-----------+----------------------------------+
        """)
    datafile_command_list_parser = \
        datafile_command_parsers.add_parser("list",
                                            help=datafile_list_help,
                                            usage=datafile_list_usage)
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
    datafile_command_list_parser.add_argument(
        "--filter", help="Filter on these fields, e.g. \"filename=file1.txt\".")

    datafile_get_help = "Display a single datafile record."
    datafile_get_usage = textwrap.dedent("""\
        mytardis datafile get [--json] datafile_id

          EXAMPLE

          $ mytardis datafile get 99
          +----------------+-------------------------------------+
          | DataFile field |                Value                |
          +================+=====================================+
          | ID             | 99                                  |
          +----------------+-------------------------------------+
          | Dataset        | /api/v1/dataset/31/                 |
          +----------------+-------------------------------------+
          | Filename       | hello.txt                           |
          +----------------+-------------------------------------+
          | URI            | James Test Dataset 001-31/hello.txt |
          +----------------+-------------------------------------+
          | Verified       | True                                |
          +----------------+-------------------------------------+
          | Size           |  13 bytes                           |
          +----------------+-------------------------------------+
          | MD5 Sum        | 9af2f8218b150c351ad802c6f3d66abe    |
          +----------------+-------------------------------------+
        """)
    datafile_command_get_parser = \
        datafile_command_parsers.add_parser("get",
                                            help=datafile_get_help,
                                            usage=datafile_get_usage)
    datafile_command_get_parser.add_argument("datafile_id",
                                             help="The datafile ID.")
    datafile_command_get_parser.add_argument(
        "--json", action='store_true', help="Display results in JSON format.")

    datafile_create_help = textwrap.dedent("""\
        Create a datafile record.
        """)
    datafile_create_usage = textwrap.dedent("""\
        mytardis datafile create
            [-s STORAGEBOX] [-d DATASET_PATH] dataset_id path

          EXAMPLE

          $ mytardis datafile create 31 dataset1/test.txt

          Model: DataFile

          +----------------+------------------------------------+
          | DataFile field |               Value                |
          +================+====================================+
          | ID             | 119                                |
          +----------------+------------------------------------+
          | Dataset        | /api/v1/dataset/31/                |
          +----------------+------------------------------------+
          | Storage Box    | default                            |
          +----------------+------------------------------------+
          | Directory      |                                    |
          +----------------+------------------------------------+
          | Filename       | test.txt                           |
          +----------------+------------------------------------+
          | URI            | James Test Dataset 001-31/test.txt |
          +----------------+------------------------------------+
          | Verified       | False                              |
          +----------------+------------------------------------+
          | Size           |   5 bytes                          |
          +----------------+------------------------------------+
          | MD5 Sum        | 2205e48de5f93c784733ffcca841d2b5   |
          +----------------+------------------------------------+

            """)
    datafile_command_create_parser = \
        datafile_command_parsers.add_parser(
            "create",
            help=datafile_create_help,
            usage=datafile_create_usage)
    datafile_command_create_parser.add_argument(
        "dataset_id", help="The dataset ID.")
    datafile_command_create_parser.add_argument(
        "-s", "--storagebox", help="The storage box containing the datafile.")
    datafile_command_create_parser.add_argument(
        "-d", "--dataset_path", help="The local dataset path.")
    datafile_command_create_parser.add_argument(
        "path",
        help="The file to be represented in the datafile record, or "
        "a directory containing the datafiles to create records for. "
        "If a relative path is provided, the first component will be "
        "assumed to be the local dataset path.")

    datafile_download_help = "Download a datafile."
    datafile_download_usage = textwrap.dedent("""\
        mytardis datafile download datafile_id

          EXAMPLE

          $ mytardis datafile download 99
          Downloaded: hello.txt
            """)
    datafile_cmd_download_parser = \
        datafile_command_parsers.add_parser("download",
                                            help=datafile_download_help,
                                            usage=datafile_download_usage)
    datafile_cmd_download_parser.add_argument("datafile_id",
                                              help="The datafile ID.")

    datafile_upload_help = "Upload a datafile."
    datafile_upload_usage = textwrap.dedent("""\
        mytardis datafile upload
            [-s STORAGEBOX] [-d DATASET_PATH] dataset_id file_path

          EXAMPLE

          We will upload datafile "new_datafile.txt" to dataset ID 35:

          $ mytardis datafile upload 35 new_datafile.txt
          Uploaded: new_datafile.txt

          Now let's display dataset 35 (including its datafiles) and
          check whether our new datafile has been uploaded:

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
          Total Count: 3
          Limit: 20
          Offset: 0

          +-------------+-----------+------------------+--------------------------------------------+----------+-----------+----------------------------------+
          | DataFile ID | Directory |     Filename     |                    URI                     | Verified |   Size    |             MD5 Sum              |
          +=============+===========+==================+============================================+==========+===========+==================================+
          |         120 |           | hello.txt        | James Test Dataset 004-35/hello.txt        | True     |  25 bytes | 214e52fcf7f98d9fb8588b42cfb7987f |
          +-------------+-----------+------------------+--------------------------------------------+----------+-----------+----------------------------------+
          |         121 |           | test.txt         | James Test Dataset 004-35/test.txt         | False    |   8 bytes | 74119cb1c9568b96feb7fa392006e40f |
          +-------------+-----------+------------------+--------------------------------------------+----------+-----------+----------------------------------+
          |         131 |           | new_datafile.txt | James Test Dataset 004-35/new_datafile.txt | True     |  21 bytes | 2ce6aa694791def6de39b3fccead9d87 |
          +-------------+-----------+------------------+--------------------------------------------+----------+-----------+----------------------------------+
        """)
    datafile_cmd_upload_parser = \
        datafile_command_parsers.add_parser("upload",
                                            help=datafile_upload_help,
                                            usage=datafile_upload_usage)
    datafile_cmd_upload_parser.add_argument("dataset_id",
                                            help="The dataset ID.")
    datafile_cmd_upload_parser.add_argument(
        "-s", "--storagebox",
        help="The storage box which will store the datafile.")
    datafile_cmd_upload_parser.add_argument(
        "-d", "--dataset_path", help="The local dataset path.")
    datafile_cmd_upload_parser.add_argument("file_path",
                                            help="The file to upload.")

    datafile_update_help = "Update a datafile record."
    datafile_update_usage = textwrap.dedent("""\
        mytardis datafile update [--md5sum MD5SUM] datafile_id

          EXAMPLE

          $ mytardis datafile update --md5sum "md5-sum" 99
          HTTP 401
          Traceback (most recent call last):
            ...
          Exception

          Datafile updates are not yet enabled in the MyTardis API.
          See the "update_detail" method in tardis/tardis_portal/api.py

          Being able to update the MD5 sum would be useful for really
          large datafiles where calculating the MD5 sum is time-consuming.
          Rather than waiting until the MD5 sum calculation is complete to
          begin a datafile upload, the datafile upload could begin
          immediately (supplying a bogus MD5 sum to MyTardis), and then
          the MD5 sum could be updated once the calculation is complete.
        """)
    datafile_cmd_update_parser = \
        datafile_command_parsers.add_parser("update",
                                            help=datafile_update_help,
                                            usage=datafile_update_usage)
    datafile_cmd_update_parser.add_argument(
        "datafile_id", help="The ID of the datafile to update.")
    datafile_cmd_update_parser.add_argument(
        "--md5sum", help="The new MD5 sum of the datafile.")

    datafile_verify_help = "Ask MyTardis to verify a datafile record."
    datafile_verify_usage = textwrap.dedent("""\
        mytardis datafile verify datafile_id

          EXAMPLE

          $ mytardis datafile verify 99
        """)
    datafile_command_verify_parser = \
        datafile_command_parsers.add_parser("verify",
                                            help=datafile_verify_help,
                                            usage=datafile_verify_usage)
    datafile_command_verify_parser.add_argument("datafile_id",
                                                help="The datafile ID.")
