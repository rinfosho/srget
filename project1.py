#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import socket
from urlparse import urlparse

def downloaddata(filename, website, header_getter):
	NL = '\r\n'
	#Parse, and find variables
	url = urlparse(website)
	path = url.path
	#port = url.port
	port = 80
	host = url.hostname
	scheme = url.scheme

	#if scheme == "https":
	#	sys.exit

	#if you want GET, make header_getter true else make it false.

	if header_getter:
		variab = "GET "
	else:
		variab = "HEAD "

	http_request = variab + path + " HTTP/1.1" + NL + "Host: " + host + NL + NL

	#open socket
	#location = '/Users/Rin/Downloads/'
	dwnld_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dwnld_socket.connect((host,port))
	dwnld_socket.send(http_request)


	#start the download process
	downloadbuffer = ""
	while True:
		data = dwnld_socket.recv(2048)
		if len(data) == 0:
			break
		downloadbuffer = downloadbuffer + data

	#write to a location in memory
	file, downloadeddata = downloadbuffer.split('\r\n\r\n')
	with open(filename,'wb') as myfile:
		myfile.write(downloadeddata)
	dwnld_socket.close()

	filedata = file.split('\r\n')
	content_len = filedata[6]
	print content_len

#if you want GET, make header_getter true else make it false.
#first send header, get the contentlenght in the downloadbuffer then send getter
#and recieve the file.
website = "http://www.muic.mahidol.ac.th/eng/wp-content/uploads/2016/10/TEA-banner-960x330-resized-1.jpg"

downloaddata("heheh.jpg",website, False)
downloaddata("heheh.jpg",website, True)
#filename will be sys.argv[2]
