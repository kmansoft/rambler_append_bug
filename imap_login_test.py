#!/usr/bin/env python

import argparse
import os
import sys
import imaplib
import smtplib
import mimetypes
import time
import base64

if __name__ == "__main__":
	'''
	Parse command line arguments
	'''
	parser = argparse.ArgumentParser(description='Logs into an IMAP account, waits, logs out, and exits')
	parser.add_argument('-u', dest='USER', required=True, help='username for logging in')
	parser.add_argument('-p', dest='PASS', required=True, help='the password')
	parser.add_argument('-s', dest='SERVER', required=False, default='imap.gmail.com', help='the server, e.g. imap.gmail.com')
	parser.add_argument('-l', dest='SLEEP', type=int, required=False, default='60', help='how long to wait before logging out')

	args = parser.parse_args()
	if not args.USER or not args.PASS:
		parser.print_help()
		sys.exit(1)

	print "Connecting to {0}...".format(args.SERVER)
	M = imaplib.IMAP4_SSL(args.SERVER, 993)
	print "Connected"

	print "Logging in..."
	M.login(args.USER, args.PASS)
	print "Logged in"

	print "Sleeping {0} seconds...".format(args.SLEEP)
	time.sleep (args.SLEEP)

	print "Logging out..."
	M.logout()

