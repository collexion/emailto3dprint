import os
import config
import logger
"""
This doesn't yet work, not least because I don't have slic3r installed.
However, this is the format I am assuming
"""
slice_logger = logger.Logger('slicer')
def slice(jobinfo):
        # this will be replaced with proper error checking code later
        assert(jobinfo.status == 'slicing')
        conf = config.read_config()
        
        # read and store config information
        # this allows us to have different version of slicer stored in different places
        slice_command = conf['Slicer']['Path']
        slice_ini = conf['Slicer']['Config']
        
        # get the last file worked on (validated file)
        infile = jobinfo.previous_file()

        # CK - Modified to work on my linux VM - passes
	# Infile OK as is, must do some work for correct outfile
	# Remove original file extension and add .gcode extension
	# AW - fixed to work with file paths that contain periods
        # put together the input and output filenames
        root, ext = os.path.splitext(infile)
        outfile = root+'.gcode'

        # construct the actual command line call
	# CK - Removed quotes around infile and outfile names
        command = '{0} {1} --output {2} --load {3}'.format(slice_command, infile, outfile, slice_ini)
        
        # execute the command line call.
        # output contains anything written to stdout by the program
	# CK - Uncommented line
        output = os.popen(command).read()
        
        # this is a debugging message. remove on release
        slice_logger.log("$ "+command)
        
        # store the newly created file into the printjob
        jobinfo['slicing'] = outfile
