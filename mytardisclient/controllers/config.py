"""
Controller class for setting up config file.
"""
from __future__ import print_function

import os
from mytardisclient.conf import config


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
            overwrite = raw_input("Are you sure you want to overwrite it? ")
            if not overwrite.strip().lower().startswith('y'):
                return
            print("")

        config.url = raw_input("MyTardis URL? ")
        config.username = raw_input("MyTardis Username? ")
        config.apikey = raw_input("MyTardis API key? ")
        config.save(self.path)
        print("\nWrote settings to %s" % self.path)
