#/bin/python

#Account Editing Script

#Version 1.1

#Author Eldo Roshi


import sys

import subprocess

import vhost_manager

import os

import crypt

import io

import MySQLdb

from  datetime import datetime

import dns.zone

from dns.exception import DNSException

from dns.rdataclass import *

from dns.rdatatype import *


CONF_FILENAME = '/etc/bind/named.conf.local'

NAMESERVERS = []

ZONE_FILENAME = '/etc/bind/zones/{domain}.hosts'

ZONE_REGEX_STR = '^zone "%s"\{.*?\s+type (.*?);\s+file ".*?";\s+\};\s*'

ZONE_REGEX = re.compile(ZONE_REGEX_STR % '(.*)', re.MULTILINE)



class AccountDelete:




	def __init__(account, username, password, domain, newdomain, email, theme):

		account.username = username

		account.password = password

		account.domain = domain

		account.newdomain = newdomain

		account.email = email

		account.theme = theme

		account.path = "/home/"+ account.username

	
	def DeleteUserDirectory(account):

		try:
			removedir =  subprocess.check_output(["rm", "-rf", account.path])	
		
		except subprocess.CalledErrorProcess:

			print "User folder can't be removed"
		
	def DeleteVirtualHosting(account):
		
		with vhost_manager.VHost() as vhost:
			
			vhost.remove(domain=account.domain, port = "80")

	def DeleteDnsZone(account):		
	
		
		file = open(CONF_FILENAME, "r+")

		list = []	
		
		zone_found = False
		
		zone = 'zone "'+ account.domain +'\"'

		for line in file:
		
			if zone in line:

				zone_found = True
			
			if zone_found :

				list.append(line)

				if "type" in line :

								
				
       

	def in_conf(account):

        	'Check if record exists within the named.conf file'

		content = open(CONF_FILENAME).read()
	
		if account.domain in content:

			return True

       	 	else:

            		return False


                  
x = AccountDelete("unisol", "unisol", "codel.com", "unisol.com", " ", " ")

x.DeleteDnsZone()

