"""
Custom exceptions to raise within MyTardis Client.
"""


class DuplicateKey(Exception):
    """
    Duplicate key exception.
    """


class MultipleObjectsReturned(Exception):
    """
    Multiple objects returned exception.
    """
    def __init__(self, message, url=None, response=None):
        super(MultipleObjectsReturned, self).__init__(message)

        self.url = url
        self.response = response


class DoesNotExist(Exception):
    """
    Does not exist exception.
    """
    def __init__(self, message, url=None, response=None, model_class=None):
        super(DoesNotExist, self).__init__(message)

        self.url = url
        self.response = response
        self.model_class = model_class


class Unauthorized(Exception):
    """
    Unauthorized exception.
    """
    def __init__(self, message, url=None, response=None):
        super(Unauthorized, self).__init__(message)

        self.url = url
        self.response = response


class InternalServerError(Exception):
    """
    Internal server exception.
    """
    def __init__(self, message, url=None, response=None):
        super(InternalServerError, self).__init__(message)

        self.url = url
        self.response = response


class SshException(Exception):
    """
    SSH exception.
    """
    def __init__(self, message, returncode=None):
        super(SshException, self).__init__(message)
        self.returncode = returncode


class StagingHostRefusedSshConnection(SshException):
    """
    Staging host refused SSH connection exception.
    """


class StagingHostSshPermissionDenied(SshException):
    """
    Staging host permission denied exception.
    """


class SshControlMasterLimit(SshException):
    """
    Reached max number of connections (or attempted connections)
    in SSH ControlMaster (Mac OS X only).
    This usually means there is a critical problem with SSHing
    to the specified staging host.
    """


class ScpException(SshException):
    """
    SCP exception.
    """
    def __init__(self, message, command=None, returncode=None):
        super(ScpException, self).__init__(message)
        self.command = command
        self.returncode = returncode


class NoActiveNetworkInterface(Exception):
    """
    No active network interface exception.
    """


class BrokenPipe(Exception):
    """
    Broken pipe exception.
    """


class IncompatibleMyTardisVersion(Exception):
    """
    Incompatible MyTardis version exception.
    """


class PrivateKeyDoesNotExist(Exception):
    """
    Private key does not exist exception.
    """


class InvalidFolderStructure(Exception):
    """
    Invalid folder structure exception.
    """


class StorageBoxAttributeNotFound(Exception):
    """
    Storage box attribute not found exception.
    """
    def __init__(self, storageBox, key):
        message = "Key '%s' not found in attributes for storage box '%s'" \
            % (key, storageBox.GetName())
        super(StorageBoxAttributeNotFound, self).__init__(message)


class StorageBoxOptionNotFound(Exception):
    """
    Storage box option not found exception.
    """
    def __init__(self, storageBox, key):
        message = "Key '%s' not found in options for storage box '%s'" \
            % (key, storageBox.GetName())
        super(StorageBoxOptionNotFound, self).__init__(message)


class InvalidConfig(Exception):
    """
    Invalid config.
    """


class MissingConfig(Exception):
    """
    Missing config.
    """
