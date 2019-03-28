"""
Controller class for setting up config file.
"""
from __future__ import print_function

import os

from six.moves import input

from mtclient.conf import config


class ConfigController(object):
    """
    Controller class for setting up config file.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, path):
        self.path = path

    def configure(self, args=None):
        """
        Configure MyTardis Client settings.
        """
        if args and hasattr(args, 'key') and args.key:
            print(getattr(config, args.key))
            return

        if os.path.exists(self.path):
            print("A config file already exists at %s" % self.path)
            overwrite = input("Are you sure you want to overwrite it? ")
            if not overwrite.strip().lower().startswith('y'):
                return
            print("")

        config.url = os.environ.get("MYTARDISCLIENT_URL") or \
            input("MyTardis URL? ")
        config.username = os.environ.get("MYTARDISCLIENT_USERNAME") or \
            input("MyTardis Username? ")
        config.apikey = os.environ.get("MYTARDISCLIENT_APIKEY") or \
            input("MyTardis API key? ")
        # Only save settings to config file if at least one of them
        # was supplied by raw input, not by an environment variable:
        if config.url != os.environ.get("MYTARDISCLIENT_URL") or \
                config.username != os.environ.get("MYTARDISCLIENT_USERNAME") or \
                config.apikey != os.environ.get("MYTARDISCLIENT_APIKEY"):
            config.save(self.path)
            print("\nWrote settings to %s" % self.path)
