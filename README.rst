mytardisclient
--------------
|travis| |codecov| |readthedocs| |pyup| |python3|

 .. |travis| image:: https://travis-ci.org/mytardis/mytardisclient.svg?branch=master
    :target: https://travis-ci.org/mytardis/mytardisclient
    
.. |codecov| image:: https://codecov.io/gh/mytardis/mytardisclient/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/mytardis/mytardisclient/commits

.. |readthedocs| image:: https://readthedocs.org/projects/mytardisclient/badge/?version=latest
  :target: https://mytardisclient.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. |pyup| image:: https://pyup.io/repos/github/mytardis/mytardisclient/shield.svg
     :target: https://pyup.io/repos/github/mytardis/mytardisclient/
     :alt: Updates
     
.. |python3| image:: https://pyup.io/repos/github/mytardis/mytardisclient/python-3-shield.svg
     :target: https://pyup.io/repos/github/mytardis/mytardisclient/
     :alt: Python 3

Command Line Interface and Python classes for interacting with MyTardis's REST API.

Install::

    pip install git+https://github.com/mytardis/mytardisclient.git@master#egg=mytardisclient

Example
~~~~~~~

Determine the location of the configuration file where the MyTardis URL is specified::

  >>> from mtclient.conf import config
  >>> config.path
  '/Users/james/.config/mytardisclient/mytardisclient.cfg'
  >>> config.url
  'https://mytardis.example.com'

Use mytardisclient's Dataset model class to look up a public dataset
(with ID 125) from the MyTardis server, using its RESTful API::

  >>> from mtclient.models.dataset import Dataset
  >>> Dataset.objects.get(id=125)
  <Dataset: Test Public Dataset1>

The syntax is intended to be similar to Django ORM syntax, however it is not
nearly as powerful yet.

Tests
~~~~~

Tests can be run with::

  pytest --cov=mtclient

or::

  pytest --cov=mtclient --cov-report=html

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

Documentation can be built with::

 cd docs/
 make html
