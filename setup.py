# -*- coding: utf-8 -*-
"""Installer for the massloader.atreal.massloader package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '3.2.0.dev0'

long_description = \
    read('README.rst') + \
    read('CHANGES.rst') + \
    read('docs', 'LICENSE.rst')

setup(name='atreal.massloader',
    version=version,
    description="Add an action to import zip files.",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='atReal',
    author_email='contact@atreal.fr',
    url='http://pypi.python.org/pypi/atreal.massloader',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['atreal'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Pillow',
        'Plone',
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'coverage',
            'flake8',
            'jarn.mkrelease',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'Sphinx',
            'zest.releaser',
            'zptlint',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
