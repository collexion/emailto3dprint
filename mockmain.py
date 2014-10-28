import mailfetch
import time
import config
import logger
import pipeline
import slicer
"""
This is a fake main function used to test slicer by itself, without having to use mailfetch each time.
"""
def main():
	job = pipeline.PrintJob("../skeinforge/test.stl", "user@email.com")
	job.status = 'slicing'
	njob = slicer.slice(job)
	
		
if __name__ == '__main__':
	main()
