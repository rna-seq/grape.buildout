.. _quick_pipeline_run:

Quickly test Grape with one of your your own datasets
=================================================

You can try out Grape with an example set of reads for the following species:

    * Homo sapiens
    * Mus musculus
    * Drosophila Melanogaster

Just download the genome and annotation for your species and follow the 
instructions in the README.txt:
    
For Homo Sapiens:

    $ cd pipelines/Quick
    $ wget http://genome.crg.es/~mroder/grape/gencode.v7.annotation.ok.gtf
    $ wget http://genome.crg.es/~mroder/grape/H.sapiens.genome.hg19.main.fa
    $ cp /path/to/a/set/of/read/files/*.fastq.gz .
    $ cat README.txt

For Mus musculus

    $ cd pipelines/Quick
    $ wget http://genome.crg.es/~mroder/grape/mm9_ucsc_UCSC_genes.gtf
    $ wget http://genome.crg.es/~mroder/grape/M.musculus.genome.mm9.main.fa
    $ cp /path/to/a/set/of/read/files/*.fastq.gz .
    $ cat README.txt

For Drosophila Melanogaster:

    $ cd pipelines/Quick
    $ wget http://genome.crg.es/~mroder/grape/flyBase.exons.genes_real.transcripts.gtf
    $ wget http://genome.crg.es/~mroder/grape/D.melanogaster.genome.fa
    $ cp /path/to/a/set/of/read/files/*.fastq.gz .
    $ cat README.txt

Create databases for your project
---------------------------------

You need two databases for the Quick project:

    1. Quick_RNAseqPipeline
    2. Quick_RNAseqPipelineCommon

The permissions you need to ask for are:

    * yourusername: read and write

Then you need to modify your MySQL configuration file: ~/.my.cnf

    [client]
    host=mysqlhost
    port=3306
    user=yourusername
    password=123

Run the buildout
----------------

You don't need to install Python, Python 2.6.6 should be available on your system.

You also don't need to install virtualenv, because it is available on our system as well:

    $ easy_install virtualenv

Run virtualenv:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ virtualenv --no-site-packages .

Run the bootstrap.py file with the python binary that has been made available by virtualenv in the bin folder:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ ./bin/python bootstrap.py

Run the buildout:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ ./bin/buildout

The parts folder now contains everything you need to run the two pipelines:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ cd parts/
    tree
    .
    |-- Run
        |-- start.sh
        |-- execute.sh
        `-- ...
    
Run the pipeline
----------------

Now it is time to run the first pipeline so that the index files for the genome and annotation
can be generated.

Go to the parts folder and run the start script:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ cd parts
    $ cd Run
    $ ./start.sh

If you get errors, you can store them into an error.log file like this:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ cd parts/
    $ cd Run
    $ ./start.sh 2> error.log

In case everything worked ok, you can run the execute script:

    $ cd grape
    $ cd pipelines
    $ cd Quick
    $ cd parts/
    $ cd parts/Run
    $ ./execute.sh
