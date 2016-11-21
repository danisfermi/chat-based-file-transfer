#! /usr/bin/python

from library import *
from socket import *


class Server(object):

  def __init__(self):
    self.s = socket(AF_INET, SOCK_STREAM)
    self.clients = []
    self.chatrooms = []

  def go_online(self, tries=10, start=20000):
    flag = False

    # Bind to a connection port from start to start+tries-1.
    for listen_port in xrange(start, start+tries-1):
      if bind_to_port(self.s, listen_port):
        flag = True
        break

    if not flag:
      print "Couldn't bind to connection port. Aborting..."
      sys.exit()

    self.s.listen(25)
    print 'Server is listening at', listen_port
    # data_port = library.bind_to_random(tries)  # bind to a random port for data
    return listen_port  # , data_port

  def check_username(self, name):
    #TODO
    usernames = [i.username for i in self.clients]
    if name in usernames:
      return True
    return False

  def create_chatroom(self, client_id):
    #TODO
    # Create chatroom, send OK to client. Inform other clients/servers.

  def add_client_to_chatroom(self, client_id, chatroom):
    #TODO
    socket = self.clients[client_id].socket
    send_ok(socket)

  def accept_login(self, client_id):
    socket = self.clients[client_id].socket
    # Get username, join/create chatroom message.
    msg = decode_data(recv_data(socket))
    self.check_username(msg[0])

    if msg[1].tolower() == 'join':  # Join existing chatroom - Send list of availables.
      send_list(socket, self.chatrooms)
      room = (decode_data(recv_data(socket)))[0]
      if room in self.chatrooms:
        self.add_client_to_chatroom(client_id, room)

    else:  # Create chatroom - check chatroom name
      self.create_chatroom(client_id)

  def client_thread(self, client_id):
    self.accept_login(client_id)
    while True:
      #TODO
    return False

  def execute(self):
    self.go_online()
    while True:
      ds, addr = self.s.accept()
      client = ClientNode(addr, ds, len(self.clients))
      self.clients.append(client)
      """
      Save client info ip, hostname and username.
      :param ip:
      :param hostname:
      :param username:
      :param port_num
      """
      print 'Incoming connection from', addr
      thread.start_new_thread(self.client_thread(), len(self.clients)-1)


s1 = Server()
s1.execute()
