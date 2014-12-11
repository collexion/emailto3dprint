import os
import config
import logger
conv_logger = logger.Logger('converter')
def convert(jobinfo):
	# this should be replaced by error handling code later
	assert(jobinfo.status == 'converting')
	
	#read  config file information
	conf = config.read_config()
	conv_command = conf['Converter']['Path']
	
	# determine input and output filenames
	infile = jobinfo.previous_file()
	root, ext = os.path.splitext(infile)
	if ext not in conf['Mailfetch']['extensions']:
		conv_logger.error(jobinfo, 'File is in an unsupported format {0}'.format(ext))
	
	outfile = None
	# don't bother converting if you already have an stl
	if ext != '.stl':
		outfile = root+'.stl'
		
		# run command
		command = '{0} {1} -c stl -o {2}.stl'.format(conv_command, infile, root)
		
		#output = os.popen(command).read()
		conv_logger.log("$ "+command)
	else:
		conv_logger.log("$ Converter: {0} is already an stl file".format(infile))
		
	# if you did not convert, this is set to None
	# this will simply tell the pipeline that no file was created in this stage
	jobinfo['converting'] = outfile