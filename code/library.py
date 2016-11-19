
import socket, random, sys


class ClientNode (object):
  """
  Class object for holding client related information
  """
  def __init__(self, ip, hostname, username, port_num):
    """
    Save client info ip, hostname and username.
    :param ip:
    :param hostname:
    :param username:
    :param port_num
    """
    self.ip = ip
    self.hostname = hostname
    self.username = username
    self.port_num = port_num


def bind_to_port(port):
  return False;


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

