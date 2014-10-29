import os
import config
import logger
"""
This doesn't yet work, not least because I don't have slic3r installed.
However, this is the format I am assuming
"""
conv_logger = logger.Logger('converter')
def convert(jobinfo):
	assert(jobinfo.status == 'converting')
	conf = config.read_config()
	conv_command = conf['Converter']['Path']
	
	infile = jobinfo.previous_file()
	basename = os.path.basename(infile)
	root, ext = os.path.splitext(basename)
	
	outfile = None
	if ext != '.stl':
		outfile = root+'.stl'
		
		command = '{0} {1} -c stl -o {2}.stl'.format(conv_command, infile, root)
		
		#output = os.popen(command).read()
		conv_logger.log("$ "+command)
	else:
		conv_logger.log("$ Warning: {0} is already an stl file".format(infile))
	jobinfo['converting'] = outfile