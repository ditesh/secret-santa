#!/usr/bin/env python

import os
import sys
import time
import shutil
import smtplib
import os.path
import random

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import utils

from optparse import OptionParser

def main(argv=None): 

        parser = OptionParser()
        parser.add_option("-H", "--host", dest="host", default="", help="Email server hostname")
        parser.add_option("-P", "--port", dest="port", default=25, help="Email server port")
        parser.add_option("-u", "--username", dest="username", default="", help="Email server username")
        parser.add_option("-p", "--password", dest="password", default="", help="Email server password")
        parser.add_option("-f", "--from", dest="fromEmail", default="", help="From email address")
        parser.add_option("-e", "--emails", dest="emails", default="", help="File containing list of valid email addresses (one per line in the format \"Name\" <email@example.com>)")
        parser.add_option("-a", "--attachment", dest="attachment", default="", help="File attachment. If the file is text, it will be inlined into the email address")
        parser.add_option("-d", "--debug", dest="debug", action="store_true", help="Enable SMTP debugging")

        (options, args) = parser.parse_args()
        emailPath = options.emails
        attachmentPath = options.attachment
        username = options.username
        password = options.password
        host = options.host
        port = options.port
        fromEmail = options.fromEmail
        debug = options.debug

        if len(emailPath) == 0 or not os.path.exists(emailPath):
                print >> sys.stderr, "No such email file exists: " + emailPath
                return(1)

        if len(attachmentPath) == 0 or not os.path.exists(attachmentPath):
                print >> sys.stderr, "No such attachment file exists: " + attachmentPath
                return(1)

        if len(host) == 0:
                print >> sys.stderr, "No email server defined"
                return(1)

        if len(username) == 0:
                print >> sys.stderr, "No email username defined"
                return(1)

        if len(password) == 0:
                print >> sys.stderr, "No email password defined"
                return(1)

	attachment = open(attachmentPath, "r").read()
	emails = open(emailPath, "r").readlines()

	if len(emails) <= 2:
                print >> sys.stderr, "The email file needs to contain more then two email addresses"
                return(1)

	random.shuffle(emails)
	sanitizedEmails = []

	for email in emails:

		email = email.strip()

		if len(email) == 0:
			continue

		sanitizedEmails.append(email)

	if len(sanitizedEmails) <= 2:
                print >> sys.stderr, "The email file needs to contain more then two valid email addresses "
                return(1)

	i = 1
	data = {}
	length = len(sanitizedEmails)

	while i < length -1:

		data[sanitizedEmails[i]] = sanitizedEmails[i+1]
		i += 1

	data[sanitizedEmails[0]] = sanitizedEmails[1]
	data[sanitizedEmails[length-1]] = sanitizedEmails[0]

	s = 0
	f = 0
	mailServer = smtplib.SMTP()

	if debug:
		mailServer.set_debuglevel(100)

	for santa, receipient in data.iteritems():

		msg = MIMEMultipart()
		msg['Subject'] = "Secret Santa!"
		msg['From'] = fromEmail
		msg['To'] = santa
		msg.preamble = 'Secret Santa'

		msgAlternative = MIMEMultipart('alternative')
		msg.attach(msgAlternative)

		text = attachment.replace("${santa}", utils.parseaddr(santa)[0]);
		text = text.replace("${receipient}", utils.parseaddr(receipient)[0]);
		text = MIMEText(text, 'html')
		msgAlternative.attach(text)

		try:
			mailServer.connect(host, port)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(username, password)
			mailServer.sendmail(username, [santa], msg.as_string())
			mailServer.close()
			s += 1

		except Exception, e:
			mailServer.close()
			print >> sys.stderr, "Error when sending email to " + santa + " because of: ", str(e)
			f += 1

	print "Automated Secret Santa has ended"
	print s, "successes"
	print f, "failures"
	return(0)

if __name__ == "__main__":
	sys.exit(main())
