#! /usr/bin/python
from socket import *
from library import *
import errno


# class Client(object):


serverList = ["0.0.0.0"] #, "127.0.0.1", "192.168.0.100", "10.139.63.161", "10.139.62.88"]  # 2 server IP's to be added here
serverPort = [i for i in xrange(20000, 20009)]

clientSocket = socket(AF_INET, SOCK_STREAM)
print bind_to_port(clientSocket, 7733)

connectFlag = False
for i in serverList:
  for j in serverPort:
    try:
      print i, j
      clientSocket.connect((i, j))
      print "You are now connected to Server " + str(i) + " on Port Number" + str(j)
      connectFlag = True
      break
    except error, exc:
      print "Exception %s " %exc

if connectFlag is False:
  sys.exit('Connection Error. Please try again later')

def listen_to_server():
  while True:
    msg = decode_data(recv_data(clientSocket))
    print msg

empty_tuple = ()
thread.start_new_thread(listen_to_server(), empty_tuple)
while True:
  input = raw_input()
  send_data(clientSocket, input)

# class Client(object):
#     info=[]
#     def __init__(self):
#         self.info.append(raw_input("Enter the username you wish to be identified as:"))
#         self.info.append("")  # Delimited to be added here
#
#     def send(self):
#         clientSocket.sendto(self.info.encode())

