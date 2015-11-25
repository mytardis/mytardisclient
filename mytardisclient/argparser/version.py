"""
argparser/version.py
"""
import textwrap


def build_version_parser(argument_parser):
    """
    Displays the mytardisclient version
    """
    version_help = "Display the MyTardis Client version."
    version_usage = textwrap.dedent("""\
        mytardis version [-h]

        $ mytardis version
        MyTardis Client v0.0.1""")
    argument_parser.model_parsers.add_parser("version", help=version_help,
                                             usage=version_usage)
