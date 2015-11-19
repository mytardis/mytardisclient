"""
resultset.py
"""


class ResultSet(object):
    """
    Abstraction to represent JSON returned by MyTardis API
    which includes a list of records and some meta information
    e.g. whether there are additional pages of records to
    retrieve.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, model, config, url, json, **filters):
        """
        Each record in the result set can be
        represented as an object of class model
        """
        self.model = model
        self.config = config
        self.url = url
        self.json = json
        self.index = -1
        self.total_count = self.json['meta']['total_count']
        self.limit = self.json['meta']['limit']
        self.offset = self.json['meta']['offset']
        self.filters = str(filters)

    def __len__(self):
        """
        Return number of records in ResultSet
        """
        return len(self.json['objects'])

    def __getitem__(self, key):
        """
        Get a record from the query set.
        """
        return self.model(self.config, self.json['objects'][key])

    def __iter__(self):
        """__iter__"""
        return self

    def next(self):
        """next"""
        self.index += 1
        if self.index >= len(self):
            raise StopIteration
        return self.model(self.config, self.json['objects'][self.index])
