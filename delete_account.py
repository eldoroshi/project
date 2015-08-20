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


class AccountDelete:




	def __init__(account, username, password, domain, newdomain, email, theme):

		account.username = username

		account.password = password

		account.domain = domain

		account.newdomain = newdomain

		account.email = email

		account.theme = theme

		account.path = "/home/"+ account.username

	#Delete UserDirectory
	def DeleteUserDirectory(account):

		try:
			removedir =  subprocess.check_output(["rm", "-rf", account.path])	
		
		except subprocess.CalledErrorProcess:

			print "User folder can't be removed"
	
	#Delete Virtual Hosting 	
	def DeleteVirtualHosting(account):
		
		with vhost_manager.VHost() as vhost:
			
			vhost.remove(domain=account.domain, port = "80")

	
	#Delete Zone in named.conf.local
	def DeleteDnsZone(account):		
		
		list = []
		
		file = open(CONF_FILENAME, "r+")
		
		zone_found = False
			
		zone = 'zone "'+ account.domain +'\" '

		for line in file:
					
			
			if zone in line:

				zone_found = True
							
			if zone_found :
				
				if "type" in line :		
					continue
			
				if "file" in line :

					continue
				 			
				if "}" in line:

					zone_found = False
	
			else:

				list.append(line)


		content = "\n".join(list)
		
		try:		

			f = open(CONF_FILENAME, "w")

			f.write(content)
		
		except IOError as e:

    			print "I/O error({0}): {1}".format(e.errno, e.strerror)	


		f.close()


	#Delete database and user responsible for this database
	def DeleteDb(account):

		db = MySQLdb.connect("localhost", "root", "eldo2014")
		
		cur = db.cursor()
		
		try:

			db_name = account.username + "db"

			deletedb = "DROP DATABASE %s;" %(db_name)
			
			results = cur.execute(deletedb)
		
			print results

			deleteuser = "DROP USER '%s'@'%s'" %(account.username, "localhost")

			results = cur.execute(deleteuser)

			print results
			
			cur.close()

		except MySQLdb.Error, e:

			print e
		
		
	#Delete User		
	def DeleteUser(account):


		try:

			removeuser =  subprocess.check_output(["userdel", account.username])	

		
		except subprocess.CalledErrorProcess:



			print "User can't be removed"			
			



                  
x = AccountDelete("unisol", "unisol", "uni.com", "uni.com", " ", " ")

x.DeleteDnsZone()

