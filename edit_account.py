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

		account.path = "/home/"+ account.username + "/public_html"

		

	#Editing User Password
	def EditUserPass(account):
		
		newpassword = crypt.crypt(account.password, "1987")
		
		try:
		
			editpassword = subprocess.Popen(["usermod", "-p", newpassword, account.username ])
		
			return "New password was changed succesfull" 
		
		except	subprocess.CalledProcessError:

			return "Error during the password editing"

	
	#Update the domain name to virtual hosting
	def EditDomainVh(account):

		
		n = open("/etc/apache2/sites-available/sites.conf").read()

		if account.domain in n:
			
			n = n.replace(account.domain, account.newdomain)
			
			f= open("/etc/apache2/sites-available/sites.conf", "w")
			
			try:
			
				f.write(n)

				return "File was writen"		

			except:

				return "File can't be written"	
			
			f.close()

		else:   
	
			return "Error during the process of changing the domain in virtual host"
	

	#Change the domain name into zone files
	def EditDomainDns(account):
		
		dnsfilezone = "/etc/bind/zones/db." + account.domain
		
		newdnsfilezone = "/etc/bind/zones/db." + account.newdomain
		
		namedfile = "/etc/bind/named.conf.local"
		
		try:
			updatednszone = subprocess.check_output(["mv", dnsfilezone, newdnsfilezone])
			
			if "" in updatednszone: 

				return "Dns file zonefile was updated"
			
		except subprocess.CalledProcessError:
			
			return "Dns file zone error during the process of update"
			
	        namedconf = open(namedfile).read()				
			
		if account.domain in namedconf :

			namedconf = namedconf.replace(account.domain, account.newdomain)
			
			try:
				newconf = open(namedfile, "w")
			
				newconf.write(namedconf)

				return "Named conf file was updated"		
		
			except IOError as e:

    				return "I/O error({0}): {1}".format(e.errno, e.strerror)	

			newconf.close()	
			
	#Update wordpress domain
	def EditDomainWp(account):


		try:
			updatedomain = subprocess.check_output(["wp", "search-replace", account.domain, account.newdomain, "--skip-columns=guid", "--path="+ account.path, "--allow-root"])
			
			return "New domain was updated"					

		except subprocces.CalledProcessError:

			return "Error during the update of the wordpress domain"

	
	#Update the wordpress password
	def EditPassWp(account):
		
		newpassword = crypt.crypt(account.password, "Abcdefgzhsh1AbCD")


		try:
		
			updatedpass =  subprocess.check_output(["wp", "user", "update", account.username, "--path=" + account.path, "--user_pass=" + newpassword, "--allow-root"])
			
			return "Password was updated for user " + account.username
		
		except subprocess.CalledProcessError:
			
			return "Error during the update of the  wordpress user password"
	
	
	#Change wordpress theme
	def EditthemeWp(account):
		
		try:
			updatetheme =  subprocess.check_output(["wp", "theme", "install", account.theme, "--allow-root", "--path="+account.path, "--activate"]) 
		       
		        return "Theme was changed"

		except subprocess.CalledProcessError:

			return "Error during the process of wordpress theme update"
			

x = AccountEditing("unisol", "unicorn", "unisol.com", "unisolnew.com", "email@unisol.com", "twentyfifteen")

#x.EditUserPass()

#x.EditDomainVh()

#x.EditDomainDns()

#x.EditDomainWp()

#x.EditPassWp()

#x.EditthemeWp()
