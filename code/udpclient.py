#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)


class UDPClient(object):
  """
  """

  def __init__(self, parent, msg, socket, cip):
    self.parent = parent
    self.socket = socket
    self.udp_clientname = msg[0][1:]
    self.sip, self.sport = '', 0
    self.cip, self.cport = self.parent.ip, cip
    self.filename = msg[2]
    self.suspended = False

  def udp_send(self, msg):
    self.socket.sendto(msg.encode(), (self.sip, self.sport))

  def udp_recv(self, size=2048):
    msg, saddr = self.socket.recvfrom(size)
    print msg, saddr[0], self.sip
    # assert saddr[0] == self.sip
    msg = str(msg.decode())
    if msg[-1:] == '\n':
      msg = msg[:-1]
    msg = msg.split("|")
    print msg
    return msg

  def execute(self):
    msg = self.udp_recv()
    if msg[0] == 'ERROR':  # File not found on peer
      self.suspended = True
      return
    elif msg[0] == 'OK':  # Save peer ip and port details, bind a port and send that
      self.sip = msg[2]
      self.sport = int(msg[3])
    else:
      return

    while not self.suspended:
      msg = self.udp_recv()
      if msg[0] == 'EOF':
        self.suspended = True
      else:
        print msg
