"""
This module is used by buildout by applying the z3c.recipe.runscript recipe
when building the RNASeq pipeline parts:

    [shortRNA001C]
    recipe = z3c.recipe.runscript
    update-script = prepare.py:main
    install-script = prepare.py:main
    accession = shortRNA001C
    pipeline = female

Both the update-script and install-script point to the prepare.py module and
its "main" method.

The accession attribute is necessary so that the corresponding files and
metadata for the pipeline run can be found in the accession database.

The pipeline attribute specifies the section defining the pipeline options.
"""

import os
import shutil
import glob
from subprocess import call
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.PrintCollector import PrintCollector


def run_python(code, accession):
    """
    Run some restricted Python code for constructing the labels of accessions
    """

    if code.startswith("python:"):
        raise AttributeError("Prefix python: should be removed")

    # In order to get the result of the Python code out, we have to wrap it
    # like this
    code = 'print ' + code + ';result = printed'

    # We compile the code in a restricted environment
    compiled = compile_restricted(code, '<string>', 'exec')

    # The getter is needed so that attributes from the accession can be used
    # for the labels
    def mygetitem(obj, attr):
        """Just get the attribute from the object"""
        return obj[attr]

    # The following globals are usable from the restricted Python code
    restricted_globals = dict(
        __builtins__=safe_builtins,  # Use only some safe Python builtins
        accession=accession,         # The accession is needed for the labels
        _print_=PrintCollector,      # Pass this to get hold of the result
        _getitem_=mygetitem,         # Needed for accessing the accession
        _getattr_=getattr)           # Pass the standard getattr

    # The code is now executed in the restricted environment
    exec(compiled) in restricted_globals

    # We collect the result variable from the restricted environment
    return restricted_globals['result']


def install_bin_folder(options, buildout, bin_folder):
    """
    The bin folder is made available globally to all pipelines
    in var/pipeline
    The shebang of all contained scripts has to be changed to use the Perl
    version defined in buildout.cfg
    """
    # Always start with a fresh installation, so remove the old bin folder in
    # var/pipeline
    shutil.rmtree(bin_folder, ignore_errors=True)
    # The original code comes from the SVN
    buildout_directory = buildout['buildout']['directory']
    pipeline_bin_folder = os.path.join(buildout_directory, 'src/pipeline/bin')
    # The bin folder is populated from the SVN version of the bin folder
    shutil.copytree(pipeline_bin_folder, bin_folder)
    # The bin folder of the current part should point to the global bin folder
    target = os.path.join(options['location'], 'bin')
    if os.path.exists(target):
        os.remove(target)
    # Make a symbolic link to the global bin folder in var/pipeline in the
    # part
    os.symlink(bin_folder, target)
    # Use the same shebang for all perl scripts
    for perlscript in os.listdir(bin_folder):
        if perlscript.endswith('.pl'):
            perl_file = open(os.path.join(bin_folder, perlscript), 'r')
            # Just the read the first line, which is expected to be the shebang
            shebang = perl_file.readline()
            # Make sure the shebang is as expected
            if not shebang.strip() in ['#!/soft/bin/perl', '#!/usr/bin/perl']:
                print "All perl scripts are expected to start with"
                print "#!/soft/bin/perl or #!/usr/bin/perl"
                print "This one (%s) starts with %s" % (perlscript, shebang)
                raise AttributeError
            # Read the rest of the file only, omitting the shebang
            content = perl_file.read()
            perl_file.close()
            # Open the file again, this time for writing
            perl_file = open(os.path.join(bin_folder, perlscript), 'w')
            # Write the new shebang using our own perl version as defined in
            # the buildout.cfg
            perl_file.write("#!%s\n" % buildout['settings']['perl'])
            # Write the rest of the content
            perl_file.write(content)
            perl_file.close()


def install_lib_folder(options, buildout, lib_folder):
    buildout_directory = buildout['buildout']['directory']
    # Remove the old lib folder in var/pipeline
    shutil.rmtree(lib_folder, ignore_errors=True)
    # The original lib folder is taken from the SVN
    pipeline_lib_folder = os.path.join(buildout_directory, 'src/pipeline/lib')
    # Copy the lin folder over to var/pipeline
    shutil.copytree(pipeline_lib_folder, lib_folder)
    # Make a symbolic link in the part to the lib folder in var/pipeline
    target = os.path.join(options['location'], 'lib')
    # Remove the old link
    if os.path.exists(target):
        os.remove(target)
    # And put in the new link
    os.symlink(lib_folder, target)


def install_results_folder(options, results_folder):
    # Create a results folder for the results of a pipeline run
    if os.path.exists(results_folder):
        pass
    else:
        os.mkdir(results_folder)
    target = os.path.join(options['location'], 'results')
    # Remove the old link
    if os.path.exists(target):
        os.remove(target)
    # And put in the new link
    os.symlink(results_folder, target)


def install_gemindices_folder(options, gemindices_folder):
    """
    Create a GEMIndices folder for sharing the GEM Indices
    """
    if os.path.exists(gemindices_folder):
        pass
    else:
        os.mkdir(gemindices_folder)
    target = os.path.join(options['location'], 'GEMIndices')
    # Remove the old link
    if os.path.exists(target):
        os.remove(target)
    # And put in the new link
    os.symlink(gemindices_folder, target)


def install_read_folder(options, accession):
    """
    Create a read folder with soft links to the read files
    """
    
    # Create the read folder in the parts folder
    read_folder = os.path.join(options['location'], 'readData')
    # There are only soft links in this folder, so the whole folder is deleted
    # every time.
    shutil.rmtree(read_folder, ignore_errors=True)
    # Now create the read folder
    os.mkdir(read_folder)
    number_of_reads = len(accession['file_location'].split('\n'))
    for number in range(0, number_of_reads):
        # Get the file location from the accession
        file_location = accession['file_location'].split('\n')[number].strip()
        # Try to recognize the url
        if file_location.startswith("http://"):
            # Unrecognized
            raise AttributeError
        # Only accept a path if it is inside of the path we expect.
        # This is so that tricks like ../ don't work
        if not os.path.exists(file_location):
            print "Warning! File does not exist: %s" % file_location
        # Make symbolic links to the read files
        # Take just the file name from the file location
        filename = os.path.split(file_location)[1]
        # Combine the read folder with the filename to get the target
        target = os.path.join(read_folder, filename)
        if os.path.exists(target):
            template = "Duplicated read files: \n%s"
            raise AttributeError(template % accession['file_location'])
        os.symlink(file_location, target)


def install_dependencies(buildout, bin_folder):
    """
    Install the flux, overlap and gem binaries.
    """
    
    # Remove any existing flux.sh in the pipeline bin folder
    buildout_directory = buildout['buildout']['directory']
    flux_sh = os.path.join(buildout_directory, 'var/pipeline/bin/flux.sh')
    if os.path.exists(flux_sh):
        os.remove(flux_sh)
    if os.path.exists(flux_sh):
        raise AttributeError

    # Use the Java binary as defined in the buildout.cfg
    java = os.path.join(buildout_directory, buildout['settings']['java'])
    # The flux.sh gets install inside the var/pipeline/bin folder
    pipeline_bin = os.path.join(buildout_directory, 'src/flux/bin')
    # The jar file location is defined in the buildout.cfg
    flux_jar = buildout['settings']['flux_jar']
    # This is the command used to create the flux.sh shell script
    template = '%s -DwrapperDir="%s" -jar "%s" --install'
    command = template % (java, pipeline_bin, flux_jar)
    # Now we can creat the flux.sh file.
    call(command, shell=True)
    os.symlink(os.path.join(pipeline_bin, 'flux.sh'), flux_sh)
    if not os.path.exists(flux_sh):
        raise AttributeError("Flux shell script not found", flux_sh)

    # Make symbolic links to the overlap and flux tools
    target = os.path.join(bin_folder, 'overlap')
    os.symlink(buildout['settings']['overlap'], target)
    if not os.path.exists(target):
        raise AttributeError("Overlap binary not found: %s" % target)

    # Make symbolic links to the gem binaries
    gem_binary_glob = os.path.join(buildout['settings']['gem_folder'], 'gem-*')
    for source in glob.glob(gem_binary_glob):
        gem_binary = os.path.split(source)[-1]
        target = os.path.join(bin_folder, gem_binary)
        os.symlink(source, target)
        if not os.path.exists(target):
            raise AttributeError("Gem binary not found: %s" % target)


def install_pipeline_scripts(options, buildout, accession):
    """
    Install the start, execute and clean shell scripts
    """
    
    # The default pipeline section is called "pipeline"
    pipeline = {}
    if 'pipeline' in buildout:
        pipeline = buildout['pipeline'].copy()

    # If the accession has a pipeline attribute, this overrides the defaults
    # of the pipeline section
    if 'pipeline' in options:
        if options['pipeline'] in buildout:
            pipeline.update(buildout[options['pipeline']].copy())
        else:
            # The advertised pipeline configuration is not there
            raise AttributeError

    command = "#!/bin/bash\n"
    command += "bin/start_RNAseq_pipeline.3.0.pl"
    command += " -species '%s'" % accession['species']
    command += " -genome %s" % pipeline['GENOMESEQ']
    command += " -annotation %s" % pipeline['ANNOTATION']
    command += " -project %s" % pipeline['PROJECTID']
    command += " -experiment %s" % options['experiment_id']
    command += " -template %s" % pipeline['TEMPLATE']
    # readType = 2x50
    # readType = 75D
    # Extract the read length taking the value after the x
    read_length = accession['readType']
    if 'x' in read_length:
        read_length = read_length.split('x')[1]
    if 'D' in read_length:
        read_length = read_length.split('D')[0]
    if read_length.isdigit():
        # read_length needs to be a number, otherwise don't pass it on
        command += " -readlength %s" % read_length
    command += " -cellline '%s'" % accession['cell']
    command += " -rnafrac %s" % accession['rnaExtract']
    command += " -compartment %s" % accession['localization']
    if 'replicate' in accession:
        command += " -bioreplicate %s" % accession['replicate']
    command += " -threads %s" % pipeline['THREADS']
    command += " -qualities %s" % accession['qualities']
    if 'CLUSTER' in pipeline:
        if str(pipeline['CLUSTER']).strip() == '':
            raise AttributeError("CLUSTER has not been specified")
        else:
            command += " -cluster %s" % pipeline['CLUSTER']
    command += " -database %s" % pipeline['DB']
    command += " -commondb %s" % pipeline['COMMONDB']
    if 'HOST' in pipeline:
        command += " -host %s" % pipeline['HOST']
    command += " -mapper %s" % pipeline['MAPPER']
    command += " -mismatches %s" % pipeline['MISMATCHES']
    if 'description' in options:
        command += " -run_description '%s'" % options['description']
    if 'PREPROCESS' in pipeline:
        command += " -preprocess '%s'" % pipeline['PREPROCESS']
    if 'PREPROCESS_TRIM_LENGTH' in pipeline:
        template = " -preprocess_trim_length %s"
        command += template % pipeline['PREPROCESS_TRIM_LENGTH']
    target = os.path.join(options['location'], 'start.sh')
    f = open(target, 'w')
    f.write(command)
    f.close()
    os.chmod(target, 0755)

    target = os.path.join(options['location'], 'clean.sh')
    command += " -clean"
    f = open(target, 'w')
    f.write(command)
    f.close()
    os.chmod(target, 0755)

    command = "#!/bin/bash\n"
    command += "bin/execute_RNAseq_pipeline3.0.pl all |tee -a pipeline.log"
    target = os.path.join(options['location'], 'execute.sh')
    f = open(target, 'w')
    f.write(command)
    f.close()
    os.chmod(target, 0755)


def install_read_list(options, buildout, accession):
    # Add a read.list.txt
    target = os.path.join(options['location'], 'read.list.txt')
    f = open(target, 'w')
    number_of_reads = len(accession['file_location'].split('\n'))
    for number in range(0, number_of_reads):
        file_location = accession['file_location'].split('\n')[number]
        if 'pair_id' in accession:
            pair_id = accession['pair_id'].split('\n')[number]
        else:
            pair_id = buildout['labeling']['pair_id'].strip()
            if pair_id.startswith("python:"):
                pair_id = run_python(pair_id[7:], accession)

        if 'mate_id' in accession:
            mate_id = accession['mate_id'].split('\n')[number]
        else:
            mate_id = buildout['labeling']['mate_id'].strip()
            if mate_id.startswith("python:"):
                # The mate id gets a postfix of ".1" and ".2"
                mate_id = run_python(mate_id[7:], accession).strip()
                if number_of_reads > 1:
                    if 'file_type' in accession:
                        # If file type is given (FASTQRD1, FASTQRD2), use
                        # this number
                        number = accession['file_type'].split('\n')[number][-1]
                        mate_id = "%s.%s" % (mate_id, number)
                    else:
                        # In the absence of the file type, just number in order
                        mate_id = "%s.%s" % (mate_id, number + 1)

        if 'label' in accession:
            label = accession['label'].split('\n')[number]
        else:
            label = buildout['labeling']['label'].strip()
            if label.startswith("python:"):
                label = run_python(label[7:], accession)

        file_name = os.path.split(file_location.strip())[1]
        if file_name.split('.')[-1] == "gz":
            file_name = file_name[:-3]
        labels = (file_name.strip(),
                  pair_id.strip().replace(' ', ''),
                  mate_id.strip().replace(' ', ''),
                  label.strip().replace(' ', ''))
        f.write('\t'.join(labels))
        f.write('\n')
    f.close()


def main(options, buildout):
    """
    This method is called for each part and does the following:

    * Create a fresh readData folder with pointers to the original read files

    * bin folder

        * The /src/pipeline/bin folder is copied to var/pipeline/bin

        * The shebangs of all Perl scripts in var/pipeline/bin is changed to
          use the Perl version defined in buildout.cfg

        * Create a fresh link in the part to the var/pipeline/bin folder

    * lib folder

        * The /src/pipeline/lib folder is copied to var/pipeline/lib

        * Create a fresh link in the part to the var/pipeline/lib folder
    """
    # Without an accession, the part can not be created, because no read files
    # can be linked to
    try:
        accession = buildout[options['accession']]
    except KeyError:
        print "Accession not found", options['accession']
        return

    for key, value in accession.items():
        if not key in ['pair_id',
                       'mate_id',
                       'label',
                       'file_location',
                       'file_type']:
            if '\n' in value:
                # Collapse the redundant values to make labeling easier
                accession[key] = value.split('\n')[0]

    # The part name is also the experiment id. As it is not given in the
    # options, we need to extract it from the current location. Sigh.
    options['experiment_id'] = os.path.split(options['location'])[-1]

    buildout_directory = buildout['buildout']['directory']

    bin_folder = os.path.join(buildout_directory, 'var/pipeline/bin')
    install_bin_folder(options, buildout, bin_folder)

    # The lib folder is copied to var/pipeline
    lib_folder = os.path.join(buildout_directory, 'var/pipeline/lib')
    install_lib_folder(options, buildout, lib_folder)

    experiment_id = options['experiment_id']
    results_folder = os.path.join(buildout_directory, 'var/%s' % experiment_id)
    install_results_folder(options, results_folder)

    gemindices_folder = os.path.join(buildout_directory, 'var/GEMIndices')
    install_gemindices_folder(options, gemindices_folder)

    install_read_folder(options, accession)

    install_dependencies(buildout, bin_folder)

    install_pipeline_scripts(options, buildout, accession)

    # Install the read list file defining the labels of the reads
    install_read_list(options, buildout, accession)
