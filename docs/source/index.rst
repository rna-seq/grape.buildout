Grape Buildout
==============

This buildout configures Grape pipelines, used for processing 
and analyzing RNA-Seq data.

`Grape Homepage <http://big.crg.cat/services/grape)>`_

To install it, check out :ref:`installation`

If you want to use Grape with your datasets, then go to the pipelines folder and
create a sub folder with your project name

    $ cd pipelines/MyProjectName

then follow :ref:`custom_pipeline_run`

If you want to test Grape with a minimal test dataset, go to the Test pipeline
folder::

    $ cd pipelines/Test

Then follow :ref:`test_pipeline_run`

If you want to test Grape with your own test dataset, go to the Quick pipeline
folder::

    $ cd pipelines/Quick

Then follow :ref:`quick_pipeline_run`


If you want to install the Raisin web server, go the the devel server folder::

    $ cd servers/devel

Then follow :ref:`run_raisin_web_server`

Contents:

.. toctree::
   :maxdepth: 2

   installation
   custom_pipeline_run
   test_pipeline_run
   quick_pipeline_run
   run_raisin_web_server   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
