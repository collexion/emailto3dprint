import os
import config
import logger
prlogger = logger.Logger('printer')
def send_job(jobinfo):
	# this should be replaced by error handling code later
	assert(jobinfo.status == 'printing')
	
	#read  config file information
	conf = config.read_config()
	print_command = conf['Printer']['Path']
	pronsole_commands = conf['Printer']['PrintCommandsPath']
	
	# determine input and output filenames
	infile = jobinfo.previous_file()
	
	# run command
	command = '{0} {1} < {2}'.format(print_command, infile, pronsole_commands)
		
	#output = os.popen(command).read()
	prlogger.log("$ "+command)