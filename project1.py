#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import socket
from urlparse import urlparse
import os

#if you want GET, make header_getter true else make it false.
#first send header, get the contentlenght in the downloadbuffer then send getter
#and recieve the file.
#def downloaddata(filename, website, header_getter): if there is HEADER and GETTER
def downloaddata(filename, website):
	NL = '\r\n'
	#Parse, and find variables
	url = urlparse(website)
	#find path
	if url.path == "":
		mypath = "/"
	else:
		mypath = url.path

	#find port
	if url.port == None:
		port = 80
	else:
		port = url.port
	host = url.hostname
	scheme = url.scheme

	if scheme == "https":
		print "HTTPS is not supported."
		sys.exit(1)

	#if you want GET, make header_getter true else make it false.

	# if header_getter:
	# 	variab = "GET "
	# else:
	# 	variab = "HEAD "

	http_request = "GET " + mypath + " HTTP/1.1" + NL + "Host: " + host + NL + NL
	#open socket
	#location = '/Users/Rin/Downloads/'
	dwnld_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dwnld_socket.connect((host,port))
	dwnld_socket.send(http_request)


	#start the download process
	downloadbuffer = ""
	while True:
		data = dwnld_socket.recv(32768)
		if len(data) == 0:
			break
		downloadbuffer = downloadbuffer + data
	print downloadbuffer

	# #IF 301 is encountered, redirect it.
	# if "301" in downloadbuffer:
	# 	dwnld_socket.close()
	# 	data = downloadbuffer.split(NL)
	# 	newurl = urlparse(data[3])
	# 	print newurl
	# 	newhost = newurl.path #this is actually the host, seems to be an error if i change it the variable name
	# 	newhost = newhost.strip(" ")
	# 	print newhost
	# 	secondhost = urlparse(newhost)
	# 	scheme = url.scheme
	# 	#find port
	# 	if url.port == None:
	# 		newport = 80


	# 	print "hostnameredirect", secondhost.hostname
	# 	print "pathredirect", newurl.hostname
	# 	#change path if its empty
	# 	if newurl.hostname == None:
	# 		newhttp = "GET " + "/" + " HTTP/1.1" + NL + "Host: " + secondhost.hostname + NL + NL
	# 	else:
	# 		newhttp = "GET " + newurl.hostname + " HTTP/1.1 " + NL + "Host: " + secondhost.hostname + NL + NL


	# 	#open new socket
	# 	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 	new_socket.connect((secondhost.hostname,newport))
	# 	new_socket.send(newhttp)

	# 	newdownloadbuffer = ""
	# 	while True:
	# 		newdata = new_socket.recv(32768)
	# 		if len(newdata) == 0:
	# 			break
	# 		newdownloadbuffer = newdownloadbuffer + newdata

	# 	#write to a location in memory
	# 	a = []
	# 	a = newdownloadbuffer.split(NL+NL)
	# 	with open(filename,'wb') as myfile:
	# 		myfile.write(a[1])

	# 	#Check header data of the server	
	# 	newlistoffiledata = a[0].split(NL)

	# 	#Find content_len
	# 	if "Content-Length" not in newlistoffiledata:
	# 		print "No details given about content length (redirect)"

	# 	new_socket.close()

	#write to a location in memory
	b = []
	b = downloadbuffer.split(NL + NL)
	with open(filename,'wb') as myfile:
		myfile.write(b[1])

	#Check header data of the server	
	listoffiledata = b[0].split(NL)

	#Find content_len
	if "Content-Length" not in listoffiledata:
		print "No details given about content length"

	dwnld_socket.close()

	#IF 301 is encountered, redirect it.
	if "301" or "302" in downloadbuffer:
		data = downloadbuffer.split(NL)
		newurl = urlparse(data[3])
		print newurl
		newhost = newurl.path #this is actually the host, seems to be an error if i change it the variable name
		newhost = newhost.strip(" ")
		print newhost
		secondhost = urlparse(newhost)
		scheme = url.scheme
		#find port
		if url.port == None:
			newport = 80


		print "hostnameredirect", secondhost.hostname
		print "pathredirect", newurl.hostname
		#change path if its empty
		if newurl.hostname == None:
			newhttp = "GET " + "/" + " HTTP/1.1" + NL + "Host: " + secondhost.hostname + NL + NL
		else:
			newhttp = "GET " + newurl.hostname + " HTTP/1.1 " + NL + "Host: " + secondhost.hostname + NL + NL


		#open new socket
		new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		new_socket.connect((secondhost.hostname,newport))
		new_socket.send(newhttp)

		newdownloadbuffer = ""
		while True:
			newdata = new_socket.recv(32768)
			if len(newdata) == 0:
				break
			newdownloadbuffer = newdownloadbuffer + newdata

		#write to a location in memory
		a = []
		a = newdownloadbuffer.split(NL+NL)
		with open(filename,'wb') as myfile:
			myfile.write(a[1])

		#Check header data of the server	
		newlistoffiledata = a[0].split(NL)

		#Find content_len
		if "Content-Length" not in newlistoffiledata:
			print "No details given about content length (redirect)"

		new_socket.close()

#website = "http://www.muic.mahidol.ac.th/eng/wp-content/uploads/2016/10/TEA-banner-960x330-resized-1.jpg"
#website = "http://10.27.8.20:8080"
#website = "http://ipv4.download.thinkbroadband.com/100MB.zip"
website = "http://www.abc.com"
#website = "http://10.27.8.20:8080/primes11.txt"

#downloaddata("heheh.jpg",website, False) #ONLY IF WE HAVE HEADER AND GETTER

#filename = sys.argv[2]
#connectionnum = sys.argv[3]
#website = sys.argv[-1]
#sample call = downloaddata(filename, website)

downloaddata("abc.txt", website)

#close connection when you reach content length
#close connection even if you dont know the content length