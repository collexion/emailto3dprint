import os
import config
import logger
prlogger = logger.Logger('printer')
def send_job(jobinfo):
	# this should be replaced by error handling code later
	assert(jobinfo.status == 'printing')
	
	#read  config file information
	conf = config.read_config()
	encode_command = conf['Printer']['Encoder']
	machine = conf['Printer']['Encoder']
	
	# determine input and output filenames
	infile = jobinfo.previous_file()
	root, ext = os.path.splitext(infile)
	
	outfile = '/dev/ttyUsb0'
	
	# convert to .x3g
	command = '{0} -s -m {3} {1} {2}'.format(encode_command, infile, outfile, machine)
	# run command
		
	#output = os.popen(command).read()
	prlogger.log("$ "+command)
