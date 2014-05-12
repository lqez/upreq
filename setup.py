#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA
import os.path

setup(
    name='upreq',
    version='0.0.1',
    py_modules=['upreq'],
    author='Park Hyunwoo',
    author_email='ez.amiryo' '@' 'gmail.com',
    maintainer='Park Hyunwoo',
    maintainer_email='ez.amiryo' '@' 'gmail.com',
    url='http://github.com/lqez/upreq',
    description='Update requirements.txt with pip freeze result',
    entry_points={
        'console_scripts': [
            'upreq = upreq:main',
        ],
    },
)
