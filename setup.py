from setuptools import setup, find_packages
import sys
import os

version = '0.1'

install_requires = [ ]

setup(name='ptwitter',
      version=version,
      description="A command line tool for twitter",
      author="kumarak",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True)
