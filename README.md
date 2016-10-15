# srget
CP2 update.
Project 1 for data communications class

Hello and welcome to README.md

I am Rin, and I am here to guide you.

In order to execute the file, simply double click it and you will be able to enter the input for the code. The input of the code will be as follows:

                                            ./srget -o filename website

The file name can be whatever you like, and you just have to put the URL of the website you want to download the data from.

If when you execute the file, permission is denied, simply input the following into the command line:

                                                  chmod +x srget
                         
That is it for this checkpoint, enjoy downloading your files!

How my code works:

It takes arguments from the command line and feeds them into the function. The function takes only the filename which includes the extension as well as the website from which it is downloaded in.

First i set the location of where I want my downloaded files to be kept, in this case it is the desktop. 
Then, what it does next is takes the url, splits it and finds the main components such as the host, and path. I found the scheme which shows whether it is HTTP or HTTPS and if it is HTTPS to exit the program.
You will use these variables in the GET part of the code. You must put in the host and path as follows in the code:

                http_request = "GET " + mypath + " HTTP/1.1" + NL + "Host: " + host + NL + NL
                
Next, I open sockets for my computer to contact the server and then send the http request. When i send the request, I create a buffer which will temporarily store my data that is downloaded from the internet. From then, I create a new file, with the filename given in the input with the extension. Once I create the file, I write the data from the buffer into the file.

From the buffer, I can gather data of headers so I get the header to see the HTTP request. I split it so that I can check see whether or not the request is 200. For this checkpoint, I have also written the redirect part of the code, however it is not needed for this checkpoint so I have commented it out. So if i have a request to redirect such as 301 or 302, I will just exit the program. This is because I wrote a statement that if it is not 200, to exit the program.
