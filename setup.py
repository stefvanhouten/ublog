"""uweb3 blog installer."""

import os
import re
from setuptools import setup, find_packages

REQUIREMENTS = [
    'uweb3',
]


def readme():
  with file(os.path.join(os.path.dirname(__file__), 'README.md')) as r_file:
    return r_file.read()


def version():
  main_lib = os.path.join(os.path.dirname(__file__), 'blog', 'pages.py')
  with file(main_lib) as v_file:
    return re.match(".*__version__ = '(.*?)'", str(v_file.read()), re.S).group(1)

setup(
    name='blog',
    version='1.1',
    description='A uweb3 based blog.',
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: uweb3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"],
    dependency_links=[
        '', ],
    author='Arjen',
    author_email='arjen@underdark.nl',
    url='',
    keywords='web uweb3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS)
