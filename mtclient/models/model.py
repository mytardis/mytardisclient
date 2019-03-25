"""
Base class for models to inherit from
"""
import six
from six import with_metaclass


class Manager(object):
    """
    Each Model.objects instance will be an instance of this
    Manager class.
    """
    @classmethod
    def get(cls, **kwargs):
        """
        Override this with a method to retrieve a single instance of the model
        """

    @classmethod
    def all(cls, **kwargs):
        """
        Override this to retrieve all instances of the model

        Initially this is being implemented for result sets, with the intention
        to also implement it for query sets, for which Model.objects.all() will
        return a generator which will not trigger any API requests until we
        attempt to index it or convert it to a list etc.
        """

    @classmethod
    def filter(cls, **kwargs):
        """
        Override this to provide a method to filter by kwargs.

        Initially this is being implemented for result sets, with the intention
        to also implement it for query sets, for which Model.objects.filter()
        will return a generator which will not trigger any API requests until
        we attempt to index it or convert it to a list etc.
        """


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

        setattr(cls._objects, "get", getattr(cls, "get"))

        list_method = getattr(cls, "list")
        setattr(cls._objects, "all", list_method)

        def _filter(**kwargs):
            filter_str = "&".join(
                "%s=%s" % (key, value) for key, value in six.iteritems(kwargs))
            return list_method(filters=filter_str)

        setattr(cls._objects, "filter", _filter)

        def _order_by(order_by):
            return list_method(order_by=order_by)

        setattr(cls._objects, "order_by", _order_by)

        return cls._objects


class Model(with_metaclass(ModelMetaclass, object)):
    """
    Base class for models to inherit from
    """
    # pylint: disable=too-few-public-methods
    def __repr__(self):
        """
        Return a string representation
        """
        if hasattr(self, "__str__"):
            return self.__str__()
        return repr(self)
