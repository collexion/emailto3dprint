import os
import config
import logger
"""
This doesn't yet work, not least because I don't have slic3r installed.
However, this is the format I am assuming
"""
slice_logger = logger.Logger('slicer')
def slice(jobinfo):
	assert(jobinfo.status == 'slicing')
	conf = config.read_config()
	
	slice_command = conf['Slicer']['Path']
	slice_ini = conf['Slicer']['Config']
	
	infile = jobinfo.previous_file()
	
	basename = os.path.basename(infile)
	root, ext = os.path.splitext(basename)
	outfile = root+'.gcode'
	command = '{0} "{1}" --output "{2}" --load {3}'.format(slice_command, infile, outfile, slice_ini)
	
	#output = os.popen(command).read()
	slice_logger.log("$ "+command)
	
	jobinfo['slicing'] = outfile