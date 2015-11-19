#!/usr/bin/env python
"""
client.py
"""
import os
import sys

from mytardisclient import __version__ as VERSION
from mytardisclient.models.config import Config
from mytardisclient.controllers.config import ConfigController
from mytardisclient.controllers.facility import FacilityController
from mytardisclient.controllers.instrument import InstrumentController
from mytardisclient.controllers.experiment import ExperimentController
from mytardisclient.controllers.dataset import DatasetController
from mytardisclient.controllers.datafile import DataFileController
from mytardisclient.argparser import ArgParser


def run():
    """
    Main function for command-line interface.
    """
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    args = ArgParser().get_args()

    if args.model == 'version':
        print "MyTardis Client v%s" % VERSION
        sys.exit(0)
    if args.verbose and (not hasattr(args, 'json') or not args.json):
        print "MyTardis Client v%s" % VERSION

    config_path = os.path.join(os.path.expanduser('~'),
                               '.config',
                               'mytardisclient',
                               'mytardisclient.cfg')

    if not os.path.exists(config_path) or \
            args.model == 'config':
        ConfigController(config_path).configure()
        if args.model == 'config':
            sys.exit(0)
    config = Config(config_path)

    if args.verbose and (not hasattr(args, 'json') or not args.json):
        print "Config: %s" % config_path
        print "MyTardis URL: %s" % config.mytardis_url
        print "Username: %s" % config.username

    if args.model == 'facility':
        FacilityController(config).run_command(args)
    elif args.model == 'instrument':
        InstrumentController(config).run_command(args)
    elif args.model == 'experiment':
        ExperimentController(config).run_command(args)
    elif args.model == 'dataset':
        DatasetController(config).run_command(args)
    elif args.model == 'datafile':
        DataFileController(config).run_command(args)


if __name__ == "__main__":
    run()
