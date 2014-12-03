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
import logger     # Module to log useful messages

mail_password = None
mlogger = logger.Logger('mailsend')

def send(receiver,stage):
    global mail_password
    if mail_password == None:
        mail_password = get_password()

    try:
        mailsend_config = config.read_config()
        servername = mailsend_config["Mailsend"]["server"]
        portnumber = mailsend_config["Mailsend"]["port"]
        sender = mailsend_config["Mailsend"]["sender"]
    except:
        mlogger.log("Mailsend configuration error")
        print("Exiting.")
        return -1

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
    else: # This should never happen
        mlogger.log("Invalid Mailsend Stage:",stage)
        return -1

    # Open a socket to SMTP server
    try:
        socket = smtplib.SMTP(servername,portnumber)
    except:
        mlogger.log("Mailsend failed to open connection to",servername,":",portnumber)
        return -2

    # Login to the sending account
    try:
        socket.starttls()
        socket.login(sender,mail_password)
    except:
        mlogger.log("Mailsend failed to login to",servername,":",portnumber)
        return -3

    # Now that we have made it this far, we can form the message to send.
    # Concatenate carriage return, newline, header fields, and body
    message = '\r\n'.join(['To: %s' % receiver,
                    'From: %s' % sender,
                    'Subject: %s' % subject,
                    '', body])

    # Try to send the message
    try:
        socket.sendmail(sender, [receiver], message)
        mlogger.log("Email sent to",receiver)
    except:
        mlogger.log("Error sending email to",receiver)

    socket.quit()

# Prompt user to enter password for the default email account
# There is some redundancy here, as Mailfetch has the same helper function.
def get_password():
    prompt = "Enter the account password:"
    pwd = getpass.getpass(prompt)
    return pwd