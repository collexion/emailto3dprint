pages = [
	'index',
	'projectspec',
	'teammembers',
	'ekstatus',
	'ckstatus',
	'awstatus',
	'schedule',
	'documentation'
]
import os, sys
import markdown2
def contentfile(name):
	return 'content/'+name+'.txt'
def htmlfile(name):
	if name != 'index':
		return 'html/'+name+'.html'
	else:
		return name+'.html'
def init_content():
	for page in pages:
		flname = contentfile(page)
		open(flname, 'a').close()
def main():
	db = {}
	for page in pages:
		flname = contentfile(page)
		with open(flname, 'r') as fl:
			contents = fl.read()
			format = 'html'
			
			# check if the file should be read as another format
			lines = contents.split('\n')
			if len(lines) > 0:
				firstline = lines[0]
				if firstline.startswith('#format '):
					format = firstline[8:]
					if '\n' in contents:
						endofline = contents.index('\n')
						if len(contents) > endofline:
							contents = contents[endofline:]
						else:
							raise RuntimeError("No message given for content file \"{0}\". Newline is requred after format specification.".format(flname))
					else:
						raise RuntimeError("No message given for content file \"{0}\". Newline is requred after format specification.".format(flname))
			if format == 'markdown':
				contents = markdown2.markdown(contents)
			#add other formats here
			
			db[page] = contents
	with open('template.html', 'r') as template:
		template_html = template.read()
		for (key, value) in db.items():
			html = template_html.replace('$CONTENT$', value)
			with open(htmlfile(key), 'w') as fl:
				fl.write(html)
		
		
		
if __name__ == '__main__':
	if len(sys.argv) > 1:
		arg = sys.argv[1]
		if arg == 'init':
			init_content()
		elif arg == 'main':
			main()
	else:
		main()