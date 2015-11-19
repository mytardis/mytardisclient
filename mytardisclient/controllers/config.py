"""
Controller class for setting up config file.
"""

import os
from ConfigParser import ConfigParser


class ConfigController(object):
    """
    Controller class for setting up config file.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, config_path):
        self.config_path = config_path

    def configure(self):
        """
        Configure MyTardis Client settings.
        """
        if os.path.exists(self.config_path):
            print "A config file already exists at %s" % self.config_path
            overwrite = raw_input("Are you sure you want to overwrite it? ")
            if not overwrite.strip().lower().startswith('y'):
                return
            print ""

        mytardis_url = raw_input("MyTardis URL? ")
        username = raw_input("MyTardis Username? ")
        api_key = raw_input("MyTardis API key? ")

        config_dir = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        cfgfile = open(self.config_path, 'w')
        cfgparser = ConfigParser()
        cfgparser.add_section('mytardisclient')
        cfgparser.set('mytardisclient', 'mytardis_url', mytardis_url)
        cfgparser.set('mytardisclient', 'username', username)
        cfgparser.set('mytardisclient', 'api_key', api_key)
        cfgparser.write(cfgfile)
        cfgfile.close()
        print "Wrote settings to %s" % self.config_path
