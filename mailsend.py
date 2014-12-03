#
# mailsend.py
# 
# The purpose of this module is to send notifications to
# users and admins, informing of a successful print job,
# or, alternately, informing them of the point of failure
#
#

import smtplib # Facilitates sending email
import config  # Module for importing configuration variable values
import getpass # Module to ask for email account password

mail_password = None
#mlogger = logger.Logger('mailsend')

def send(receiver,stage):
    global mail_password
    if mail_password == None:
        mail_password = get_password()

    mailsend_config = config.read_config()

    servername = mailsend_config["Mailsend"]["server"]
    portnumber = mailsend_config["Mailsend"]["port"]
    sender = mailsend_config["Mailsend"]["sender"]

    subject = "emailto3dprint job status"
    body = ""


    # Form subject line and message body based on print job result
    if (stage == "convert"):
        body = "This is an automated message to inform you that your recent print job has failed.\nReason: Unable to convert model from .obj to .stl"
    elif (stage == "validate"):
        body = "This is an automated message to inform you that your recent print job has failed.\nReason: Model failed validation"
    elif (stage == "slice"):
        body = "This is an automated message to inform you that your recent print job has failed.\nReason: Slicing failure"
    elif (stage == "print"):
        body = "This is an automated message to inform you that your recent print job has failed.\nReason: Printer failure"
    elif (stage == "success"):
        body = "This is an automated message to inform you that your recent print job was successful."
    else:
        print("Invalid stage... Exiting.")
        return -1

    # Open a socket to SMTP server and login
    socket = smtplib.SMTP(servername,portnumber)
    socket.starttls()
    socket.login(sender,mail_password)

    # Concatenate carriage return, newline, header fields, and body
    message = '\r\n'.join(['To: %s' % receiver,
                    'From: %s' % sender,
                    'Subject: %s' % subject,
                    '', body])

    # Try to send the message
    try:
        socket.sendmail(sender, [receiver], message)
        print ("==> Email sent to",receiver)
    except:
        print ("Error sending email to",receiver)

    socket.quit()

# Prompt user to enter password for the default email account
def get_password():
    prompt = "Enter the account password:"
    pwd = getpass.getpass(prompt)
    return pwd