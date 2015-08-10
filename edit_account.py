#/bin/python

#Account Editing Script

#Version 1.1

#Author Eldo Roshi


import sys

import subprocess

import os

import crypt

import io

import MySQLdb

from  datetime import datetime

import dns.zone

from dns.exception import DNSException

from dns.rdataclass import *

from dns.rdatatype import *

class AccountEditing:
	
	def __init__(account, username, password, domain, newdomain, email, theme):

		account.username = username
		
		account.password = password
	
		account.domain = domain

		account.newdomain = newdomain

		account.email = email

		account.theme = theme


	#Editing User Password

	def EditUserPass(account):
		
		newpassword = crypt.crypt(account.password, "1987")
		
		try:
		
			editpassword = subprocess.Popen(["usermod", "-p", newpassword, account.username ])
		
			print "New password was changed succesfull" 
		
		except	subprocess.CalledProcessError:

			print "Error during the password editing"

	
	def EditDomainVh(account):

		
		n = open("/etc/apache2/sites-available/sites.conf").read()

		if account.domain in n:
			
			n = n.replace(account.domain, account.newdomain)
			
			f= open("/etc/apache2/sites-available/sites.conf", "w")
			
			try:
			
				f.write(n)

				print "File was writen"		

			except:

				print "File can't be written"	
			
			f.close()

		else:   
	
			print "Error during the process of changing the domain in virtual host"

	def EditDomainDns(account):
		
		dnsfilezone = "/etc/bind/zones/db." + account.domain
		
		newdnsfilezone = "/etc/bind/zones/db." + account.newdomain
		
		namedfile = "/etc/bind/named.conf.local"
		
		try:
			updatednszone = subprocess.check_output(["mv", dnsfilezone, newdnsfilezone])
			
			if "" in updatednszone: 

				print "Dns file zonefile was updated"
			
		except subprocess.CalledProcessError:
			
			print "Dns file zone error during the process of update"
			
	        namedconf = open(namedfile).read()				
			
		if account.domain in namedconf :

			namedconf = namedconf.replace(account.domain, account.newdomain)
			
			try:
				newconf = open(namedfile, "w")
			
				newconf.write(namedconf)

				print "Named conf file was updated"		
		
			except IOError as e:

    				print "I/O error({0}): {1}".format(e.errno, e.strerror)	

			newconf.close()	
			
x = AccountEditing("unisol", "unicorn", "unisol.com", "unisolnew.com", "email@unisol.com", "twentyfifteen")

#x.EditUserPass()

#x.EditDomainVh()

x.EditDomainDns()


