==============================
Get Started Quickly With Grape
==============================

Before using the Grape buildout, you need to have access to a MySQL database.

Put the MySQL database connection information into your home folder::

  $ vim ~/.my.cnf

This is the example configuration that you can adapt to your system. Change the host to
your MySQL host::

  [client]
  host=pou
  user=guest
  password=guest

Ask your database administrator for a login of the guest user and read/write access to 
the following two databases on this host::

  - Test_RNAseqPipeline
  - Test_RNAseqPipelineCommon

Check out the buildout from svn::

  $ svn co --username guest --password guest svn://svn.crg.es/big/grape/grape.buildout/trunk grape.buildout
  $ cd grape.buildout

Edit the buildout.cfg file to point to the location of the Java and Perl binaries:

  [settings]
  java = /soft/bin/java
  perl = /soft/bin/perl

Get the testdata:

  $ wget -m 'ftp://ftp.encode.crg.cat/pub/rnaseq/pipeline/testdata' --directory-prefix=src/testdata --no-directories

Create a virtual environment and run the buildout::

  $ /path/to/your/python/bin/virtualenv --no-site-packages .
  $ bin/easy_install RestrictedPython
  $ bin/python bootstrap.py
  $ bin/buildout

After running buildout, the parts folder contains three folders with your RNASeq pipelines:

[+] parts
    [+] TestClusttrun
    [+] TestLocaltrun
    [+] TestTrunk

Go to one of the RNASeq pipelines and start it:
 
  $ cd parts/TestTrunk
  $./bin/start.sh

Then execute the pipeline

  $ ./bin/execute.sh

If you want to visualize the data in a web page, install the Raisin buildout available here:

  $ svn co svn co --username guest --password guest svn://svn.crg.es/big/raisin/raisin.buildout/trunk raisin.buildout
  
Enjoy!
