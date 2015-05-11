# coding: utf-8

"""
Some glue around luigi.

Provides a base class, that autogenerates its output filenames based on some
tag, classname and parameters.

Additionally, provide some smaller utilities, like a TSV format, a benchmark
decorator and some task templates.
"""
from setuptools import setup

setup(name='pyqueued',
      version='0.1.2',
      description='A client for queued.',
      url='https://github.com/miku/pyqueued',
      author='Martin Czygan',
      author_email='martin.czygan@gmail.com',
      py_modules=['pyqueued'],
      install_requires=['requests>=2'],
)
