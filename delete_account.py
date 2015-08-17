#/bin/python

#Account Editing Script

#Version 1.1

#Author Eldo Roshi


import sys

import subprocess

import vhost_manager

with vhost_manager.VHost() as vhost:

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

		account.path = "/home/"+ account.username

	def DeleteUserDirectory(account):

		try:
			removedir =  subprocess.check_output(["rm", "-rf", account.path])	
		
		except subprocess.CalledErrorProcess:

			print "User folder can't be removed"
		
	def DeleteVirtualHosting(account):

		vhost.remove(domain=account.domain, port = "80")

	def DeleteDnsZone
