from datetime import datetime, date, time
"""
This object represents the state of a single print job at one point in the pipeline. Each step should recieve one as an argument, and create a new one.
"""
class PrintJob(object):
	ID = 1000
	def __init__(self, attachment_path, users_email = None):
		self.jobid = PrintJob.ID + 1
		PrintJob.ID += 1
		
		self.stages = {
			'pending' : 0,
			'converting' : 1,
			'validating' : 2,
			'slicing' : 3,
			'printing' : 4
		}
		
		# remember who sent the job.
		# this is useful so we can send error messages
		# as well as keeping track of who uses the printer
		self.sender = users_email
		
		# record the location of the file we are working with.
		# each stage should keep its file stored here, so we can backtrack if neccesary.
		# no file will exist if the stage has not completed
		self.files = [attachment_path, None, None, None, None]
		
		# remember approximately when the job was sent
		self.time_sent = datetime.utcnow()
		
		# what stage of the pipeline this job is in
		# update status everytime we pass it to a new step
		# this will help keep track of errors
		self.status = "pending"
		
	
	def __setitem__(self, key, value):
		# store a file for the given stage.
		n = self.stages[key]
		self.files[n] = value
		
	def __getitem__(self, key):
		# retrieve the given file for the given stage
		n = self.stages[key]
		return self.files[n]
		
	def previous_file(self):
		# gets the last file that was stored in the job
		n = self.stages[self.status]
		value = self.files[n]
		while n > 0 and value == None:
			n -= 1
			value = self.files[n]
		assert(value != None)
		return value
			
	def next(self, key):
		# gets the stage that comes after this one.
		n = self.stages[key]
		n += 1
		for key, value in self.stages.items():
			if n == value:
				return key
		raise IndexError("No stage after {0}".format(key))
		
	def prev(self, key):
		# gets the stage that comes before this one
		n = self.stages[key]
		n -= 1
		for key, value in self.stages.items():
			if n == value:
				return key
		raise IndexError("No stage before {0}".format(key))
		
	def __str__(self):
		return 'PrintJob<#{0} {1} [{2}]>'.format(self.jobid, self.sender, self.status)