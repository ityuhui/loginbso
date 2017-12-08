#! /usr/bin/env python
import time
import requests
import sys,getopt

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
class AESCrypto():
    def __init__(self,key):
        if len(key)%16!=0:
            key=key+str((16-len(key)%16)*'0')
        self.key = key
        self.mode = AES.MODE_CBC
        #print(AES.block_size)

    def encrypt(self,text):
        if len(text)%16!=0:
            text=text+str((16-len(text)%16)*'0')
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode("utf-8").rstrip('0')

def readnextline(f):
    line=f.readline()
    return line.rstrip()

def version():
    print("Version 20171208")

opts, args = getopt.getopt(sys.argv[1:], "v",["version"])

for opt, val in opts:
    if opt in ( '-v', '--version' ):
        version()
        sys.exit()
		
f=open('hostlist.txt','r')
f.seek(0)
hoststr=readnextline(f)
hosts=hoststr.split(',')

f=open('config.txt','r')
f.seek(0)
pre_user_name=readnextline(f)
pre_user_password=readnextline(f)

pwdstr = input("Enter your password for decyption: ")

pc = AESCrypto(pwdstr)
try:
    user_name = pc.decrypt(pre_user_name)
    user_password = pc.decrypt(pre_user_password)
except :
    print("The password is wrong")
    sys.exit(1)

print(hosts)
print(user_name)
#print(user_password)

for host_name in hosts:
    try:
        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        r = s.get("http://" + host_name, verify=False)
        #print(r.url)
        #print(r.text)
        args = r.url.split('?')
        base_url = args[0][0:args[0].rfind('/')]
        sid = args[1][args[1].index('=') + 1:]

        login_params1 = {'sid':sid, 'login':'Log In Now'}
        login_params2 = {'username':user_name, 'password':user_password, 'login':'Continue','sid':sid}

        time.sleep(1)
        r = s.post(base_url + "/connstatus.html", data=login_params1, verify=False)
        print(r.url)
        print(r.status_code)
        print(r.history)
        #print(r.text)

        time.sleep(1)
        r = s.post(base_url + "/loginuser.html", data=login_params2, verify=False)
        print(r.url)
        print(r.status_code)
        print(r.history)
        #print(r.text)
	
    #except IOError as ere:
    #    print("Error happended")
        #print(e)
    except Exception as e:
        print(e)

# print a blank line
print 
# wait for user to check the result

