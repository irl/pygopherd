README for Pygopherd for Python 3
=================================

[![Build Status](https://travis-ci.org/irl/pygopherd.svg?branch=master)](https://travis-ci.org/irl/pygopherd)

This is a fork of Pygopherd. It's probably not useful to you.

QUICKSTART (non-Debian)
-----------------------

1. Download and install Python 3.6 or above from your Linux distribution.

You can run pygopherd either in-place (as a regular user account) or
as a system-wide daemon.  For running in-place, do this:

1. Modify conf/pygopherd.conf:
   * Set usechroot = no
   * Comment out (add a # sign to the start of the line) the 
     pidfile, setuid, and setgid lines
   * Set mimetypes = ./conf/mime.types
   * Set root = to something appropriate.
   * Set port to a number greater than 1024.

2. Modify the first line of executables/pygopherd to reflect
   the location of your Python installation.

3. Invoke pygopherd by running:
   ./executables/pygopherd

For installing:

1. Run python3 setup.py install

2. Make sure that the /etc/pygopherd/pygopherd.conf names valid users
   (setuid, setgid) and valid document root (root).
