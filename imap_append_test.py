#!/usr/bin/env python

import argparse
import os
import sys
import imaplib
import smtplib
import mimetypes
import time
import base64

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if __name__ == "__main__":
	'''
	Parse command line arguments
	'''
	parser = argparse.ArgumentParser(description='Uploads messages with IMAP APPEND')
	parser.add_argument('-u', dest='USER', required=True, help='username for logging in')
	parser.add_argument('-p', dest='PASS', required=True, help='the password')
	parser.add_argument('-s', dest='SERVER', required=False, default='imap.rambler.ru', help='the server, e.g. imap.rambler.ru')
	parser.add_argument('-f', dest='FOLDER', required=False, default='SentBox', help='the folder, e.g. SentBox')

	args = parser.parse_args()
	if not args.USER or not args.PASS:
		parser.print_help()
		sys.exit(1)

	timestr = imaplib.Time2Internaldate(time.time())

	outer = MIMEMultipart()
	outer['Subject'] = 'Test message {0}'.format(timestr)
	outer['To'] = args.USER
	outer['From'] = args.USER
	outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

	try:
		srcfile = open('image1.jpg', 'r')
	except IOError as x:
		print x
		exit(1)
	with srcfile:
		msg = MIMEImage(srcfile.read(), _subtype='jpg')

	msg.add_header('Content-Disposition', 'attachment', filename='image1.jpg')
	outer.attach(msg)

	print "Connecting to {0}...".format(args.SERVER)
	M = imaplib.IMAP4_SSL(args.SERVER, 993)
	print "Connected"

	print "Logging in..."
	M.login(args.USER, args.PASS)
	print "Logged in"

	print M

	msg = str(outer)

	print msg[:2048]

	print "Uploading {0} bytes, started at {1}...".format(len(msg), timestr)
	M.append(args.FOLDER, "\Seen", timestr, msg)

	timeend = imaplib.Time2Internaldate(time.time())
	print "Upload done {0}".format(timeend)

	M.logout()

