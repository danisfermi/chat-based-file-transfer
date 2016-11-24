#! /usr/bin/python
from library import *


class Client(object):
  """

  """
  def __init__(self, start=7733, tries=10):
    self.serverList = ['0.0.0.0', '192.168.0.100', '192.168.0.103', '127.0.0.1', '10.139.63.161', '10.139.62.88',
                  'localhost']  # 2 server IP's to be added here
    # self.portlist = [i for i in xrange(, 7744)]
    self.serverPort = [i for i in xrange(50000, 50009)]
    self.socket = socket(AF_INET, SOCK_STREAM)
    for port in xrange(start, start+tries-1):
      if bind_to_port(self.socket, port):
        break

    connectFlag = False
    for s in self.serverList:
      print s, port
      self.socket.connect((s, port))
      connectFlag = True
      break

    if connectFlag is False:
      sys.exit('Connection Error. Please try again later')

    def listen_to_server():
      while True:
        msg = client_recv(self.socket)

    def execute():
      empty_tuple = ()
      thread.start_new_thread(listen_to_server(), empty_tuple)
      while True:
        input = raw_input()
        client_send(self.socket, input)

c1 = Client()
c1.execute()