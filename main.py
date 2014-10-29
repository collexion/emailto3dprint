import mailfetch
import time
import config
import logger

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
	mailfetch.initialize()
	
	while True:
	
		# mailfetch.poll gets list of printjobs to work on
		for job in mailfetch.poll():
			"""
			pipeline goes here
			I'm not doing any concurrency on the pipeline since python doesn't support it very well, and it wouldn't give us a significant speed up anyway.
			"""
			job.status = 'converting'
			converter.convert(job)
			
			#job.status = 'validating'
			#validator.validate(job)
			
			job.status = 'slicing'
			job = slicer.slice(job)
			
			#job.status = 'printing'
			#printer.send_job(job)
			
		# wait a while. This lets the computer do something else
		delay_time = float(configrc['Pipeline']['poll_frequency'])
		time.sleep(delay_time)
		
if __name__ == '__main__':
	main()
