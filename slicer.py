import os
"""
This doesn't yet work, not least because I don't have slic3r installed.
However, this is the format I am assuming
"""
def slice(jobinfo):
	infile = jobinfo.previous_file()
	basename = os.path.basename(filename)
	outfile = basename+'.gcode'
	command = "slic3r {0} --output {1}".format(infile, outfile)
	os.system(command)
	jobinfo.next_stage(outfile)