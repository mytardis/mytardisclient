"""
Model class for the configuration,
usually stored in ~/.config/mytardisclient/mytardisclient.cfg
"""

# pylint: disable=missing-docstring

import os
import json
import traceback
from urlparse import urlparse
from ConfigParser import ConfigParser
from dogpile.cache import make_region  # pylint: disable=import-error

from mytardisclient.logs import logger

DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config',
                                   'mytardisclient', 'mytardisclient.cfg')
DEFAULT_DATASETS_PATH = os.path.join(os.path.expanduser('~'), '.config',
                                     'mytardisclient', 'datasets')
DEFAULT_CACHE_PATH = os.path.join(os.path.expanduser('~'), '.cache',
                                  'mytardisclient', 'mytardisclient.cache')


class Config(object):
    """
    Model class for the minimal MyTardis server configuration
    (MyTardis URL, username and API key),
    usually stored in ~/.config/mytardisclient/mytardisclient.cfg
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.path = path
        self.url = ""
        self.username = ""
        self.apikey = ""
        self.default_headers = None
        def key_generator(namespace, function):
            # pylint: disable=unused-argument
            def generate_key(*args, **kwargs):
                return "%s(%s,%s)" % \
                    (function.__name__, str(args), str(kwargs))
            return generate_key
        self.datasets_path = DEFAULT_DATASETS_PATH
        if not os.path.exists(self.datasets_path):
            os.makedirs(self.datasets_path)
        self.cache_path = DEFAULT_CACHE_PATH
        if not os.path.exists(os.path.dirname(self.cache_path)):
            os.makedirs(os.path.dirname(self.cache_path))
        self.region = \
            make_region(function_key_generator=key_generator) \
                .configure(
                    'dogpile.cache.dbm',
                    expiration_time=30,
                    arguments={
                        "filename": self.cache_path
                    })
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
        file.

        :param path: The path to the config file, usually
            ~/.config/mytardisclient/mytardisclient.cfg
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

        self.update_default_headers()

    def update_default_headers(self):
        """
        If the client is launched with a query request, but no valid
        configuration has been set, then the application's
        configuration object will need to be updated, and the default
        header will need to updated, because it depends on the API
        key in the configuration.
        """
        self.default_headers = {
            "Authorization": "ApiKey %s:%s" % (self.username,
                                               self.apikey),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def validate(self):
        """
        Ensure that the config contains a non-empty username,
        API key and MyTardis URL.
        """
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
        """
        Saves the configuration to disk.

        :param path: The path to save to, usually
            ~/.config/mytardisclient/mytardisclient.cfg
        """
        if path:
            self.path = path
        else:
            path = self.path
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        config_parser = ConfigParser()
        with open(self.path, 'w') as config_file:
            config_parser.add_section("mytardisclient")
            fields = ["url", "username", "apikey"]
            for field in fields:
                config_parser.set("mytardisclient", field, self.__dict__[field])
            config_parser.write(config_file)
        logger.info("Saved settings to " + self.path)
