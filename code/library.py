
from socket import *
import random
import sys
import thread


class ClientNode (object):
  """
  Class object for holding client related information
  """
  def __init__(self, ip, socket, user_id):
    """
    Save client info ip, hostname and username.
    :param ip:
    :param socket:
    :param username:
    :param port_num
    """
    self.ip = ip
    self.socket = socket
    self.username = user_id


def send_data(data):
  #TODO
  return False


def send_ok(socket):
  #TODO
  msg = 'OK'
  send_data(msg)


def send_err(socket, err_msg):
  #TODO
  msg = 'ERROR|' + err_msg
  send_data(msg)


def send_list(socket, list):
  #TODO
  msg = "|".join(list)
  return send_data(msg)


def recv_data(socket):
  try:
    recv_buf = socket.recv(4096)
  except socket.error:
    print 'recv_data error'
    recv_buf = 0
  return recv_buf


def decode_data(recv_buf):
  recv_buf = recv_buf.decode()
  message = recv_buf.split("|")
  print message
  return message


def bind_to_port(s, port):
  host = gethostname()
  try:
    s.bind((host, port))
  except socket.error:
    return False
  return True


def bind_to_random(tries=10, start=40000, stop=50000):
  """
  Try to bind to random port from start to stop port numbers, tries number of times.
  :param tries:
  :param start:
  :param stop:
  :return:
  """
  while tries > 0:
    port = random.randint(start, stop-1)
    tries = -1 if bind_to_port(port) else tries - 1
  if tries is 0:
    print "Couldn't bind to data port. Aborting..."
    sys.exit()
  return port


def make_packet(data, ip):
  packet = data
  return packet

