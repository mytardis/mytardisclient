"""
argparser/__init__.py
"""
from argparse import ArgumentParser
import textwrap

from .api import build_api_parser
from .config import build_config_parser
from .version import build_version_parser
from .facility import build_facility_parser
from .instrument import build_instrument_parser
from .experiment import build_experiment_parser
from .dataset import build_dataset_parser
from .datafile import build_datafile_parser
from .storagebox import build_storagebox_parser
from .schema import build_schema_parser


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
        build_api_parser(self)
        build_config_parser(self)
        build_version_parser(self)
        build_facility_parser(self)
        build_instrument_parser(self)
        build_experiment_parser(self)
        build_dataset_parser(self)
        build_datafile_parser(self)
        build_storagebox_parser(self)
        build_schema_parser(self)

        return self.parser


def get_parser():
    """
    Used by sphinx-argparse.
    """
    return ArgParser().build_parser()
