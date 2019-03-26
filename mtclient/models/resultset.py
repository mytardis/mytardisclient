"""
This module contains the :class:`ResultSet` class, an abstraction to represent
the JSON returned by the MyTardis API, particularly for queries which return
multiple records and could be subject to pagination.
"""


class ResultSet(object):
    """
    Abstraction to represent JSON returned by MyTardis API
    which includes a list of records and some meta information
    e.g. whether there are additional pages of records to
    retrieve.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    def __init__(self, model, url, response_dict):
        """
        Each record in the result set can be
        represented as an object of class model
        """
        self.model = model
        self.url = url
        self.response_dict = response_dict
        self.total_count = self.response_dict['meta']['total_count']
        self.limit = self.response_dict['meta']['limit']
        self.offset = self.response_dict['meta']['offset']
        self._objects = None

    def __repr__(self):
        """
        String representation
        """
        if not self._objects:
            self._objects = []
            for index in range(len(self.response_dict['objects'])):
                self._objects.append(self.model(self.response_dict['objects'][index]))
        return "<ResultSet [%s]>" % ", ".join(str(obj) for obj in self._objects)

    def __len__(self):
        """
        Return number of records in ResultSet
        """
        return len(self.response_dict['objects'])

    def __bool__(self):
        """
        Return True if there's a list one object in the result set
        """
        return len(self) > 0

    def __nonzero__(self):
        """
        For Python 2.x
        """
        return self.__bool__()

    def __getitem__(self, key):
        """
        Get a record from the query set.
        """
        if 'include_metadata' in self.model.__init__.__code__.co_varnames:
            return self.model(self.response_dict['objects'][key],
                              include_metadata=False)
        return self.model(self.response_dict['objects'][key])

    def __iter__(self):
        """
        Return the ResultSet's iterator object, which is itself.
        """
        kwargs = {}
        if 'include_metadata' in self.model.__init__.__code__.co_varnames:
            kwargs['include_metadata'] = False
        for index in range(len(self.response_dict['objects'])):
            args = [self.response_dict['objects'][index]]
            yield self.model(*args, **kwargs)

    @staticmethod
    def empty(model):
        """
        Return an empty result set
        """
        response_dict = {
            "meta": {
                "limit": 20,
                "next": None,
                "offset": 0,
                "previous": None,
                "total_count": 0
            },
            "objects": [
            ]
        }
        return ResultSet(model, None, response_dict)
