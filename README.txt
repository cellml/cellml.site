This is the standard CellML website buildout.

To test, just do:
::

    $ python2.4 bootstrap.py
    $ bin/buildout

Start it off by
::

    $ bin/zeoserver-testing start
    $ bin/instance-testing start

If you are trying to stage this, please use the appropriate buildout
configuration file.
::

    $ bin/buildout -c staging-instance.cfg

Since Zope 2.4, VirtualHostMonster is recommended over SiteRoot to put
Zope behind Apache and have all requests be redirected correctly.  In
this case, this will be the URI to use:

http://localhost:13080/VirtualHostBase/http/www.cellml.org:80/cellml/VirtualHostRoot/

For https, this will be the URI:

http://localhost:13080/VirtualHostBase/https/www.cellml.org:443/cellml/VirtualHostRoot/
