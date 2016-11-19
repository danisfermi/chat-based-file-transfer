from socket import *

serverList = ["127.0.0.1","192.168.0.102"] # 2 server IP's to be added here
serverPort = [i for i in xrange(20000,20009)]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.bind(('', 7733))
connectFlag=True

for i in serverList:
    for j in serverPort:
        if clientSocket.connect(i,j) is True:
            print "You are now connected to Server " + i + " on Port Number" + j
            break
        else:
            connectFlag=False

if connectFlag is False:
    print "Connection Error. Please try again later"

class Client(object):
  def __init__(self):
    print "Hello World"
