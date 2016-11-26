#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)


class UDPServer(object):
  """
  """

  def __init__(self, parent, msg):
    self.cip, self.cport = '', 0
    self.sport = bind_to_random(self.socket)
    if len(msg) < 3:
      client_send(self.parent.socket, '@' + self.udp_server_name + '|ERROR| Please specify filename')
      self.suspended = True
    else:
      self.filename = msg[2]
      self.suspended = not self.check_file(self.filename)
    self.parent = parent
    self.socket = socket(AF_INET, SOCK_DGRAM)
    self.suspended = False
    self.udp_clientname = msg[0][1:]

  def execute(self):
    message = "@" + self.destname + "|" + self.parent.ip + "|" + self.udpport
    clientsend(self.parent.socket, message)
    data, ip = self.socket.recvfrom(4096)
