import os
import config
import logger
vlogger = logger.Logger('validator')
def validate(jobinfo):
	# this should be replaced by error handling code later
	assert(jobinfo.status == 'validating')
	
	#we are using slic3r alone for validation right now.
	# so don't do anything
	vlogger.log("$ validating...")