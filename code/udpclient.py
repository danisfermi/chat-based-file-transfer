#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging
import os

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
    # try:
    #   msg = msg
    # except TypeError:
    #   try:
    #     msg = msg.encode('utf-8')
    #   except UnicodeDecodeError:
    #     try:
    #       msg = msg.encode('latin-1')
    #     except TypeError:
    #       self.suspended = True
    #       return
    msg = str(msg)
    # if msg[-1:] == '\n':
    #   msg = msg[:-1]
    # print msg
    return msg

  def write_filename(self, filename):
    if self.parent.check_file(filename):
      return self.write_filename('1' + filename)
    else:
      return filename

  def execute(self):
    msg = self.udp_recv()
    if msg[:5] == 'ERROR':  # Peer rejects connection or File not found on peer
      print msg
      self.suspended = True
      return
    elif msg[:2] == 'OK':  # Save peer ip and port details, bind a port and send that
      print msg
      msg = msg.split("|")
      self.sip = msg[2]
      self.sport = int(msg[3])
      print self.sip, self.sport
    else:
      return
    new_name = self.write_filename(self.filename)
    f = open('folder/' + new_name, 'w')
    while not self.suspended:
      msg = self.udp_recv()
      self.udp_send('ACK')
      if msg[:3] == 'EOF':
        f.close()
        os.rename('folder/' + new_name, 'folder' + self.filename)
        self.suspended = True
        # print "Client all close"
      else:
        f.write(msg)
        # print msg
    # print 'finished'
