Custom Pipeline
===============


Choosing a project name
-----------------------

Choose your project name wisely. Some examples:

    * CLL
    * ENCODE
    * HBM

Let's say you have a project about Drosophila and you are interested in Selenoproteins, 
you choose the project name 'Dsel'. We are going to use the project name 'MyProject'
here.

Layout
------

There are a number of top level folders containing configuration files, like accessions,
and  profiles. We'll come back to these later, but right now we will create a custom 
folder for our project inside the pipelines folder.

    $ cd grape
    $ cd pipelines
    $ mkdir MyProject
    $ cd MyProject

Now copy some files over from the Test folder:

    $ cp ../Test/bootstrap.py .
    $ cp ../Test/buildout.cfg .

Configure the buildout.cfg
--------------------------

The content of the buildout.cfg needs to be adapted to your project:

    [buildout]
    extends = ../dependencies.cfg
              ../../accessions/Test/db.cfg
              ../../profiles/Test/db.cfg
    
Change this to:

    [buildout]
    extends = ../dependencies.cfg
              ../../accessions/MyProject/db.cfg
              ../../profiles/MyProject/db.cfg

Adding a configuration file for the accessions
----------------------------------------------

Add a project folder to the top level accessions folder, and add a db.cfg file:

    cd grape
    cd accessions
    mkdir MyProject
    cd MyProject
    touch db.cfg

We'll cover how to configure this file after taking care of the profile.

Adding a configuration file for the profile
-------------------------------------------

Add a project folder to the top level profiles folder, and add a db.cfg file:

    cd grape
    cd profiles
    mkdir MyProject
    cd MyProject
    touch db.cfg

Configuring the profile
-----------------------

Let's copy over the configuration for the profile of the Test project.

    cd grape
    cd profiles
    cd MyProject
    cp ../Test/db.cfg .

We adapt this file to our case:

    [runs]
    parts = Male
            Female
    
    [pipeline]
    TEMPLATE   = ${buildout:directory}/src/pipeline/template3.0.txt
    PROJECTID  = MyProject
    DB         = MyProject_RNAseqPipeline
    COMMONDB   = MyProject_RNAseqPipelineCommon
    HOST       = pou
    THREADS    = 2
    MAPPER     = GEM
    MISMATCHES = 2
    CLUSTER    = mem_6
    ANNOTATION = /users/yourusername/Drosophilas/Dwill/dwil_all_r1.3.gff
    GENOMESEQ  = /users/yourusername/Genomes/Drosophila_willistoni/genome.fa
    
    [Male]
    recipe = grape.recipe.pipeline
    accession = Male
    
    [Female]
    recipe = grape.recipe.pipeline
    accession = Female

What we have done in this configuration is:

    1. Decide how to call the pipeline runs: Male and Female
    2. Configured the Databases in which to store the results: MyProject_RNAseqPipeline and MyProject_RNAseqPipelineCommon
    3. Given the location of the annotation and the genome
    4. Configured the pipelines to be run on the cluster with 2 threads

Configuring the accessions
--------------------------

Let's copy over the configuration for the profile of the MyProject project.

    cd grape
    cd accessions
    cd MyProject

Edit the db.cfg file we created earlier.

    [Female]
    file_location = /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_female_read1_qseq.fastq
                    /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_female_read2_qseq.fastq
    mate_id = Female.1
              Female.2
    pair_id = Female
              Female
    label = Female
            Female
    gender = female
    dataType=RNASeq
    cell=CELL
    rnaExtract=UNKNOWN
    localization=CELL
    replicate=1
    lab=CRG
    type=fastq
    readType=2x96
    qualities=phred
    species=Drosophila willistoni
    
    [Male]
    file_location = /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_male_read1_qseq.fastq
                    /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_male_read2_qseq.fastq
    mate_id = Male.1
              Male.2
    pair_id = Male
              Male
    label = Male
            Male
    gender = male
    dataType=RNASeq
    cell=CELL
    rnaExtract=UNKNOWN
    localization=CELL
    replicate=1
    lab=CRG
    type=fastq
    readType=2x96
    qualities=phred
    species=Drosophila willistoni

Now you have the two accessions defined and the profiles specify how to run the 
two pipelines. Now we need a database for storing the results of the pipeline runs.

Create databases for your project
---------------------------------

You need two databases for the MyProject project:

    1. MyProject_RNAseqPipeline
    2. MyProject_RNAseqPipelineCommon

The permissions you need to ask for are:

    1. rnaseqweb: read
    2. yourusername: read and write

The rnaseqweb user needs read access in order to show the statistical results.

You needs to have read write access.

Then you need to modify your MySQL configuration file: ~/.my.cnf

	[client]
	host=mysqlserver
	port=3306
	user=yourusername
	password=123

Run the buildout
----------------

Run virtualenv:

	cd grape
	cd pipelines
	cd MyProject
	virtualenv --no-site-packages .

If you get an error, you may have to remove your .pydistutils.cfg file.

    .pydistutils.cfg

Run the bootstrap.py file with the python binary that has been made available by virtualenv in the bin folder:

	cd grape
	cd pipelines
	cd MyProject
	./bin/python bootstrap.py

Run the buildout:

	cd grape
	cd pipelines
	cd MyProject
	./bin/buildout

The parts folder now contains everything you need to run the two pipelines:

	cd grape
	cd pipelines
	cd MyProject
	cd parts/
	tree
	.
	|-- Female
	|   |-- GEMIndices -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/GEMIndices
	|   |-- bin -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/pipeline/bin
	|   |-- clean.sh
	|   |-- execute.sh
	|   |-- lib -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/pipeline/lib
	|   |-- read.list.txt
	|   |-- readData
	|   |   |-- lane8_W_female_read1_qseq.fastq -> /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_female_read1_qseq.fastq
	|   |   `-- lane8_W_female_read2_qseq.fastq -> /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_female_read2_qseq.fastq
	|   |-- results -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/Female
	|   `-- start.sh
	|-- Male
	|   |-- GEMIndices -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/GEMIndices
	|   |-- bin -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/pipeline/bin
	|   |-- clean.sh
	|   |-- execute.sh
	|   |-- lib -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/pipeline/lib
	|   |-- read.list.txt
	|   |-- readData
	|   |   |-- lane8_W_male_read1_qseq.fastq -> /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_male_read1_qseq.fastq
	|   |   `-- lane8_W_male_read2_qseq.fastq -> /users/myusername/sequencing_drosophilas_saltans/RNAseq/fastq/lane8_W_male_read2_qseq.fastq
	|   |-- results -> /users/yourusername/Drosophilas/Dwill/Pipeline/pipelines/MyProject/var/Male
	|   `-- start.sh
	`-- buildout

Run the first pipeline
----------------------

Now it is time to run the first pipeline so that the index files for the genome and
annotation can be generated. Once these files are present we can run all the other 
pipelines in parallel.

Go to the parts folder and run the start script:

    cd grape
    cd pipelines
    cd MyProject
    cd parts/
    cd parts/Female
    ./start.sh

If you get errors, you can store them into an error.log file like this:

    cd grape
    cd pipelines
    cd MyProject
    cd parts/
    cd parts/Female
    ./start.sh 2> error.log

In case everything worked ok, you can run the execute script:

    cd grape
    cd pipelines
    cd MyProject
    cd parts/
    cd parts/Female
    ./execute.sh

Run the other pipeline
----------------------

The second pipeline is run exactly like the first one:

Go to the parts folder and run the start script:

    cd grape
    cd pipelines
    cd MyProject
    cd parts/
    cd parts/Male
    ./start.sh

If you get errors, you can store them into an error.log file like this:

    cd grape
    cd pipelines
    cd MyProject
    cd parts/
    cd parts/Male
    ./start.sh 2> error.log

In case everything worked ok, you can run the execute script:

    cd grape
    cd pipelines
    cd MyProject
    cd parts/
    cd parts/Male
    ./execute.sh
