README for Pygopherd for Python 3
=================================

[![Build Status](https://travis-ci.org/irl/pygopherd3k.svg?branch=master)](https://travis-ci.org/irl/pygopherd3k)
[![Coverage Status](https://coveralls.io/repos/github/irl/pygopherd3k/badge.svg?branch=master)](https://coveralls.io/github/irl/pygopherd3k?branch=master)
[![Code Health](https://landscape.io/github/irl/pygopherd3k/master/landscape.svg?style=flat)](https://landscape.io/github/irl/pygopherd3k/master)

This is a fork of [Pygopherd](https://github.com/jgoerzen/pygopherd). It is
still experimental and there are probably still things that are broken.

Try it out
----------

1. Modify conf/pygopherd.conf:

   * Set usechroot = no (expect that chroot will be broken)
   * Comment out (add a # sign to the start of the line) the 
     pidfile, setuid, and setgid lines
   * Set mimetypes = ./conf/mime.types
   * Set root = to something appropriate.
   * Set port to a number greater than 1024.

2. Modify the first line of bin/pygopherd to reflect
   the location of your Python installation.

3. Invoke pygopherd by running:
   `PYTHONPATH=. ./bin/pygopherd`
