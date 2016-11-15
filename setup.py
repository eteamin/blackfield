# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages
py_version = sys.version_info[:2]


install_requires = [
    "Cython==0.23",
    "pygame",
    "kivy",
    "coverage"
]

setup(
    name='blackfield',
    version='0.1-dev',
    description='',
    author='eteamin',
    author_email='aminetesamian1371@gmail.com',
    url='https://github.com/eteamin/blackfield',
    packages=find_packages(),
    install_requires=install_requires,
)