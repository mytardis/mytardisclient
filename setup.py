"""
setup.py for mytardisclient

python setup.py develop
python setup.py sdist
etc.
"""
from setuptools import setup
from setuptools import find_packages

import mytardisclient

setup(name='mytardisclient',
      packages=find_packages(),
      version=mytardisclient.__version__,
      description='Command-line client for MyTardis API',
      author='James Wettenhall',
      author_email='james.wettenhall@monash.edu',
      url='http://github.com/wettenhj/mytardisclient',
      download_url='https://github.com/wettenhj/mytardisclient/archive/0.0.7.tar.gz',
      keywords=['mytardis', 'REST'], # arbitrary keywords
      classifiers=[],
      license='GPL',
      entry_points={
          "console_scripts": [
              "mytardis = mytardisclient.client:run",
          ],
      },
      install_requires=['requests', 'ConfigParser', 'texttable',
                        'dogpile.cache'],
      zip_safe=False)
