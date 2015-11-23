"""
Model class for the configuration stored in ~/.mytardisclient.cfg
"""

# pylint: disable=missing-docstring

import os
import json
import traceback
from urlparse import urlparse
from ConfigParser import ConfigParser

from mytardisclient.logs import logger

DEFAULT_PATH = os.path.join(os.path.expanduser('~'), '.config',
                            'mytardisclient', 'mytardisclient.cfg')

class Config(object):
    """
    Model class for the minimal MyTardis server configuration
    (MyTardis URL, username and API key),
    usually stored in ~/.mytardisclient.cfg
    """
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.url = ""
        self.username = ""
        self.apikey = ""
        self.default_headers = None
        if path:
            self.load()

    def __unicode__(self):
        return json.dumps(self.__dict__, indent=2)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    def load(self, path=None):
        """
        Sets some default values for settings fields, then loads a config
        file, usually ~/.config/mytardisclient/mytardisclient.cfg
        """
        self.url = ""
        self.username = ""
        self.apikey = ""

        if path:
            self.path = path
        else:
            path = self.path

        if path is not None and os.path.exists(path):
            logger.info("Reading settings from: " + path)
            # pylint: disable=bare-except
            try:
                config_parser = ConfigParser()
                config_parser.read(path)
                section = "mytardisclient"
                fields = ["url", "username", "apikey"]

                # For backwards compatibility:
                if config_parser.has_option(section, "mytardis_url"):
                    self.url = config_parser.get(section, "mytardis_url")
                if config_parser.has_option(section, "api_key"):
                    self.apikey = config_parser.get(section, "api_key")

                for field in fields:
                    if config_parser.has_option(section, field):
                        self.__dict__[field] = \
                            config_parser.get(section, field)
            except:
                logger.error(traceback.format_exc())

        self.default_headers = {
            "Authorization": "ApiKey %s:%s" % (self.username,
                                               self.apikey),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def validate(self):
        if self.username == "":
            raise Exception("MyTardis username is missing from config.")
        if self.apikey == "":
            raise Exception("MyTardis API key is missing from config.")
        if self.url == "":
            raise Exception("MyTardis URL is missing from config.")
        parsed_url = urlparse(self.url)
        if parsed_url.scheme not in ('http', 'https') or parsed_url.netloc == '':
            raise Exception("Invalid MyTardis URL found in config: %s", self.url)

    def save(self, path=None):
        if path:
            self.path = path
        else:
            path = self.path

        config_parser = ConfigParser()
        with open(self.path, 'w') as config_file:
            config_parser.add_section("mytardisclient")
            fields = ["url", "username", "apikey"]
            for field in fields:
                config_parser.set("mytardisclient", field, self.__dict__[field])
            config_parser.write(config_file)
        logger.info("Saved settings to " + self.path)
