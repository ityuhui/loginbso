#! /usr/bin/env python

import urllib, urllib2, httplib 
import sys,getopt

# input the visit host
#host_name = "9.111.251.46"
host_name = "qataix06.eng.platformlab.ibm.com"

#hosts = ["9.111.251.46","qataix06.eng.platformlab.ibm.com","ibm01.eng.platformlab.ibm.com"]

#user_name = ""
#user_password = ""

def readnextline(f):
	line=f.readline();
	return line.rstrip()

	
def version():
	print "Version 1.2"
	
opts, args = getopt.getopt(sys.argv[1:], "v",["version"])

for opt, val in opts:
	if opt in ( '-v', '--version' ):
		version()
		sys.exit()
		
f=open('data.txt','r')
f.seek(0)
hoststr=readnextline(f)
hosts=hoststr.split(',')
user_name=readnextline(f)
user_password=readnextline(f)
print hosts
print user_name
print user_password

def openerDirector(_url, _params):
	request = urllib2.Request(_url)
	if _params != None:
		request = urllib2.Request(_url, urllib.urlencode(_params))
	return urllib2.build_opener().open(request)

for host_name in hosts:
	try:
		# get the session id - sid
		f_open = openerDirector("https://" + host_name, None)
		args = f_open.url.split('?')
		
		base_url = args[0][0:args[0].rfind('/')]
		sid = args[1][args[1].index('=')+ 1:]

		# to go to login
		blogin_params = {'sid':sid, 'login':'Log In Now'}
		blogin_url = base_url + '/connstatus.html'
		blogin_open = openerDirector(blogin_url, blogin_params)
		# print blogin_open.url

		# to login 
		login_url = base_url + "/loginuser.html"
		login_params = {'username':user_name, 'password':user_password, 'Login':'Continue','sid':sid}

		login_open = openerDirector(login_url, login_params)
		print login_open.read()
	except Exception,inst:
		print "The host - " + host_name + " has been released!"

# print a blank line
print 
# wait for user to check the result
raw_input("Press any key to exit ...")
