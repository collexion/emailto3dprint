import imaplib        # Facilitates connection to mailserver
import email          # Facilitates message parsing/extraction
import os             # Used to construct attachment save path
import configparser   # Used to read/write configuration values from/to file

mailfetch_config_filename = "mailfetch.conf"

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
def main():
    mailfetch_config = read_config()

    servername = mailfetch_config["Mailfetch"]["server"]
    portnumber = mailfetch_config["Mailfetch"]["port"]
    username = mailfetch_config["Mailfetch"]["username"]
    mailbox = mailfetch_config["Mailfetch"]["mailbox"]
    savedir = mailfetch_config["Mailfetch"]["savedir"]

    password = get_password(username)

    connection = open_connection(servername,portnumber)

    login(connection,username,password,mailbox)

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

            # If we make it this far, there is an attachment to be extracted and saved
            extract_attachment(part,savedir)

    #write_config(mailfetch_config,mailfetch_config_filename)

    # Clean up when done
    connection.close()
    connection.logout()
    return 0

# Prompt user to enter password for the default email account
def get_password(user):
    prompt = "Enter the password for " + user + ": "
    pwd = input(prompt)
    return pwd

# Uses the configparser module to read configuration variable values from mailfetch.conf
def read_config():
    config = configparser.ConfigParser()
    config.read(mailfetch_config_filename)
    config.sections()
    print("Configuration data read from",mailfetch_config_filename,"...")
    return config

# Helper function to display config values.
# This function will disappear in the future.
def print_config(config):
    for key in config["Mailfetch"]:
        print(key,config["Mailfetch"][key])
    return 0

# Write current configuration values back to mailfetch.conf
# May or may not be used in the future.
def write_config(config,filename):
    with open(filename,"w") as confFile:
        config.write(confFile)
    print("Configuration data written to",mailfetch_config_filename,"...")
    return 0

# Open a connection to server:port
def open_connection(server,port):
    socket = imaplib.IMAP4_SSL(server,port)
    print("Connecting to server",server,"...")
    return socket

# Login to mailserver
#     socket - Connection opened from open_connection()
#     id - the email account username
#     pwd - the password for the account
#     mbox - name of the mailbox to check
def login(socket,id,pwd,mbox):
    socket.login(id,pwd)
    print("Logged in as",id,"...")

    socket.select(mbox)
    print("Selected Mailbox:",mbox)

    return 0

def get_message_list(socket):
    # Look for messages not yet marked as read, get a list of id's, and use the id's
    # to get to the message body
    typ, data = socket.search(None,"UNSEEN")
    list = data[0].split()
    print("Returning Message List...")
    return list

def get_message_contents(socket,msg):
    typ, data = socket.fetch(msg, "(RFC822)")
    body = data[0][1]
    contents = email.message_from_bytes(body) # parsing the mail content to get a mail object

    return contents

def extract_attachment(attachment,path):
    filename = attachment.get_filename()
    ctr = 0

    # If there is no filename... create one (Think about this !!!)
    # Also, join the filename and directory path to construct final save location
    if not filename:
        filename = 'attachment-%03d%s' % (counter, '.sav')
        ctr = ctr + 1
    save_path = os.path.join(path,filename)

    # Don't overwrite a preexisting file with the same name
    if not os.path.isfile(save_path):
        save_attachment(save_path,attachment)
    else:
        print(save_path,"already exists ...")
    return 0

def save_attachment(location,attachment):
    fileptr = open(location,'wb')
    fileptr.write(attachment.get_payload(decode=True))
    print("Saved attachment",location)
    fileptr.close()
    
    return 0

main()
