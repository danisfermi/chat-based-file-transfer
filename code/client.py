#! /usr/bin/python
from library import *
from udpclient import *
from udpserver import *
import fnmatch
import os
import random

class Client(object):
  """

  """
  def __init__(self, sport=None, ip=None, start=7744, tries=10):
    """

    :param pport:
    :param sport:
    :param ip:
    :param start:
    :param tries:
    """
    self.socket = socket(AF_INET, SOCK_STREAM)
    self.suspended = False
    self.pport = random.randrange(23456, 24567)
    self.ip = gethostbyname(gethostname())

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
    print ip, self.pport, sport
    self.socket.bind(('', self.pport))
    self.socket.connect((ip, sport))

  def check_file(self, filename):
    """
    iterate over file-folder and check if the filename is available. Else: send an error message.
    """
    for file in os.listdir('folder'):
      if fnmatch.fnmatch(file, filename):
        return True
    return False

  def listen_to_server(self):
    while not self.suspended:
      msg = client_recv(self.socket)
      if msg[0].lower() in ['exit', 'quit']:
        print "Thank You for using our chatroom. Press enter to continue."
        self.suspended = True
      elif len(msg) > 1:
        if msg[1].lower() in ['whohas']:
          if self.check_file(msg[2]):
            client_send(self.socket, '@' + msg[0][1:] + '|ME')
        elif msg[1].lower() in ['getfile']:
          if len(msg) < 3:
            client_send(self.socket, '@' + msg[0][1:] + '|ERROR: Please specify filename')
          else:
            empty_tuple = ()
            msg += client_recv(self.socket)[1:]  # add cip and cport sent from client
            udpserver = UDPServer(self, msg)
            thread.start_new_thread(udpserver.execute, empty_tuple)

  def execute(self):
    empty_tuple = ()
    thread.start_new_thread(self.listen_to_server, empty_tuple)
    while not self.suspended:
      input = raw_input()
      client_send(self.socket, input)
      input = input.rstrip('\n')
      input = input.split("|")
      if len(input) > 2 and input[1] == 'getfile':
        s = socket(AF_INET, SOCK_DGRAM)
        cp = bind_to_random(s)
        client_send(self.socket, '|'.join([input[0], str(self.ip), str(cp)]))
        empty_tuple = ()
        udpclient = UDPClient(self, input, s, cp)
        thread.start_new_thread(udpclient.execute, empty_tuple)


print int(sys.argv[2]), sys.argv[1]
c1 = Client(int(sys.argv[2]), sys.argv[1]);
c1.execute()

