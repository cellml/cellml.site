Installation (Upgrade) Instruction for www.cellml.org
=====================================================

Introduction
------------

The following instructions are for installing/upgrading Zope/Plone on
the server that are accessible via these three domain names:
::

    cellml.org
    site.cellml.org
    www.cellml.org

They currently all point to the same machine.


Important information
---------------------

The results created by this setup will result in these important files.

These startup scripts will be created.  They both follow typical \*nix
distribution conventions, i.e. $SCRIPT {start|stop}:

* /etc/init.d/cellml.org-instance

  - Daemon script for Zope/Plone

* /etc/init.d/cellml.org-zeoserver

  - Daemon script for Zeo (ZODB database server)

These other system files will be created/reconfigured manually:

* Apache2 (httpd)

  - /etc/httpd/conf.d/90_cellml.org.conf

Important paths on the filesystem not residing in /etc:

* /home/zope/cellml.site.instance/$DATE

  - Zope/Plone instance home directory

* /home/zope/cellml.site.zeoserver/$DATE

  - Zeo home directory

(Note: $DATE is the date of the last time that an installation requiring
extensive update step to Zope/Plone, which rarely happens for a standard
installation without extensive customization or other external packages
that are stable).

Important settings in there are found in the files relative to the 
Zope/Plone instance directory:

* buildout.cfg

  - Installation configuration file for the buildout system.  Please
    refer to its documentation for detailed information.

* parts/instance-deploy/etc/zope.conf

  - Other Zope specific configuration settings, include locations of
    log files, other security settings, location of the zodb server
    and the like.
  - This file is automatically generated.  Refer to buildout.cfg.

Important settings in there are found in the files relative to the 
Zeo home directory:

* buildout.cfg
  - See above.

* parts/zeoserver-deploy/etc/zeo.conf

  - Contains location of log files and port numbers.
  - This file is automatically generated.  Refer to buildout.cfg.


Checklist for making a release
------------------------------

(very similar to models.cellml.org, but this can be quicker as
Zope/Plone is stable and reinstallation is unlikely to happen at this
point in time.)

For creating a staging instance, the detailed instructions for 
deployment may be followed, but some steps could be simplified (such
as not needing ssh tunnels, not using the deployment split buildout or
the default test instance buildout).

For reliable testing, do get a copy of the live Data.fs, but do change
the admin password for that copy to prevent mixup with logging into the
production copy.

Then stage this on an identical VM as a dry run before repeating this
on the production server using the instructions below.  Verify that the
tests passed and no other visible flaws are found (also let those
nominated users have a go at it, if firewall permitting).


Operational procedures on production/deployment server
------------------------------------------------------

The instructions below assume these conditions are met:

0) user can ssh to www.cellml.org;
1) sudo as the zope user on the server;
2) create ssh tunnel to the internal zope server port;
3) navigate around the ZMI;
4) know the IP address of the ABI proxy, or access to a known proxy;
5) know how to configure Apache reverse proxy;
6) reconfigure the virtual host monster string to the upgraded server;
7) know how to setup init.d/rc.# scripts.

Optional, but extremely helpful knowledge:

0) use screen for multiple terminal windows.


Detailed instructions for fresh deployment
------------------------------------------

Get a shell on the production server using your favorite terminal 
emulator, then sudo as zope like so.
::

    upi000@abiwwwprd02 ~ $ sudo -H -u zope http_proxy=<...> bash

Enter the location of the http_proxy as installation requires packages
from pypi and other places outside the firewall.

Once that is done, go into the root of the default CellML site checkout:
::

    zope@abiwwwprd02 /home/upi000 $ cd ~/cellml.site

Update the local checkout of the buildout git svn clone.
::

    $ git svn rebase

Do note at this point in time, I have not created a live branch with the
proxy information.  Doing a git diff should show you the differences.
If/when this is fixed, you can do something like
::

    $ git checkout live
    $ git merge remote/trunk  # or the latest version branch

Resolve all conflicts and commit them if any exists.

Open up the buildout file and make sure the port numbers specified are
not being used by the current production server.  The actual buildout is
not executed here, but in the two other subdirectories (screen is useful
to open these two locations at once), which resides in:
::

    ${INSTANCE_HOME}    /home/zope/cellml.site.instance/`date +%Y%m%d`
    ${ZEOSERVER_HOME}   /home/zope/cellml.site.zeo/`date +%Y%m%d`

(Note: `date +%Y%m%d` generates the current datestamp)

Alternatively, if you are trying to updating a minor point release, you
may go directly into the current directories.

The current servers should reside in each of these datestamped 
directories.  So what you would do is to clone or export the git local
clone into a new directory in this format, and then run the respective
buildout scripts in them after bootstrapping (in both of them) like so:

In ${ZEOSERVER_HOME}
::

    $ git clone /home/zope/cellml.site ${ZEOSERVER_HOME}
    $ cd ${ZEOSERVER_HOME}
    $ python2.4 bootstrap.py
    $ bin/buildout -c zeo-instance.cfg

In ${INSTANCE_HOME}
::

    $ git clone /home/zope/cellml.site ${INSTANCE_HOME}
    $ cd ${INSTANCE_HOME}
    $ python2.4 bootstrap.py
    $ bin/buildout -c deploy-instance.cfg

Hopefully everything should build without errors.  Go get a sandwich
during the mean time as it takes about 15-30 minutes.

If everything is done, go back into the ${INSTANCE_HOME} directory and
run tests.
::

    $ bin/instance test -s cellml

This tests the CellML Theme package such that it works.

If doing a new installation, obtain a clone of current Data.fs.  Do pack
it using the ZML (or alternatively through the command line) and then
put it into ${ZEOSERVER_HOME}/var/filestorage.


Manually starting Zope
----------------------

Note: If there is an existing running installation, you may need to
change the port numbers specified in the buildout.cfg file, and rerun
the buildout steps.  It should not take as long as all it will do is
scan through your installation and find that all files are in place, and
recreate the startup scripts.

To start PMR2, the database must be started, it can be done like so:
::

    $ ${ZEOSERVER_HOME}/bin/zeoserver-deploy start

Now start the instance using paster, but run it in the foreground.
::

    $ ${ZEOSERVER_HOME}/bin/instance-deploy start


Testing/Upgrading the new deployed server
-----------------------------------------

If this deployment step is done on the production server (to facilitate
final testing on production, for instance), you will need to set up port
forwarding as our data center routing rules only permit ssh, http and
https.

Once everything started and ssh tunnel set up, the upgrade may procede.

In the products installation zmi menu, reinstall all affected products.
This usually means The CellML Theme.

Run any extra migration scripts if necessary.

Verify all contents look the same.

Then everything should be ready.


Final configuration for deployment
----------------------------------

At this point the PMR2 specific settings for Apache must be reconfigured
to point to the new port.  You will again need sudo rights as root to
edit the following file:
::

    /etc/httpd/conf.d/90_cellml.org.conf

Change the ProxyPass and ProxyPassReverse to use the port number of the
newly installed, configured and/or upgraded instance for every vhosts
defined in that file.

Send out notification about the impending brief downtime to PMR2 to the
appropriate mailing lists and/or users.

Reload apache.  It should come back with this fresh but manually started
daemon.
::

    $ sudo /etc/init.d/httpd reload

The old daemons could be stopped at this point as it is no longer 
needed or accessible from the outside world.
::

    $ sudo /etc/init.d/cellml.org-instance stop
    $ sudo /etc/init.d/cellml.org-zeoserver stop

Verify that everything is again in working order when accessed via the
following URIs:
::

    http://www.cellml.org/

The old init.d scripts need to be moved to allow the new ones be
symlinked.
::

    $ cd /etc/init.d
    $ sudo mv cellml.org-instance cellml.org-instance.old
    $ sudo mv cellml.org-zeoserver cellml.org-zeoserver.old
    $ sudo ln -s ${INSTANCE_HOME}/bin/instance-deploy
    $ sudo ln -s ${ZEOSERVER_HOME}/bin/zeoserver-deploy

Stop the temporary server (this causes the downtime).
::

    $ ${ZEOSERVER_HOME}/bin/zeoserver-deploy stop
    $ ${ZEOSERVER_HOME}/bin/instance-deploy stop

Start the new instance again as a normal service via /etc/init.d):
::

    $ sudo /etc/init.d/cellml.org-zeoserver start
    $ sudo /etc/init.d/cellml.org-instance start

If this was a completely fresh installation, please consult your system
distribution's manual on how to get those services to automatically
started/stopped with the machine.

We are done.


Known Issues
------------

In Red Hat Enterprise Linux

- The provided python-setuptools package is out of date.  Remove it to
  prevent conflicts during buildout.
