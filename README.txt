==========================================
Grape RNAseq Analysis Pipeline Environment
==========================================

High throughput sequencing technologies generate vast amounts of data that 
require subsequent management, analysis and visualization.

The Grape RNAseq Analysis Pipeline Environment implements a set of workflows 
that allow for easy exploration of RNAseq data. Among other features, it 
enables the users to perform

* quality checks
* read mapping
* eneration of expression and splicing statistics

The results are stored in a MySQL database and become immediately available
through a RESTful back end server that is connected to a web application using 
the Google chart tools for display.

For further information and downloading, please refer to the home page:

http://big.crg.cat/services/grape

============
Dependencies
============

You need to have access to a MySQL database

Make sure to have the following standard programming languages installed:

   Perl
    Java
    R
    Python

The following Perl modules must be installed

    DBI
    DBD::mysql
    Bio::DB::Fasta
    Bundle::BioPerl
    Bio::Seq
    Bio::DB::Sam

You need to have the following module installed in Python:

    virtualenv

==============================
Get Started Quickly With Grape
==============================

You can try out Grape with an example set of reads for the following species:

    * Homo sapiens
    * Mus musculus
    * Drosophila Melanogaster

Just download the genome and annotation for your species and follow the 
instructions in the README.txt:

For Homo Sapiens:

    cd pipelines/Quick
    wget http://genome.crg.es/~mroder/grape/gencode.v7.annotation.ok.gtf
    wget http://genome.crg.es/~mroder/grape/H.sapiens.genome.hg19.main.fa
    cp /path/to/a/set/of/read/files/*.fastq.gz .
    cat README.txt

For Mus musculus

    cd pipelines/Quick
    wget http://genome.crg.es/~mroder/grape/mm9_ucsc_UCSC_genes.gtf
    wget http://genome.crg.es/~mroder/grape/M.musculus.genome.mm9.main.fa
    cp /path/to/a/set/of/read/files/*.fastq.gz .
    cat README.txt

For Drosophila Melanogaster:

    cd pipelines/Quick
    wget http://genome.crg.es/~mroder/grape/flyBase.exons.genes_real.transcripts.gtf
    wget http://genome.crg.es/~mroder/grape/D.melanogaster.genome.fa
    cp /path/to/a/set/of/read/files/*.fastq.gz .
    cat README.txt

=============
Testing Grape
=============

If you want to test Grape with a test dataset, go to the Test pipeline folder:

    cd pipelines/Test

Then follow the README.txt

================
Grape web server
================

If you want to install the Grape web server, go the the devel server folder:

    cd servers/devel

Then follow the README.txt
