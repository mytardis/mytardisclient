"""
Custom exceptions to raise within MyTardis Client.
"""


class DuplicateKey(Exception):
    """
    Duplicate key exception.
    """


class SshException(Exception):
    """
    SSH exception.
    """
    def __init__(self, message, returncode=None):
        super(SshException, self).__init__(message)
        self.returncode = returncode


class InvalidConfig(Exception):
    """
    Invalid config.
    """


class MissingConfig(Exception):
    """
    Missing config.
    """
