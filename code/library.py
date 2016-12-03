
from socket import *
import random
import sys
import thread


def client_send(s, data):
  """
  Try send data to server using socket s.
  """
  try:
    s.sendall(data)
  except error:
    print 'sendall data error'


def client_recv(s):
  """
  Receive 4KB data from server and decode and return message after splitting using delimiter '|'
  """
  try:
    recv = s.recv(4096)
    recv = str(recv)
  except UnicodeDecodeError:
    print 'Unexpected byte stream in received data'
  except error:
    print 'recv_data error'
  if recv[-1:] == '\n':
    recv = recv[:-1]
  print recv
  message = recv.split("|")
  return message


def send_data(s, data):
  """
  Send data to client via socket s
  """
  try:
    data_left = s.send(data)
  except error:
    print 'send_data error'


def send_ok(socket, opt_msg=''):
  """
  Send an OK followed by an optional message to client
  """
  msg = 'OK|' + opt_msg
  send_data(socket, msg)


def send_err(socket, err_msg):
  """
  Send an ERROR followed by a mandatory message to client
  """
  msg = 'ERROR|' + err_msg
  send_data(socket, msg)


def send_list(socket, list):
  """
  Join the list using delimiter '|' and send data to client
  """
  msg = "|".join(list) + '\n'
  return send_data(socket, msg)


def recv_data(s):
  """
  Receive up to 4KB data into socket s and return the data
  """
  try:
    recv_buf = s.recv(4096)
  except error:
    print 'recv_data error'
  return recv_buf


def decode_data(recv_buf):
  """
  Remove trailing \r\n added and decode message to list
  :param recv_buf: Buffer of size 4KB
  :return: Received data split into list delimited by '|'
  """
  try:
    recv_buf = str(recv_buf.decode())
    if recv_buf[-2:] == '\r\n':
      recv_buf = recv_buf[:-2]
    elif recv_buf[-1:] == '\n':
      recv_buf = recv_buf[:-1]
    print recv_buf
  except UnicodeDecodeError:
    print 'Unexpected byte stream in received data'
    #TODO make sure the server does not exit.
    thread.exit()
  message = recv_buf.split("|")
  return message


def bind_to_port(s, port):
  """
  :param s: Socket to bind
  :param port: Port to bind to
  :return: True on success, False otherwise
  """
  try:
    s.bind(('', port))
  except error:
    return False
  return True


def bind_to_random(s, tries=10, start=40000, stop=50000):
  """
  Try to bind to random port from start to stop port numbers, tries number of times.
  :param tries:
  :param start:
  :param stop:
  """
  while tries > 0:
    port = random.randint(start, stop-1)
    tries = -1 if bind_to_port(s, port) else tries - 1
  if tries is 0:
    print "Couldn't bind to data port. Aborting..."
    sys.exit()
  return port
