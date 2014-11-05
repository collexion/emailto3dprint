import mailfetch
import time, sys
import config
import logger
import pipeline

import slicer
import converter
import validator
import printer
"""
Each step of the module should be a function that takes a PrintJob object, and returns a new PrintJob object. See pipeline.py for more info.
"""
def main():
	# read the config file. We'll need this later.
	# also caches the file for stages
	configrc = config.read_config()
	
	#load the logger
	plogger = logger.Logger('pipeline')
	
	if len(sys.argv) == 1:
		plogger.log("Error: no model given to pipeline")
		return
	infile = sys.argv[1]
	
	job = pipeline.PrintJob(infile, "username@email.com")

	job.status = 'converting'
	converter.convert(job)
	
	#replaced by slic3r automatic validation
	#job.status = 'validating'
	#validator.validate(job)
	
	job.status = 'slicing'	
	slicer.slice(job)
	
	job.status = 'printing'
	printer.send_job(job)
		
if __name__ == '__main__':
	main()
