from setuptools import setup

import mytardisclient

setup(name='mytardisclient',
      version=mytardisclient.__version__,
      description='Command-line client for MyTardis API',
      url='http://github.com/wettenhj/mytardisclient',
      author='James Wettenhall',
      author_email='james.wettenhall@monash.edu',
      license='GPL',
      packages=['mytardisclient'],
      entry_points={
          "console_scripts": [
              "mytardis = mytardisclient.client:run",
          ],
      },
      install_requires=['requests', 'ConfigParser', 'texttable'],
      zip_safe=False)
