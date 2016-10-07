#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket

def downloaddata(filename, connecnum, website):
	website.replace(':', ' ')
	port = website[1]
	#open socket
	NL = '\r\n'
	#location = '/Users/Rin/Downloads/'
	srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv_socket.connect(hostname,serv_port)
	srv_socket.read()

	#start the download process
	downloadbuffer = ""
	while True:
		data = conn.recv(16384)
		if len(data) == 0:
			break
		downloadbuffer = downloadbuffer + data

	#write to a location in memory
	CurrName, downloadeddata = downloadbuffer.split(NL + NL)
	with open(filename,'wb') as myfile:
		myfile.write(downloadeddata)
	socket.close()

#take into account the input into the terminal (parse)
url = sys.argv[-1]

#parse url
