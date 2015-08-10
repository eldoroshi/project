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
	
	def __init__(account, username, password, domain, email, theme):

		account.username = username
		
		account.password = password
	
		account.domain = domain

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

	def EditDomain(account):

		newdomain

	
x = AccountEditing("unisol", "unicorn", "unisol.com", "email@unisol.com", "twentyfifteen")

x.EditUserPass()
