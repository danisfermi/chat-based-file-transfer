#! /usr/bin/python
from socket import *
from library import *

serverList = ["127.0.0.1", "192.168.0.100"]  # 2 server IP's to be added here
serverPort = [i for i in xrange(20000, 20009)]

clientSocket = socket(AF_INET, SOCK_STREAM)
bind_to_port(clientSocket, 7733)

connectFlag = False
for i in serverList:
  for j in serverPort:
    try:
      print i, j
      clientSocket.connect((i, j))
      print "You are now connected to Server " + i + " on Port Number" + j
      connectFlag = True
      break
    except:
      continue

if connectFlag is False:
  sys.exit('Connection Error. Please try again later')

def listen_to_server():
  while True:
    msg = decode_data(recv_data(clientSocket))
    print msg

thread.start_new_thread(listen_to_server())
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

