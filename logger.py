import config
import sys, os
import time


#########
# This module allows us to have fine tuned control over what gets printed and to where.
# In the future in can be extended to be helpful for the admin
#########

# get logger config info from config file
config_data = config.read_config()
default_logfile = None
if 'Logger' in config_data:
	if 'log_file' in config_data['Logger']:	
		default_logfile = config_data['Logger']['log_file']


# Each discrete functional unit should register its own logger
# Loggers can access each other through the logger.get_logger function farther down
# Loggers have their own set of options and their own logfile.
#

def get_logger(name):
	if name in Logger.LoggerIDs:
		return Logger.LoggerIDs[name]
	else:
		raise RuntimeError("attempted to modify a nonexistant logger")

def load_file(flname):
	if flname == 'stdout':
		return sys.stdout
	elif flname == 'stderr':
		return sys.stderr
	elif flname.startswith('email:'):
		import mailsend
		return mailsend.EmailFile(flname[6:])
	else:
		return open(flname, 'w')

class Logger(object):

	LoggerIDs = {}
		
	def __init__(self, name, logfile = default_logfile):	
		self.options = {
			'timestamp' : False,
			'enable' : True,
			'minimal' : False,
			'logfile' : default_logfile or 'stdout',
		}
		self.name = name
		Logger.LoggerIDs[name] = self
		
	def set_option(self, **kwargs):
		self.options.update(kwargs)
		
	def set_logfile(self, flname):
		self.options['logfile'] = flname
		
	def enable(self):
		self.options['enable'] = True
		
	def disable(self):
		self.options['enable'] = False
		
	def get_timestamp(self):
		return time.strftime('[%c]')
		
	def error(self, info, what):
		import mailsend
		text = mailsend.error_message(what)
		addr = 'email:' + info.sender
		self.log_to(addr, text)
		
	def log_to(self, flname, *text):
		tmp = self.options['logfile']
		self.set_logfile(flname)
		self.log(*text)
		self.set_logfile(tmp)
		
	def log(self, *text):
		text = ' '.join(str(x) for x in text)
		if self.options['enable']:
			if self.options['timestamp']:
				timestamp = self.get_timestamp()
			else:
				timestamp = ''
			output_line = timestamp + str(text) + os.linesep
			logfile = load_file(self.options['logfile'])
			logfile.write(output_line)
		