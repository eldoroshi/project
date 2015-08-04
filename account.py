#/bin/python

#Account Registration Script

#Version 1.0

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


class AccountCreation:

    

	def __init__(account, name, username, password, domain, email, theme):

		account.name = name

		account.password = password                

		account.username = username
		
		account.domain = domain
	
		account.email = email

		account.theme = theme
					        
		


    #Create User Function

	def CreateUser(account):

		password = crypt.crypt(account.password, "1987")

		adduser = subprocess.Popen(["useradd",  "-d", "/home/" + account.username, "-m", account.username, "-p", password])	
	

	#Create public html directory
    
	def publichtml_dir(account):

		try:
			createdir = subprocess.check_output(["mkdir", "/home/" + account.username + "/public_html"])
		
			print "Public Folder Created"

		except subprocess.CalledProcessError:
			

				print "Error Folder can't be created"

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

	#Populate the named.conf.local zone

	def addzone (account):
		
		f = open("/etc/bind/named.conf.local", "a+")
		
		f.write("\t zone \""+ account.domain + "\" { \n")
		
		f.write("\t\t type master;\n")
	
		f.write("\t\tfile \"/etc/bind/zones/db." + account.domain + "\"; \n")

		f.write("};")

		f.close()	
		
     	

	def loadconfig (account):
		
		
		try: 
		
			apachereload = subprocess.Popen(["apache2ctl", "graceful"])
			print "restarted"
		
		except subprocess.CalledProcessError:

			print "Some error in the sites.conf file"		

		namedconfig = subprocess.check_output(["named-checkconf"])
		
		if "" in namedconfig :
			
			zonereload = subprocess.Popen(["rndc", "reload"])
			
			zonereload.wait()

			print zonereload.communicate()	
			
	
	def createdb(account):

		db = MySQLdb.connect("localhost", "root", "eldo2014")
		
		cur = db.cursor()
		
		try:
			db_name = account.username + "db"

			createdb = "CREATE DATABASE IF NOT EXISTS %s;" %(db_name)
 					
			results = cur.execute(createdb)
			
			print "Database Creation", results
			
			createuser = "CREATE USER '%s'@'%s'" %(account.username, account.domain)  
			
			results = cur.execute(createuser)
			
			print "User Creation", results
	
			setpassword ="SET PASSWORD FOR '%s'@'%s' = PASSWORD('%s')" %(account.username, account.domain, account.password)
			
			results = cur.execute(setpassword)
		
			print "Set the user password", results			

			give_priviledges = "GRANT ALL ON %s.* TO '%s'@'%s';" %(db_name, account.username, account.domain)		     
		
			results = cur.execute(give_priviledges) 
		
			print "Set user priviledges", results

		except MySQLdb.Error, e:
			
			print e

	#Installation of Wordpress Core

	def downloadWP(account):
		
		try:
			download = subprocess.check_output(["wp", "core", "download" , "--path=/home/"+ account.username + "/public_html", "--url="+ account.domain, "--user="+account.email ])
			
			print "Wordpress Download Complete"
				
		except subprocess.CalledProcessError:

			print "Error during the process of wordpress core download"
	
	
	#Install and configure wordpress
	def installWP(account):
		
		try:
		
	        	 config = subprocess.check_output(["wp", "core", "config", "--path=/home/"+ account.username + "/public_html", "--dbname="+ account.username + "db", "--dbuser="+ account.username , "--dbpass="+ account.password ])	
		       	installation = subprocess.check_output(["wp", "core", "install", "--path=/home/" + account.username + "/public_html", "--title=" + account.name , "--url=" + account.domain , "--admin_user=" + account.username, "--admin_password=" + account.password, "--admin_email=" + account.email ])
		
		except subprocess.CalledProcessError:

			print "Error during installation process"  		
	
	
	def installtheme(account):
		
		try:
			
			theme = subprocess.check_output(["wp", "theme", "install", "--path=/home/"+ account.username + "/public_html", account.theme, "--activate"])


			print "Theme was Installed"


		except subprocess.CalledProcessError:

			
			print "Theme installation error"


x = AccountCreation("codel", "codel", "codel_pass", "codel.com", "email@codel.com", "specular.zip" )
    
#x.CreateUser()

#x.VirtualHosting()

#x.dnszone()

#x.addzone()

#x.loadconfig()

#x.publichtml_dir()

x.createdb()
