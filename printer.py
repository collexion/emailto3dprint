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
	
	# determine input and output filenames
	infile = jobinfo.previous_file()
	root, ext = os.path.splitext(infile)
	encoded_file = '/dev/tty/usb0/' + os.path.basename(root) + ".x3g"
	
	# convert to .x3g
	encode_command = '{0} {1} {2}'.format(encode_command, 
	# run command
	command = '{0} {1} < {2}'.format(print_command, infile, pronsole_commands)
		
	#output = os.popen(command).read()
	prlogger.log("$ "+command)