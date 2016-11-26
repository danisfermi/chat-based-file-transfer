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
    self.udp_server_name = msg[0][1:]
    self.socket = socket(AF_INET, SOCK_DGRAM)
    self.sip, self.sport = '', 0
    self.cport = bind_to_random(self.socket)
    if len(msg) < 3:
      client_send(self.parent.socket, '@' + self.udp_server_name + 'ERROR| Please specify filename')
      self.suspended = True
    else:
      self.filename = msg[2]
      self.suspended = not self.check_file(self.filename)

  def udp_send(self, msg):
    self.socket.sendto(msg.encode(), (self.sip, self.sport))

  def udp_recv(self, size=2048):
    msg, saddr = self.socket.recvfrom(size)
    assert saddr == self.sip
    msg = msg.decode()
    print msg
    return msg

  def check_file(self):
    """
    iterate over file-folder and check if the filename is available. Else: send an error message.
    """
    for file in os.listdir('Folder'):
      if fnmatch.fnmatch(file, self.filename):
        return True
    client_send(self.parent.socket, '@' + self.udp_server_name + 'ERROR| File Not Found')
    return False

  def execute(self, msg):
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
    msg = client_recv(self.parent.socket)
    try:
      self.sip, self.sport = msg[1], int(msg[2])
    except ValueError:
      self.suspended = True
    client_send(self.parent.socket, 'OK| Sending file on port ' + self.sport + '. Send (N)ACKs to |' + self.cport)

  def transfer(self):
    """
    Transfer the filename in our folder/filename to the server.
    """
    # TODO::take buffer size from an ip
    if self.suspended:
      return
    buff = 2048
    f = open(self.filename)
    msg = f.read(buff)
    while msg != '' and not self.suspended:
      send_pkt(msg)
      msg = f.read(buff)
    f.close()

  def send_pkt(self, msg, tries=10):
    """
    Send msg to socket. Receive an ACK from other side that has format #FROM|(N)ACK
    retry send if NACK, else return.
    """
    self.udp_send(msg)
    msg_list = self.udp_recv()
    while msg_list[1] == 'NACK' and tries > 1:
      tries -= 1
      self.udp_send(msg)
      msg_list = self.udp_recv()
    if msg_list[1] != 'ACK':
      self.suspended = True
