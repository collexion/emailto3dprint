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
	command = "c:/python27/python.exe ../skeinforge/skeinforge_application/skeinforge_utilities/skeinforge_craft.py {0}".format(infile, outfile)
	print("$ {0}".format(command))
	output = os.popen(command).read()
	jobinfo.next_stage(outfile)