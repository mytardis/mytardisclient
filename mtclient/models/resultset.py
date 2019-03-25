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
    def __init__(self, model, url, json):
        """
        Each record in the result set can be
        represented as an object of class model
        """
        self.model = model
        self.url = url
        self.json = json
        self.total_count = self.json['meta']['total_count']
        self.limit = self.json['meta']['limit']
        self.offset = self.json['meta']['offset']
        self._objects = None

    def __repr__(self):
        """
        String representation
        """
        if not self._objects:
            self._objects = []
            for index in range(len(self.json['objects'])):
                self._objects.append(self.model(self.json['objects'][index]))
        return "<ResultSet [%s]>" % ", ".join(str(obj) for obj in self._objects)

    def __len__(self):
        """
        Return number of records in ResultSet
        """
        return len(self.json['objects'])

    def __getitem__(self, key):
        """
        Get a record from the query set.
        """
        if 'include_metadata' in self.model.__init__.__code__.co_varnames:
            return self.model(self.json['objects'][key],
                              include_metadata=False)
        return self.model(self.json['objects'][key])

    def __iter__(self):
        """
        Return the ResultSet's iterator object, which is itself.
        """
        kwargs = {}
        if 'include_metadata' in self.model.__init__.__code__.co_varnames:
            kwargs['include_metadata'] = False
        for index in range(len(self.json['objects'])):
            args = [self.json['objects'][index]]
            yield self.model(*args, **kwargs)
