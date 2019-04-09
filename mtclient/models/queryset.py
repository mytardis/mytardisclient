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
        self._filters = filters
        self._limit = limit
        self._offset = offset or 0
        self._order_by = order_by

        self._result_set = None

    def order_by(self, order_by):
        """
        Populate the self._order_by instance attribute
        """
        self._order_by = order_by
        return self

    def _execute_query(self):
        """
        The user has requested something which requires evaluating the query
        """
        self._result_set = self.model.list(
            filters=self._filters, limit=self._limit, offset=self._offset,
            order_by=self._order_by)

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
        for index in range(0, len(self._result_set)):
            response_dict = \
                self._result_set.response_dict['objects'][index]
            yield self.model(response_dict)

        while self._result_set.next:
            self._offset += self._result_set.limit
            self._execute_query()
            for index in range(0, len(self._result_set)):
                response_dict = \
                    self._result_set.response_dict['objects'][index]
                yield self.model(response_dict)
