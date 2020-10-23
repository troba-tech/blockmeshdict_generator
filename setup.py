# -*- coding: utf-8 -*-
"""
    Setup file for datacenter_room_regulation.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys

from pkg_resources import VersionConflict, require
from setuptools import setup

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

def get_requirements_from_files():
    """
    Collect all dependencies required to run the project from requirements files
    :return: a list of required packages
    """
    with open('requirements.txt', 'r') as pypi_lines:
        requirement_list = pypi_lines.readlines()

    return [elt for elt in requirement_list]


if __name__ == "__main__":
    setup(
        use_pyscaffold=True,
        install_requires=get_requirements_from_files()
    )
