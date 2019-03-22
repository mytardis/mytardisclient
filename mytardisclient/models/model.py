"""
Base class for models to inherit from
"""
from six import with_metaclass


class Object(object):
    """
    Simple class allowing us to add attributes to an object
    """


class ModelMetaclass(type):
    """
    Metaclass to allow mytardisclient model classes to use
    Django-style syntax (Model.objects.get etc.) to access
    their methods from a .objects property
    """
    @property
    def objects(cls):
        if not hasattr(cls, "_objects"):
            cls._objects = Object()
            for attr in dir(cls):
                if not attr.startswith("__"):
                    setattr(cls._objects, attr, getattr(cls, attr))
        return cls._objects


class Model(with_metaclass(ModelMetaclass, object)):
    """
    Base class for models to inherit from
    """
