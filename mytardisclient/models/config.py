"""
Model class for the configuration,
usually stored in ~/.config/mytardisclient/mytardisclient.cfg
"""

# pylint: disable=missing-docstring

import os
import json
from urlparse import urlparse

from ConfigParser import ConfigParser
from dogpile.cache import make_region  # pylint: disable=import-error

DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config',
                                   'mytardisclient', 'mytardisclient.cfg')
CACHE_PATH = os.path.join(os.path.expanduser('~'), '.cache',
                          'mytardisclient', 'mytardisclient.cache')
DATASETS_PATH_PREFIX = os.path.join(os.path.expanduser('~'), '.config',
                                    'mytardisclient', 'servers')
LOGFILE_PATH = os.path.join(os.path.expanduser('~'), '.mytardisclient.log')
LOGGING_CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config',
                                   'mytardisclient', 'logging.cfg')
DEFAULT_LOGGING_CONF = """\
[loggers]
keys=root

[handlers]
keys=fileHandler,consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=fileHandler,consoleHandler

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('%(file_path)s', 'a')

[handler_consoleHandler]
class=StreamHandler
level=WARNING
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s
datefmt=
""" % {'file_path': LOGFILE_PATH}


class Config(object):
    """
    Model class for the minimal MyTardis server configuration
    (MyTardis URL, username and API key),
    usually stored in ~/.config/mytardisclient/mytardisclient.cfg
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, path=DEFAULT_CONFIG_PATH):
        #: The config file's location.
        #: Default: ~/.config/mytardisclient/mytardisclient.cfg
        self.path = path

        #: The logging config path.
        #: Default: ~/.config/mytardisclient/logging.cfg
        self.logging_config_path = LOGGING_CONFIG_PATH
        if not os.path.exists(os.path.dirname(self.logging_config_path)):
            os.makedirs(os.path.dirname(self.logging_config_path))
        if not os.path.exists(self.logging_config_path):
            with open(self.logging_config_path, 'w') as logging_config:
                logging_config.write(DEFAULT_LOGGING_CONF)
        self.logfile_path = LOGFILE_PATH

        #: The MyTardis URL, e.g. 'http://mytardisdemo.erc.monash.edu.au'
        self.url = ""

        #: The MyTardis username, e.g. 'demofacility"
        self.username = ""

        #: The MyTardis API key, e.g. '644be179cc6773c30fc471bad61b50c90897146c'
        self.apikey = ""

        #: Path for caching results of frequently used queries.
        #: Default: ~/.cache/mytardisclient/mytardisclient.cache
        self.cache_path = CACHE_PATH

        #: Cache backend.
        #: Default: 'dogpile.cache.dbm'.
        #: Set to 'dogpile.cache.null' to disable caching.
        self.cache_backend = 'dogpile.cache.dbm'

        #: Cache expiry time.
        #: Default: 30 seconds.
        self.cache_expiry = 30

        def key_generator(namespace, function):
            # pylint: disable=unused-argument
            def generate_key(*args, **kwargs):
                return "%s(%s,%s)" % \
                    (function.__name__, str(args), str(kwargs))
            return generate_key
        if not os.path.exists(os.path.dirname(self.cache_path)):
            os.makedirs(os.path.dirname(self.cache_path))
        self.region = \
            make_region(function_key_generator=key_generator) \
                .configure(
                    self.cache_backend,
                    expiration_time=self.cache_expiry,
                    arguments={
                        "filename": self.cache_path
                    })

        if path:
            self.load()

    def __unicode__(self):
        attrs = dict(path=self.path,
                     url=self.url,
                     username=self.username,
                     apikey=self.apikey,
                     cache_path=self.cache_path,
                     cache_backend=self.cache_backend,
                     cache_expiry=self.cache_expiry,
                     datasets_path=self.datasets_path)
        return json.dumps(attrs, indent=2)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    @property
    def hostname(self):
        parsed_url = urlparse(self.url)
        return parsed_url.netloc

    @property
    def datasets_path(self):
        #: Location to create symlinks to dataset folders.
        #: Default: ~/.config/mytardisclient/servers/[mytardis_hostname]/
        datasets_path = os.path.join(DATASETS_PATH_PREFIX, self.hostname)
        if not os.path.exists(datasets_path):
            os.makedirs(datasets_path)
        return datasets_path

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
            config_parser = ConfigParser()
            config_parser.read(path)
            section = "mytardisclient"
            fields = ["url", "username", "apikey", "cache_backend", "cache_expiry"]

            for field in fields:
                if config_parser.has_option(section, field):
                    self.__dict__[field] = \
                        config_parser.get(section, field)

    @property
    def default_headers(self):
        """
        Default headers to use for API queries
        (including API key authorization).
        """
        return {
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
        if parsed_url.scheme not in ('http', 'https') or \
                parsed_url.netloc == '':
            raise Exception("Invalid MyTardis URL found in config: %s",
                            self.url)

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
            fields = ["url", "username", "apikey", "cache_backend", "cache_expiry"]
            for field in fields:
                config_parser.set("mytardisclient", field, self.__dict__[field])
            config_parser.write(config_file)
