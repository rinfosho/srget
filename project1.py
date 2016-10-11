#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import socket
from urlparse import urlparse

#if you want GET, make header_getter true else make it false.
#first send header, get the contentlenght in the downloadbuffer then send getter
#and recieve the file.
#def downloaddata(filename, website, header_getter): if there is HEADER and GETTER
def downloaddata(filename, website):
	NL = '\r\n'
	#Parse, and find variables
	url = urlparse(website)
	path = url.path
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

	http_request = "GET " + path + " HTTP/1.1" + NL + "Host: " + host + NL + NL

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

	#write to a location in memory
	file, downloadeddata = downloadbuffer.split(NL + NL)
	with open(filename,'wb') as myfile:
		myfile.write(downloadeddata)
	dwnld_socket.close()

	filedata = file.split(NL)
	if len(filedata) == 9:
		content_len = filedata[6]
	else:
		print "No details given about content length"


#website = "http://www.muic.mahidol.ac.th/eng/wp-content/uploads/2016/10/TEA-banner-960x330-resized-1.jpg"
#website = "http://10.27.8.20:8080"
website = "http://ipv4.download.thinkbroadband.com/100MB.zip"

#downloaddata("heheh.jpg",website, False) #ONLY IF WE HAVE HEADER AND GETTER

#filename = sys.argv[2]
#connectionnum = sys.argv[3]
#website = sys.argv[4]
#sample call = downloaddata(filename, website)

downloaddata("heheh.zip", website)

#close connection when you reach content length
#close connection even if you dont know the content length
