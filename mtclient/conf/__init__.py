"""
Defines the singleton configuration instance
of :class:`mtclient.models.config.Config`.

It can be imported as follows:

`from mtclient.conf import config`
"""
from mtclient.models.config import Config

config = Config()  # pylint: disable=invalid-name
