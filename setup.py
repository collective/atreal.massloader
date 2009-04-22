from setuptools import setup, find_packages
import os

version = '2.1.0-beta1'

setup(name='atreal.massloader',
      version=version,
      description="Add an action to import zip files.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='atReal',
      author_email='contact@atreal.net',
      url='http://www.atreal.net/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['atreal'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
