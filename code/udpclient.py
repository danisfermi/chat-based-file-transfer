#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)


class UDPClient(object):
  """
  """

  def __init__(self, parent, msg, s, cp):
    self.parent = parent
    self.socket = s
    self.udp_clientname = msg[0][1:]
    self.sip, self.sport = '', 0
    self.cip, self.cport = self.parent.ip, cp
    self.filename = msg[2]
    self.suspended = False

  def udp_send(self, msg):
    self.socket.sendto(msg.encode(), (self.sip, self.sport))

  def udp_recv(self, size=2048):
    msg, saddr = self.socket.recvfrom(size)
    msg = str(msg.decode())
    if msg[-1:] == '\n':
      msg = msg[:-1]
    print msg
    return msg

  def execute(self):
    msg = self.udp_recv()
    if msg[:5] == 'ERROR':  # File not found on peer
      self.suspended = True
      return
    elif msg[:2] == 'OK':  # Save peer ip and port details, bind a port and send that
      msg = msg.split("|")
      self.sip = msg[2]
      self.sport = int(msg[3])
      print self.sip, self.sport
    else:
      return
    f = open('folder/' + self.filename + '1', 'w')
    while not self.suspended:
      msg = self.udp_recv()
      self.udp_send('ACK')
      if msg[:3] == 'EOF':
        self.suspended = True
      else:
        f.write(msg)
        # print msg
