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
    self.parent = parent
    self.udp_client_name = msg[0][1:]
    self.socket = socket(AF_INET, SOCK_DGRAM)
    self.cip, self.cport = msg[3], int(msg[4])
    self.sip, self.sport = self.parent.ip, bind_to_random(self.socket)
    self.filename = msg[2]
    self.suspended = False

  def udp_send(self, msg):
    # print self.cip, self.cport
    self.socket.sendto(msg.encode(), (self.cip, self.cport))

  def udp_recv(self, size=2048):
    msg, saddr = self.socket.recvfrom(size)
    assert saddr[0] == self.cip
    msg = str(msg.decode())
    if msg[-1:] == '\n':
      msg = msg[:-1]
    print msg
    return msg

  def execute(self):
    """
    Comes here when a file is requested.
    Msg from UDPServer is in format: #FROM|getfile|filename|udpserver_IP|udpserver_port
    """
    self.connect()
    self.transfer()

  def connect(self):
    """
    Connect to server ip and port from a random client port cport = random.randrange(something)
    Save c-port in self. Bind to cport and connect to server.
    """
    if self.suspended:
      return
    if not self.parent.check_file(self.filename):
      self.udp_send('ERROR| File Not Found')
      self.suspended = True

    self.udp_send('OK| Sending file on port ' + str(self.cport) + ' from |' + str(self.sip) + '|' + str(self.sport))

  def transfer(self):
    """
    Transfer the filename in our folder/filename to the server.
    """
    # TODO::take buffer size from an ip
    if self.suspended:
      return
    buff = 2048
    f = open('folder/' + self.filename)
    msg = f.read(buff)
    while msg != '' and not self.suspended:
      self.send_pkt(msg)
      msg = f.read(buff)
    self.send_pkt('EOF')
    f.close()

  def send_pkt(self, msg, tries=10):
    """
    Send msg to socket. Receive an ACK from other side that has format #FROM|(N)ACK
    retry send if NACK, else return.
    """
    self.udp_send(msg)
    msg = self.udp_recv()
    while len(msg) > 3 and msg[:4] == 'NACK' and tries > 1:
      tries -= 1
      self.udp_send(msg)
      msg = self.udp_recv()
    if msg[:3] != 'ACK':
      self.suspended = True
