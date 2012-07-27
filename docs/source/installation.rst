.. _installation:

Installing the Grape Buildout
=============================

Download grape.buildout::

`Grape Homepage <http://big.crg.cat/services/grape>`_

After downloading the package, unpack it::

    $ tar xfvz grape.buildout-1.7.tar.gz
    $ cd grape.buildout-1.7

Dependencies
------------

You need to have access to a MySQL database.

- MySQL 5.1.45 or above

Make sure to have the following standard programming languages installed:

- Perl 5.10.1 or above

- R 2.13.0 or above

- Python 2.6.x

- Java 1.6 compliant runtime environment is necessary.

It is recommended to employ the most recent Java Runtime Environment (JRE) available
from the traditional Java project:

`Java Project <http://java.com/en/download/index.jsp>`_

The following Perl modules must be installed

- DBI
- DBD::mysql
- Bio::DB::Fasta
- Bundle::BioPerl
- Bio::Seq
- Bio::DB::Sam

If you have trouble installing the Bio::DB::Sam package, you may have to
edit the Makefile and add a -fPIC flag.

You need to have the following module installed in Python:

- virtualenv
