from datetime import datetime, date, time
"""
This object represents the state of a single print job at one point in the pipeline. Each step should recieve one as an argument, and create a new one.
"""
class PrintJob(object):
	Stages = ['pending', 'slicing', 'printing']
	ID = 1000
	@classmethod
	def NextStage(klass, current):
		i = klass.Stages.index(current)
		if i >= len(klass.Stages):
			return None
		else:
			return klass.Stages[i+1]
	@classmethod
	def PrevStage(klass, current):
		i = klass.Stages.index(current)
		if i <= 0:
			return None
		else:
			return klass.Stages[i-1]
		
	def __init__(self, attachment_path, users_email = None):
		self.jobid = PrintJob.ID + 1
		PrintJob.ID += 1
		# remember who sent the job.
		# this is useful so we can send error messages
		# as well as keeping track of who uses the printer
		self.sender = users_email
		
		# record the location of the file we are working with.
		# each stage should keep its file stored here, so we can backtrack if neccesary.
		# no file will exist if the stage has not completed
		self.files = {'pending' : attachment_path}
		
		# remember approximately when the job was sent
		self.time_sent = datetime.utcnow()
		
		# what stage of the pipeline this job is in
		# update status everytime we pass it to a new step
		# this will help keep track of errors
		self.status = "pending"
	
	# return the file created in the last stage
	def previous_file(self):
		last = PrintJob.PrevStage(self.status)
		return self.files[last]
	
	# finish the current stage
	def next_stage(self, info):
		self.files[self.status] = info
		self.status = PrintJob.NextStage(self.status)
		
	def __str__(self):
		return 'PrintJob<#{0} {1} [{1}]>'.format(self.jobid, self.sender, self.status)