"""
This module contains the :class:`QuerySet` class, an abstraction to represent
a query to send to the MyTardis API.  It is designed to be lazy, so it will
only submit the query / queries to the REST API when we iterate through the
results.
"""


class QuerySet(object):
    """
    An abstraction to represent a query to send to the MyTardis API.  It is
    designed to be lazy, so it will only submit the query / queries to the
    REST API when we iterate through the results.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, model, filters=None, limit=None, offset=None,
                 order_by=None):
        """
        Each record in the query set can be
        represented as an object of class model
        """
        self.model = model
        self.filters = filters
        self.limit = limit
        self.offset = offset
        self.order_by = order_by

        self._result_set = None
        # The user-requested offset (self.offset) is not expected to change
        # during the life of this QuerySet instance, but the instance's
        # internal self._offset (which will be added to the user-requested
        # self.offset) will be incremented after each page of results has
        # been retrieved from the REST API.
        self._offset = 0

    def _execute_query(self):
        """
        The user has requested something which requires evaluating the query
        """
        #self._result_set = self.model.list(
            #filters=self.filters, limit=self.limit, offset=self.offset,
            #order_by=self.order_by)
        self._result_set = self.model.list(
            filters=self.filters, limit=self.limit, offset=self.offset,
            order_by=self.order_by)

    def __repr__(self):
        """
        String representation
        """
        if not self._result_set:
            self._execute_query()
        pre_ellipsis = ""
        if self._result_set.offset > 0:
            pre_ellipsis = "..."
        post_ellipsis = ""
        if self._result_set.total_count > \
                len(self._result_set) + self._result_set.offset:
            post_ellipsis = "..."
        return "<QuerySet [%s%s%s]>" % (
            pre_ellipsis,
            ", ".join(str(obj) for obj in self._result_set),
            post_ellipsis)

    def __iter__(self):
        """
        Return an iterator for the QuerySet
        """
        if not self._result_set:
            self._execute_query()
        #for index in range(0, min(self._result_set.total_count, self._result_set.limit)):
        for index in range(0, self._result_set.total_count):
            if index == self._result_set.offset + self._result_set.limit:
                self._execute_query()
                self._offset += self._result_set.limit
            response_dict = self._result_set.response_dict['objects'][index - self._offset]
            yield self.model(response_dict)
