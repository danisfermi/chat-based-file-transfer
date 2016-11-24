#! /usr/bin/python
from library import *


class Client(object):
  """

  """
  def __init__(self, pport=None, sport=None, ip=None, start=7744, tries=10):


    self.socket = socket(AF_INET, SOCK_STREAM)

    # if port is None or ip is None:
    #   self.serverList = ['0.0.0.0', '192.168.0.100', '192.168.0.103', '127.0.0.1', '10.139.63.161', '10.139.62.88',
    #                      'localhost']  # 2 server IP's to be added here
    #   # self.portlist = [i for i in xrange(, 7744)]
    #   self.serverPort = [i for i in xrange(50000, 50009)]
    #   for port in xrange(start, start+tries-1):
    #     if bind_to_port(self.socket, port):
    #       break
    #
    #   connectFlag = False
    #   for s in self.serverList:
    #     print s, port
    #     try:
    #       self.socket.connect((s, port))
    #       connectFlag = True
    #       print "Connect success"
    #       break
    #     except error:
    #       print "No luck there."
    #
    #   if connectFlag is False:
    #     sys.exit('Connection Error. Please try again later')
    # else:
    print ip, pport, sport
    self.socket.bind(('', pport))
    self.socket.connect((ip, sport))

  def listen_to_server(self):
    while True:
      msg = client_recv(self.socket)

  def execute(self):
    empty_tuple = ()
    thread.start_new_thread(self.listen_to_server(), empty_tuple)
    while True:
      input = raw_input()
      client_send(self.socket, input)

print int(sys.argv[3]), int(sys.argv[2]), sys.argv[1]
c1 = Client(int(sys.argv[3]), int(sys.argv[2]), sys.argv[1]);
c1.execute()





