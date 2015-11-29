"""
Defines the singleton configuration instance
of :class:`mytardisclient.models.config.Config`.

It can be imported as follows:

`from mytardisclient.conf import config`
"""
from mytardisclient.models.config import Config

config = Config()  # pylint: disable=invalid-name
