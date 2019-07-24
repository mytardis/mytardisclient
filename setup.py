"""
setup.py for mytardisclient

Build docs:
  python setup.py build_sphinx

Upload source distribution:
    # Put credentials in ~/.pypirc
    rm dist/*
    python setup.py sdist
    pip install twine
    twine upload dist/*
"""
import os
from setuptools import setup
from setuptools import find_packages

import mtclient

# read the contents of your README file
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(THIS_DIR, 'README.rst')) as readme:
    LONG_DESCRIPTION = readme.read()

setup(name='mytardisclient',
      packages=find_packages(),
      version=mtclient.__version__,
      description="Command Line Interface and Python classes "
      "for interacting with MyTardis's REST API.",
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/x-rst',
      author='James Wettenhall',
      author_email='james.wettenhall@monash.edu',
      url='http://github.com/mytardis/mytardisclient',
      download_url='https://github.com/mytardis/mytardisclient'
      '/archive/%s.tar.gz' % mtclient.__version__,
      keywords=['mytardis', 'REST'], # arbitrary keywords
      classifiers=[],
      license='GPL',
      entry_points={
          "console_scripts": [
              "mytardis = mtclient.client:run",
          ],
      },
      install_requires=['requests', 'pyopenssl', 'ndg-httpsclient', 'pyasn1',
                        'configparser', 'texttable', 'dogpile.cache', 'six',
                        'clint'],
      zip_safe=False)
