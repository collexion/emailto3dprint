import mailfetch
import time
import config
import logger
import pipeline

import slicer
import converter
#import validator
#import printer
"""
Each step of the module should be a function that takes a PrintJob object, and returns a new PrintJob object. See pipeline.py for more info.
"""
def main():
	# read the config file. We'll need this later.
	# also caches the file for stages
	configrc = config.read_config()
	
	# set up mailfetch. Just fetches the password for now.
	# v option is temporary, and prevents pipeline from flooding console
	# should eventually be replaced by proper logging system
	plogger = logger.Logger('pipeline')
	
	job = pipeline.PrintJob("../Cube_Base.stl", "username@email.com")

	job.status = 'converting'
	converter.convert(job)
	
	#job.status = 'validating'
	#validator.validate(job)
	
	job.status = 'slicing'	
	job = slicer.slice(job)
	
	#printer.send_job(job)
		
if __name__ == '__main__':
	main()
