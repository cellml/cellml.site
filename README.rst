Introduction
============

This is the standard buildout configuration for the `CellML Website`_.

.. _CellML Website: https://www.cellml.org/

To install, it requires the standard set of system dependencies needed
for a Zope/Plone installation, namely the C compiler, Python 2.7 header
files and build related packages.  On a Debian/Ubuntu compatible system
please install the following packages:

* build-essential
* zlib1g-dev
* libxml2-dev
* libxslt1-dev
* python2.7-dev

To test, just do::

    $ python2.7 bootstrap.py
    $ bin/buildout

Start it off by::

    $ bin/zeoserver-testing start
    $ bin/instance-testing start

If you are trying to stage this, please use the appropriate buildout
configuration file::

    $ bin/buildout -c staging-instance.cfg

Since Zope 2.4, VirtualHostMonster is recommended over SiteRoot to put
Zope behind Apache and have all requests be redirected correctly.  In
this case, this will be the URI to use:

http://localhost:13080/VirtualHostBase/http/www.cellml.org:80/cellml/VirtualHostRoot/

For https, this will be the URI:

http://localhost:13080/VirtualHostBase/https/www.cellml.org:443/cellml/VirtualHostRoot/


