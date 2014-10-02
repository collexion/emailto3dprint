import mailfetch
import time
import config
"""
Each step of the module should be a function that takes a PrintJob object, and returns a new PrintJob object. See pipeline.py for more info.
"""
def main():
	# read the config file. We'll need this later.
	# also caches the file for stages
	configrc = config.read_config()
	
	# set up mailfetch. Just fetches the password for now.
	mailfetch.initialize()
	
	while True:
	
		# mailfetch.poll gets list of printjobs to work on
		for job in mailfetch.poll():
		
			"""
			pipeline goes here
			I'm not doing any concurrency on the pipeline since python doesn't support it very well, and it wouldn't give us a significant speed up anyway.
			"""
			print(job)
			
		# wait a while. This lets the computer do something else
		time.sleep(configrc['Pipeline']['poll_frequency'])