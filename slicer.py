import os
"""
This doesn't yet work, not least because I don't have slic3r installed.
However, this is the format I am assuming
"""
def slice(jobinfo):
	assert(jobinfo.status == 'slicing')
	infile = jobinfo.previous_file()
	
	basename = os.path.basename(infile)
	outfile = basename+'.gcode'
	command = "../Slic3r/slic3r-console.exe \"{0}\" --load slicerconf.ini --output {1}".format(infile, outfile)
	print("$ {0}".format(command))
	os.system(command)
	jobinfo.next_stage(outfile)