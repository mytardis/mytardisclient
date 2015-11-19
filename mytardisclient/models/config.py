"""
Model class for the configuration stored in ~/.mytardisclient.cfg
"""

# pylint: disable=missing-docstring

import os
import traceback
from ConfigParser import ConfigParser

from mytardisclient.logs import logger
from mytardisclient.models.user import User


class Config(object):
    """
    Model class for the configuration stored in ~/.mytardisclient.cfg
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.mytardis_url = ""
        self.username = ""
        self.api_key = ""
        self.mytardis_user = None
        self.load_config()

    def load_config(self, config_path=None):
        """
        Sets some default values for settings fields, then loads a config
        file, usually ~/.mytardisclient.cfg
        """
        self.mytardis_url = ""
        self.username = ""
        self.api_key = ""

        if config_path is None:
            config_path = self.config_path

        if config_path is not None and os.path.exists(config_path):
            logger.info("Reading settings from: " + config_path)
            # pylint: disable=bare-except
            try:
                config_parser = ConfigParser()
                config_parser.read(config_path)
                section = "mytardisclient"
                fields = ["mytardis_url", "username", "api_key"]
                for field in fields:
                    if config_parser.has_option(section, field):
                        self.__dict__[field] = \
                            config_parser.get(section, field)
            except:
                logger.error(traceback.format_exc())

    def get_mytardis_user(self):
        if self.mytardis_user and \
                self.mytardis_user.username == self.username:
            return self.mytardis_user
        self.mytardis_user = User.get_user_by_username(self, self.username)
        return self.mytardis_user

    def save_to_disk(self):
        config_parser = ConfigParser()
        with open(self.config_path, 'w') as config_file:
            config_parser.add_section("mytardisclient")
            fields = ["mytardis_url", "username", "api_key"]
            for field in fields:
                config_parser.set("mytardisclient", field, self.__dict__[field])
            config_parser.write(config_file)
        logger.info("Saved settings to " + self.config_path)
