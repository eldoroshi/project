#/bin/python

#Account Registration Script

#Version 1.0

#Author Eldo Roshi



import sys

import subprocess

import os

import crypt

import io

import pprint

from  datetime import datetime

import dns.zone

from dns.exception import DNSException

from dns.rdataclass import *

from dns.rdatatype import *


class AccountCreation:

    

	def __init__(account, name, username, password, domain, email):

		account.name = name

		account.password = password                

		account.username = username
		
		account.domain = domain
	
		account.email = email
					        
		


    #Create User Function

	def CreateUser(account):

		password = crypt.crypt(account.password, "1987")

		adduser = subprocess.Popen(["useradd",  "-d", "/home/" + account.username, "-m", account.username, "-p", password])	

    #Create Virtual Hosting

	def VirtualHosting(account):

		f = open("/etc/apache2/sites-available/sites.conf", "a+") 
		
		f.write("<VirtualHost *:80> \n")


		f.write("\tServerAdmin " + account.email + "\n") 


		f.write("\tServerName " + account.domain + "\n")
		

		f.write("\tServerAlias " + "www." + account.domain + "\n")


		f.write("\tDocumentRoot " + "/home/" + account.username + "/public_html \n") 

	
		f.write("\t<Directory /home/" + account.username + "/public_html> \n")

	
		f.write("\t\tOptions Indexes FollowSymLinks MultiViews \n")


		f.write("\t\tAllowOverride All \n")


		f.write("\t\tRequire all granted \n")


		f.write("\t</Directory> \n")
	

		f.write("\tErrorLog ${APACHE_LOG_DIR}/error.log \n")


		f.write("\tCustomLog ${APACHE_LOG_DIR}/access.log combined \n")


		f.write("</VirtualHost> \n")		
	
	
        	f.close()


   #Add Dns Zones
	
	def dnszone (account):
   	
		zone_file = "/etc/bind/db.local"
	
		domain = "localhost"
  
		try:

			
			zone = dns.zone.from_file(zone_file, domain)

	
			for (name, ttl, rdata) in zone.iterate_rdatas(SOA):	

				print rdata

				serial = rdata.serial

				new_serial = datetime.now().strftime("%Y%m%d%H%M%S")

    				print "Changing SOA serial from %s to %s" % (serial, new_serial)
							
				rdata.serial = int(new_serial)						
				rdata.mname = dns.name.Name(("ns1", "codeless-hosting", "co", ""))

				
				

			print "Adding record of type A:", account.domain

			NS_add = "@"

			target = dns.name.Name(("ns1", "codeless-hosting", "co", ""))

			print "Adding record of type NS:", NS_add

			rdataset = zone.find_rdataset(NS_add, rdtype=NS, create=True)

			rdata = dns.rdtypes.ANY.NS.NS(IN, NS, target)

			rdataset.add(rdata, ttl=86400)	
				
			rdataset = zone.find_rdataset("www", rdtype=A, create=True)

			rdata = dns.rdtypes.IN.A.A(IN, A, address="192.168.1.30")

			rdataset.add(rdata, ttl=86400)
	     
			new_zone_file = "/etc/bind/zones/db.%s" % account.domain
			
			zone.to_file(new_zone_file)

		
		except DNSException, e:

			print e



x = AccountCreation("codel", "codel", "codel_pass", "codel.com", "email@codel.com" )
    
x.CreateUser()

x.VirtualHosting()

x.dnszone()
