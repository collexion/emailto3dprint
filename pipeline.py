from datetime import datetime, date, time
"""
This object represents the state of a single print job at one point in the pipeline. Each step should recieve one as an argument, and create a new one.
"""
class PrintJob(object):
	ID = 1000
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
		self.files = StatusList()
		self.files['pending'] = attachment_path
		
		# remember approximately when the job was sent
		self.time_sent = datetime.utcnow()
		
		# what stage of the pipeline this job is in
		# update status everytime we pass it to a new step
		# this will help keep track of errors
		self.status = "pending"
	
	def advance(self):
		self.status = self.next_stage()
	
	# return the file created in the last stage
	def previous_file(self):
		return self.files.prev(self.status)
	
	# finish the current stage
	def next_stage(self):
		return self.files.next(self.status)
		
	def __str__(self):
		return 'PrintJob<#{0} {1} [{2}]>'.format(self.jobid, self.sender, self.status)
		
class StatusList(object):
	"""
	Handles keeping track of the order of stages, and the files associated with them.
	"""
	def __init__(self):
		self.stages = {
			'pending' : 0,
			'converting' : 1,
			'validating' : 2,
			'slicing' : 3,
			'printing': 4
		}
		self.contents = [None for x in self.stages]
	def __setitem__(self, key, value):
		index = self.getkey(key)
		self.contents[index] = value

	def __getitem__(self, key):
		'gets the file associated with an index or status name'
		index = self.getkey(key)
		value = self.contents[index]
		# This lets you implictly keep the same file as the last stage
		# if a stage does not have a file, gets the file from the previous stage
		while value == None and index >= 0:
			value = self.contents[index]
			index -= 1
		return value
	def getkey(self, key):	
		if isinstance(key, str):
			index = self.stages[key]
		else:
			index = key
		return index
	
	def next(self, start):
		index = self.getkey(start)
		nxt = index + 1
		if index >= len(self.stages):
			raise IndexError('There is no stage after stage {0}'.format(start))
		else:
			return self[nxt]
	def prev(self, start):
		index = self.getkey(start)
		prv = index - 1
		if index < 0:
			raise IndexError('There is no stage before stage {0}'.format(start))
		else:
			pfl = self[prv]
			return pfl
	def __str__(self):
		out = 'Stages('
		parts = []
		for stage in self.stages.keys():
			index = self.getkey(stage)
			flpath = self.contents[index]
			parts.append("{0}: \"{1}\"".format(stage, flpath))
		out += ', '.join(parts)
		out +=  ")"
		return out