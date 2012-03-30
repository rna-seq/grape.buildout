==================================================
Benchmark pipeline run for Drosophila Melanogaster
==================================================

In order to run this benchmark, download the genome and annotation:

    cd pipelines/BenchDM
    wget http://genome.crg.es/~mroder/grape/flyBase.exons.genes_real.transcripts.gtf
    wget http://genome.crg.es/~mroder/grape/D.melanogaster.genome.fa
    wget ...

== Create databases for your project ==

You need two databases for the BenchDM project:

 1. BenchDM_RNAseqPipeline
 2. BenchDM_RNAseqPipelineCommon

The permissions you need to ask for are:

 * yourusername: read and write

Then you need to modify your MySQL configuration file: ~/.my.cnf

<pre>
[client]
host=mysqlhost
port=3306
user=yourusername
password=123
</pre>

== Run the buildout ==

Run virtualenv, which you should have installed for Python:

<pre>
cd grape
cd pipelines
cd BenchDM
virtualenv --no-site-packages .
</pre>

Run the bootstrap.py file with the python binary that has been made available 
by virtualenv in the bin folder:

<pre>
cd grape
cd pipelines
cd BenchDM
./bin/python bootstrap.py
</pre>

Run the buildout:

<pre>
cd grape
cd pipelines
cd BenchDM
./bin/buildout
</pre>

The parts folder now contains everything you need to run the two pipelines:

<pre>
cd grape
cd pipelines
cd BenchDM
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

<pre>
cd grape
cd pipelines
cd BenchDM
cd parts/
cd parts/Run
./start.sh
</pre>

If you get errors, you can store them into an error.log file like this:

<pre>
cd grape
cd pipelines
cd Quick
cd parts/
cd parts/Run
./start.sh 2> error.log
</pre>

In case everything worked ok, you can run the execute script:

<pre>
cd grape
cd pipelines
cd Quick
cd parts/
cd parts/Run
./execute.sh
</pre>
