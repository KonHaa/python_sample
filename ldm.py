#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this little piece of code is written to be executed by
# as a cronjob or by incron.
# with this combination you can monitor a logfile
# and send an email that contains the new log entries.


# start it with 2 args:
# first arg is the logfile you want to monitor
# second arg is the recipient who should recieve an email
# that contains the new log entries

# if the linecount between 2 runtimes differs it will
# mail the new lines to the recipient.


#------------------#
# imports          #
#------------------#

from sys import argv
from email.mime.text import MIMEText
import smtplib
import sys
import linecache

script, logfile, recipient = argv

#-----------------#
# data settings   #
#-----------------#

#the storagefile holds the linecount of the last run
storagefile = 'storage.txt'
#path to the textfile that contains the email password
path_to_passwdfile = 'pass.txt'

#-----------------#
# mail settings   #
#-----------------#

#sender's mail adress
sender = ''
#sender's smtp-server 
smtpserver = ''
#sender's username for the mail-account
smtpusername = ''
#the emails subject
subject = 'new entries in in your observed logfile'
#use tls?
usetls = True

#---------------------------------------#
# function to read the stored linecount #
#---------------------------------------#

def get_old_linecount():
	target = open(storagefile, 'r')	
	return int(target.read())
	target.close()

old_linecount = get_old_linecount()

#---------------------------------------#
# function to get the current linecount #
#---------------------------------------#

def get_new_linecount():
	target = open(logfile, 'r')
	return int(len(target.readlines()))
	target.close()
new_linecount = get_new_linecount()

#---------------------------------------#
# function to read the new lines        #
#---------------------------------------#

def read_new_lines(logfile,firstline,lastline):

	current_line = int(old_linecount) + 1
	new_lines = ''

	while current_line <= new_linecount:
		if new_lines == '':
			new_lines = linecache.getline(logfile, current_line)
		else:
			new_lines = new_lines + linecache.getline(logfile, current_line)
		current_line += 1
	return new_lines
	target.close()

#-------------------------------#
# function to get the password	#
#-------------------------------#

def get_passwd():
	passfile = open(path_to_passwdfile, 'r')
	return str(passfile.read())

smtppassword = get_passwd()

#------------------------------------#
# function to save the new linecount #
#------------------------------------#

def save_linecount(new_linecount):
	target = open(storagefile, 'w')
	target.seek(0)
	target.write(str(new_linecount))
	target.close()

#---------------------------#
# function to send a mail	#
#---------------------------#

def sendmail(recipient,subject,content):
  	# generate a RFC 2822 message
	msg = MIMEText(content)
 	msg['From'] = sender
	msg['To'] = recipient
	msg['Subject'] = subject

	# open SMTP connection
	server = smtplib.SMTP(smtpserver)

	# start TLS encryption
 	if usetls:
 	   server.starttls()

  	# login with specified account
 	if smtpusername and smtppassword:
		server.login(smtpusername,smtppassword)

	# send generated message
		server.sendmail(sender,recipient,msg.as_string())

	# close SMTP connection
	server.quit()

#------------------------#
# main function          #
#------------------------#
# get the content of the new lines, call sendmail() 
# and generate mail with subject and content
def main():

	if new_linecount != old_linecount:
		new_lines = str(read_new_lines(logfile,old_linecount,new_linecount))

		sendmail(recipient,subject,new_lines)

		save_linecount(new_linecount)


	sys.exit(0)

#if __name__ == '__main__':
main()