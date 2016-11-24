#! /usr/bin/python
from library import *


# class Client(object):


serverList = ['0.0.0.0', '127.0.0.1', '192.168.0.103', '10.139.63.161', '10.139.62.88', 'localhost']  # 2 server IP's to be added here
serverPort = [i for i in xrange(20000, 20009)]

clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
print bind_to_port(clientSocket, 7733)

connectFlag = False
for i in serverList:
  for j in serverPort:
    try:
      print i, j
      clientSocket.connect(('', j))
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
    input = raw_input()
    send_data(clientSocket, input)  # Danis: I brought this here because it wasn't getting called before

empty_tuple = ()
thread.start_new_thread(listen_to_server(), empty_tuple)

