
from socket import *
import random
import sys
import thread


def send_data(socket, data):
  #TODO
  try:
    data_left = socket.send(data+'\n')
  except error:
    print 'sendall data error' + data_left


def send_ok(socket, opt_msg=''):
  #TODO
  msg = 'OK|' + opt_msg
  send_data(socket, msg)


def send_err(socket, err_msg):
  #TODO
  msg = 'ERROR|' + err_msg
  send_data(socket, msg)


def send_list(socket, list):
  #TODO
  msg = "|".join(list)
  return send_data(socket, msg)


def recv_data(socket):
  try:
    recv_buf = socket.recv(4096)
  except error:
    print 'recv_data error'
    recv_buf = 0
  return recv_buf


def decode_data(recv_buf):
  try:
    recv_buf = str(recv_buf.decode())
    if recv_buf[-2:] == '\r\n' : recv_buf = recv_buf[:-2]
    # recv_buf = recv_buf.replace('\r', '')  # Remove \r at the end of each message
    print recv_buf
    # recv_buf = recv_buf.replace('\n', '')  # Remove \n at the end of each message
  except UnicodeDecodeError:
    print 'Unexpected byte stream in received data'
    #TODO make sure the server does not exit.
    thread.exit()
  message = recv_buf.split("|")
  return message


def bind_to_port(s, port):
  host = gethostname()
  try:
    s.bind(('', port))
  except error:
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

