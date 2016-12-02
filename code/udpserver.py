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
    udp_client_name = msg[0][1:]
    sock = socket(AF_INET, SOCK_DGRAM)
    filename, cip, cport = msg[2], msg[3], int(msg[4])
    self.parent = parent
    self.udp_client_name = udp_client_name
    self.socket = sock
    self.cip, self.cport = cip, cport
    self.sip, self.sport = self.parent.ip, bind_to_random(self.socket)
    self.filename = filename
    self.suspended = False

    if not self.parent.conn_left:
      message = '@' + msg[0][1:] + '|ERROR: Max file share connections reached. Please try later'
      self.udp_send(message)
      self.suspended = True
    else:
      self.parent.max_conn_lock.acquire()
      self.parent.conn_left -= 1
      self.parent.max_conn_lock.release()

  def udp_send(self, msg):
    # print self.cip, self.cport
    # try:
    #   msg = msg
    # except TypeError:
    #   try:
    #     msg = msg.decode('hex')
    #   except TypeError:
    #     try:
    #       msg = msg.decode('utf-8')
    #     except UnicodeDecodeError:
    #       try:
    #         msg = msg.decode('latin-1')
    #       except TypeError:
    #         self.suspended = True
    #         return

    self.socket.sendto(msg, (self.cip, self.cport))

  def udp_recv(self, size=2048):
    msg, saddr = self.socket.recvfrom(size)
    assert saddr[0] == self.cip
    msg = str(msg.decode())
    if msg[-1:] == '\n':
      msg = msg[:-1]
    if msg != 'ACK':
      print msg
    return msg

  def execute(self):
    """
    Comes here when a file is requested.
    Msg from UDPServer is in format: #FROM|getfile|filename|udpserver_IP|udpserver_port
    """
    self.connect()
    self.transfer()
    self.parent.max_conn_lock.acquire()
    self.parent.conn_left += 1
    self.parent.max_conn_lock.release()

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
    # print "All close"

  def send_pkt(self, send_msg, tries=10):
    """
    Send msg to socket. Receive an ACK from other side that has format #FROM|(N)ACK
    retry send if NACK, else return.
    """
    self.udp_send(send_msg)
    msg = self.udp_recv()
    while len(msg) > 3 and msg[:4] == 'NACK' and tries > 1:
      tries -= 1
      self.udp_send(send_msg)
      msg = self.udp_recv()
    if msg[:3] != 'ACK':
      print "Non ACK non NACK"
      self.suspended = True
