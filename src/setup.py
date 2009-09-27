from setuptools import setup, find_packages
import os

version = '0'

setup(name='cellml.site',
      version=version,
      description="CellML Site",
      long_description=open("README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        ],
      keywords='zope plone',
      author='CellML Web Working Group',
      author_email='team@cellml.org',
      url='http://www.cellml.org/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cellml'],
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
