"""
setup.py for mtclient

Update and upload docs:
  python setup.py build_sphinx
  python setup.py upload_sphinx

Upload source distribution:
    python setup.py sdist upload
"""
from setuptools import setup
from setuptools import find_packages

import mtclient

setup(name='mytardisclient',
      packages=find_packages(),
      version=mtclient.__version__,
      description="Command Line Interface and Python classes "
      "for interacting with MyTardis's REST API.",
      long_description='',
      author='James Wettenhall',
      author_email='james.wettenhall@monash.edu',
      url='http://github.com/jameswettenhall/mytardisclient',
      download_url='https://github.com/jameswettenhall/mytardisclient'
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
