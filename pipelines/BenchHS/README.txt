=======================================
Benchmark pipeline run for Homo sapiens
=======================================

In order to run this benchmark, download the genome, annotation and read files:

    cd pipelines/BenchDM
    wget http://genome.crg.es/~mroder/grape/gencode.v7.annotation.ok.gtf
    wget http://genome.crg.es/~mroder/grape/H.sapiens.genome.hg19.main.fa
    wget ...

== Create databases for your project ==

You need two databases for the BenchDM project:

 1. BenchHS_RNAseqPipeline
 2. BenchHS_RNAseqPipelineCommon

The permissions you need to ask for are:

 * yourusername: read and write

Then you need to modify your MySQL configuration file: ~/.my.cnf

[client]
host=mysqlhost
port=3306
user=yourusername
password=123

== Run the buildout ==

Run virtualenv, which you should have installed for Python:

cd grape
cd pipelines
cd BenchHS
virtualenv --no-site-packages .

Run the bootstrap.py file with the python binary that has been made available 
by virtualenv in the bin folder:

cd grape
cd pipelines
cd BenchHS
./bin/python bootstrap.py

Run the buildout:

cd grape
cd pipelines
cd BenchHS
./bin/buildout

The parts folder now contains everything you need to run the two pipelines:

cd grape
cd pipelines
cd BenchHS
cd parts/
tree
.
|-- Run
    |-- start.sh
    |-- execute.sh
    `-- ...
    
== Run the pipeline ==

Now it is time to run the first pipeline so that the index files for the genome
and annotation can be generated.

Go to the parts folder and run the start script:

cd grape
cd pipelines
cd BenchHS
cd parts/
cd parts/Run
./start.sh

If you get errors, you can store them into an error.log file like this:

cd grape
cd pipelines
cd BenchHS
cd parts/
cd parts/Run
./start.sh 2> error.log

In case everything worked ok, you can run the execute script:

cd grape
cd pipelines
cd BenchHS
cd parts/
cd parts/Run
./execute.sh
