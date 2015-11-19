"""
Controller class for setting up config file.
"""

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
        mytardis_url = raw_input("MyTardis URL? ")
        username = raw_input("MyTardis Username? ")
        api_key = raw_input("MyTardis API key? ")

        cfgfile = open(self.config_path, 'w')
        cfgparser = ConfigParser()
        cfgparser.add_section('mytardisclient')
        cfgparser.set('mytardisclient', 'mytardis_url', mytardis_url)
        cfgparser.set('mytardisclient', 'username', username)
        cfgparser.set('mytardisclient', 'api_key', api_key)
        cfgparser.write(cfgfile)
        cfgfile.close()
        print "Wrote settings to %s" % self.config_path
