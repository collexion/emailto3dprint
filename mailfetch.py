import imaplib	  # Facilitates connection to mailserver
import email	  # Facilitates message parsing/extraction
import os	      # Used to construct attachment save path
import config
import pipeline
import getpass
import logger
# General Program Flow:
#    - Read values of configuration variables in mailfetch.conf
#    - Prompt user for the account password
#    - Make a connection to the server
#    - Pass login credentials to the server
#    - Construct a list of unread messages
#    - "Walk" through parts of each message to find attachments
#    - Extract and save found attachments
#    - Logout and close connection
#    - (Optional?) write configuration variables to mailfetch.conf

# this means you only need to log in once.
# run once at the top of the pipeline
mail_password = None
mlogger = logger.Logger('mailfetch')
def initialize():
	global mail_password
	if mail_password == None:
		mail_password = get_password()
	
# reads email, gets attachments, returns all attachments as list
def poll(verbose = True):
	global mail_password
	if mail_password == None:
		mail_password = get_password()

	mailfetch_config = config.read_config()

	servername = mailfetch_config["Mailfetch"]["server"]
	portnumber = mailfetch_config["Mailfetch"]["port"]
	username = mailfetch_config["Mailfetch"]["username"]
	mailbox = mailfetch_config["Mailfetch"]["mailbox"]
	savedir = mailfetch_config["Mailfetch"]["savedir"]

	connection = open_connection(servername,portnumber)

	login(connection,username,mail_password,mailbox)

	infolist = []
	messagelist = get_message_list(connection)
	for message in messagelist:
		email = get_message_contents(connection,message)

		# If the email is not multipart, don't process further.
		# Only multipart messages have attachments.
		if email.get_content_maintype() != 'multipart':
			continue

		# Iterate over the parts of an individual message
		for part in email.walk():
			# An attachment itself is NOT multipart
			if part.get_content_maintype() == 'multipart':
				continue

			# A condition where no attachment is to be found
			if part.get('Content-Disposition') is None:
				continue

			# If we make it this far, extract and save the attachment
			path = extract_attachment(part,savedir)
			
			# put all the information here
			sendaddr = get_sender_addr(connection,message)
			jobinfo = pipeline.PrintJob(path,sendaddr)
			infolist.append(jobinfo)

	#write_config(mailfetch_config,mailfetch_config_filename)

	# Clean up when done
	connection.close()
	connection.logout()
	return infolist

# Prompt user to enter password for the default email account
# ~AW: This will have to be automated eventually
def get_password():
    prompt = "Enter the account password:"
    pwd = getpass.getpass(prompt)
    return pwd

# Open a connection to server:port
def open_connection(server,port):
    socket = imaplib.IMAP4_SSL(server,port)
    mlogger.log("Connecting to server",server,"...")
    return socket

# Login to mailserver
#     socket - Connection opened from open_connection()
#     id - the email account username
#     pwd - the password for the account
#     mbox - name of the mailbox to check
def login(socket,id,pwd,mbox):
    socket.login(id,pwd)
    mlogger.log("Logged in as",id,"...")

    socket.select(mbox)
    mlogger.log("Selected Mailbox:",mbox)

    return 0

def get_message_list(socket):
    # Look for messages not yet marked as read, get a list of id's, and use the id's
    # to get to the message body
    typ, data = socket.search(None,"UNSEEN")
    list = data[0].split()
    mlogger.log("Returning Message List...")
    return list

def get_message_contents(socket,msg):
    typ, data = socket.fetch(msg, "(RFC822)")
    body = data[0][1]
    contents = email.message_from_bytes(body) # parsing the mail content to get a mail object
    return contents

def get_sender_addr(socket,msg):
	# There is some redundancy here, as this function initially does everytning
	# in the first 3 lines of get_message_contents(). Improve Later !!!
	typ, data = socket.fetch(msg, "(RFC822)")
	body = data[0][1]
	contents = email.message_from_bytes(body)
	sender = email.utils.parseaddr(contents['From'])
	mlogger.log(sender[1])
	return sender[1] # The sender addr
	
def extract_attachment(attachment,path):
	filename = attachment.get_filename()
	counter = 0

    # If there is no filename... create one (Think about this !!!)
    # Also, join the filename and directory path to construct final save location
	if not filename:
		filename = 'attachment-%03d%s' % (counter, '.sav')
		counter += 1
	save_path = os.path.join(path,filename)

    # Don't overwrite a preexisting file with the same name
	if not os.path.isfile(save_path):
		save_attachment(save_path,attachment)
	else:
		# should this throw an exception?
		mlogger.log(save_path,"already exists ...")
	return save_path

def save_attachment(location,attachment):
    fileptr = open(location,'wb')
    fileptr.write(attachment.get_payload(decode=True))
    mlogger.log("Saved attachment",location)
    fileptr.close()
    
    return 0

if __name__ == '__main__':
	initialize()
	poll()
