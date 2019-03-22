"""
Base class for models to inherit from
"""
from six import with_metaclass


class Manager(object):
    """
    Each Model.objects instance will be an instance of this
    Manager class.
    """
    @classmethod
    def get(cls, **kwargs):
        pass


class ModelMetaclass(type):
    """
    Metaclass to allow mytardisclient model classes to use
    Django-style syntax (Model.objects.get etc.) to access
    their methods from a .objects property
    """
    @property
    def objects(cls):
        """
        Provides the .objects property, allowing the model's
        static methods to be accessed with Model.objects.[method]
        """
        if not hasattr(cls, "_objects"):
            cls._objects = Manager()
            for attr in dir(cls):
                if not attr.startswith("__"):
                    setattr(cls._objects, attr, getattr(cls, attr))
        return cls._objects


class Model(with_metaclass(ModelMetaclass, object)):
    """
    Base class for models to inherit from
    """
    def __repr__(self):
        """
        Return a string representation
        """
        if hasattr(self, "__str__"):
            return self.__str__()
        return repr(self)
