#!/usr/bin/env python
"""
client.py
"""
from __future__ import print_function

import os
import sys
import logging
import logging.config

from . import __version__ as VERSION
from .models.config import Config
from .models.config import DEFAULT_CONFIG_PATH
from .controllers.api import ApiController
from .controllers.config import ConfigController
from .controllers.facility import FacilityController
from .controllers.instrument import InstrumentController
from .controllers.experiment import ExperimentController
from .controllers.dataset import DatasetController
from .controllers.datafile import DataFileController
from .controllers.storagebox import StorageBoxController
from .controllers.schema import SchemaController
from .argparser import ArgParser


def run():
    """
    Main function for command-line interface.
    """
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches

    args = ArgParser().get_args()

    if args.model == 'version':
        print("MyTardis Client v%s" % VERSION)
        sys.exit(0)
    if args.verbose and (not hasattr(args, 'json') or not args.json):
        print("MyTardis Client v%s" % VERSION)

    config_path = DEFAULT_CONFIG_PATH
    if not os.path.exists(config_path) or \
            args.model == 'config':
        ConfigController(config_path).configure(args)
        if args.model == 'config':
            sys.exit(0)
    config = Config(config_path)
    config.validate()

    logging.config.fileConfig(config.logging_config_path,
                              disable_existing_loggers=False)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    logger.info("MyTardis Client v%s", VERSION)

    if args.verbose and (not hasattr(args, 'json') or not args.json):
        print("General config: %s" % config_path)
        print("Logging config: %s" % config.logging_config_path)
        print("MyTardis URL: %s" % config.url)
        print("Username: %s" % config.username)

    if args.model == 'api':
        ApiController().run_command(args)
    elif args.model == 'facility':
        FacilityController().run_command(args)
    elif args.model == 'instrument':
        InstrumentController().run_command(args)
    elif args.model == 'experiment':
        ExperimentController().run_command(args)
    elif args.model == 'dataset':
        DatasetController().run_command(args)
    elif args.model == 'datafile':
        DataFileController().run_command(args)
    elif args.model == 'storagebox':
        StorageBoxController().run_command(args)
    elif args.model == 'schema':
        SchemaController().run_command(args)


if __name__ == "__main__":
    run()
