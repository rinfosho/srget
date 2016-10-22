#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Checkpoint 2
import sys
import socket as skt
from urlparse import urlparse
import os

#if you want GET, make header_getter true else make it false.
#first send header, get the contentlenght in the downloadbuffer then send getter
#and recieve the file.
#def downloaddata(filename, website, header_getter): if there is HEADER and GETTER
NL = '\r\n'
def downloaddata(filename, website):
	#get elements from parsing
	parsed = parsing(website)
	mypath, port, host, scheme = parsed[0], parsed[1], parsed[2], parsed[3]

	if scheme == "https":
		print "HTTPS is not supported."
		sys.exit()



	http_request = "GET " + mypath + " HTTP/1.1" + NL + "Host: " + host + NL + NL
	#open socket
	#location = '/Users/Rin/Downloads/'
	dwnld_socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
	dwnld_socket.settimeout(2)
	dwnld_socket.connect((host,port))
	dwnld_socket.send(http_request)

	print "Your file is downloading.."

	#start the download process
	downloadbuffer = ""
	counter = 0
	while True and counter <4:
		counter = counter + 1
		try:
			data = dwnld_socket.recv(32768)
		except skt.timeout:
			break
		downloadbuffer = downloadbuffer + data
	dwnld_socket.close()

	header = downloadbuffer.split(NL)
	httpheader = header[0].split(" ")

	#REDICECT!!
	if 300<= int(httpheader[1])<=307:
		data = downloadbuffer.split(NL)
		urldata = parsing(data[3])
		newhost, newport, newpath, newscheme = urldata[0], urldata[1], urldata[2], urldata[3]
		newhost = newhost.strip(" ")
		usethishost = urlparse(newhost)
		if newpath == None:
			newpath = "/"

		newhttp = "GET " + newpath + " HTTP/1.1" + NL + "Host: " + usethishost.hostname + NL + NL

		#open new socket
		new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		new_socket.settimeout(2)
		new_socket.connect((usethishost.hostname,newport))
		new_socket.send(newhttp)

		newdownloadbuffer = ""
		while True:
			try:
				newdata = new_socket.recv(32768)
			except skt.timeout:
				break
			newdownloadbuffer = newdownloadbuffer + newdata

		return newdownloadbuffer

	elif 400<= int(httpheader[1]) <= 417:
		sys.exit("Client error")
	elif 500<= int(httpheader[1]) <= 505:
		sys.exit("Server error")
	else:
		return downloadbuffer

def writetofile(filename, data):
	b = []
	b = data.split(NL+NL)
	#write to a location in memory
	with open(filename,'wb') as myfile:
		myfile.write(b[1])

def parsing(website):
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
	return mypath, port, host, scheme

def getrange(path, host, bytes):
	#bytes = bytes recieved from original file (len)
	return ("GET {a} HTTP/1.1" + NL + "Host: {b}" + NL + "Connection: close" + NL + "Range: bytes={c}-" + NL + NL).format(a=path, b=host, c=bytes)

def writetempfile(filename, data, bytesrec):
	#write to a location in memory
	with open(filename + ".cr" + ".txt",'wb') as tempfile:
		b = []
		b = data.split(NL + NL)
		head = b[0].split(NL)[1:]
		for dat in head:
			newdat = dat.split(":")
			if newdat[0] == "Content-Length" or newdat[0] == "ETag" or newdat[0] == "Last-Modified":
				print dat
				tempfile.write(dat+ NL)
		tempfile.write("Bytes-Received: " + str(len(str(bytesrec))))

def findcontentandlastmod(filename, website):
	content_len = 0
	lastmod = ""

	b = []
	b = downloaddata(filename,website).split(NL+NL)
	for i in b:
		spl = i.split(" ")
		if spl[0] == "Content-Length:":
			content_len = spl[1]
		if spl[0] == "Last-Modified:":
			lastmod = spl[1]
	
	return content_len, lastmod

def resume(filename, website):
	content_len = ""
	etag = ""
	lastmodif = ""
	#Check if file exists, if exist then terminate program
	if os.path.exists(filename):
		#see if file size is the same as the content length
		fileinfo = os.stat(filename)
		#info about the headers kept in here
		contentetag = []		
		tempfilename = filename+".cr"+".txt"
		with open(tempfilename,'r') as tempfile:
			for line in tempfile:
				contentetag.append(line)
		res_file = open(filename, 'a')
		#put content len, etag and last modi in variables
		for ele in contentetag:
			splele = ele.split(":")
			if splele[0] == "Content-Length":
				content_len = splele[1]
			if splele[0] == "ETag":
				etag = splele[1]
			if splele[0] == "Last-Modified":
				lastmodif += splele[1]


		a = parsing(website)
		path = a[0]
		port = a[1]
		host = a[2]

		#mamke new connection		
		dwnld_socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
		dwnld_socket.connect((host,port))
		dwnld_socket.settimeout(2)
		newhttp_request = getrange(path, host, fileinfo.st_size)
		print newhttp_request
		dwnld_socket.send(newhttp_request)
		print "sockets opened"
		con,idc=findcontentandlastmod(filename,website)

		#start the download process
		new_head = ""
		downloadbuffer = ""
		while NL+NL not in new_head:
			data = dwnld_socket.recv(1)
			new_head = new_head + data
		while True:
			data = dwnld_socket.recv(32768)
			if len(data) == 0:
				break
			downloadbuffer = data
			res_file.write(downloadbuffer)
		dwnld_socket.close()
		res_file.close()
		print "checking and downloading remaining."

		writetempfile(filename, website, len(downloadbuffer))

	else:
		data = downloaddata(filename, website)
		writetofile(filename, data)
		#create a temp file for contentlen, bytes recieeved, last modified e-tag
		bytes_received = os.stat(filename)
		writetempfile(filename,data, bytes_received)





#website = "http://www.muic.mahidol.ac.th/eng/wp-content/uploads/2016/10/TEA-banner-960x330-resized-1.jpg"
website = "http://10.27.8.20:8080/primes11.txt"
#website = "http://ipv4.download.thinkbroadband.com/100MB.zip"
#website = "http://www.abc.com"
#website = "http://10.27.8.20:8080/bigfile.xyz"
#website = "http://www.muic.mahidol.ac.th/eng/wp-content/uploads/2016/10/King.jpg"

#downloaddata("heheh.jpg",website, False) #ONLY IF WE HAVE HEADER AND GETTER

#filename = sys.argv[2]
# #connectionnum = sys.argv[3]
#website = sys.argv[-1]
filename = "hihi.txt"
resume(filename, website)

#resume("raja.jpg", website)

#close connection when you reach content length
#close connection even if you dont know the content length