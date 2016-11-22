#! /usr/bin/python

from library import *
from socket import *


class Server(object):

  def __init__(self):
    self.s = socket(AF_INET, SOCK_STREAM)
    self.clients = []
    self.chatrooms = []

  class ChatRoom(object):
    """
    Class object for holding chatroom specific info
    """

    def __init__(self, server_reference, name, client_id):
      """

      :param server_reference:
      :param name:
      :param id:
      :param client:
      """
      self.server = server_reference
      self.name = name
      self.id = len(server_reference.chatrooms)
      self.clients = [client_id]

    def broadcast(self, msg, source=None):
      if source:
        msg = 'FROM:' + source + '|' + msg
      for i in xrange(len(self.clients)):
        client_id = self.clients[i].client_id
        socket = self.server.clients[client_id].socket
        send_data(socket, msg)

  class ClientNode(object):
    """
    Class object for holding client related information
    """

    def __init__(self, server_reference, ip, socket, client_id):
      """

      :param ip:
      :param socket:
      :param client_id:
      """
      self.server = server_reference
      self.ip = ip
      self.socket = socket
      self.client_id = client_id
      self.username = None
      self.suspended = False
      self.chatroom_admin = False

    def accept_login(self):
      self.check_username()
      self.check_chatroom()

    def check_username(self, tries=5):
      """
      Try tries number of times to get a unique username from client.
      :param client_id:
      :param tries:
      :return: login message from client
      """
      msg = decode_data(recv_data(self.socket))
      name = msg[0]
      usernames = [i.username for i in self.clients]
      if name in usernames:
        if tries > 0:
          send_err(self.socket, 'Username already taken, kindly choose another.')
          self.check_username(tries-1)
        else:
          send_err(self.socket, 'Max tries for unique username reached, closing connection.')
          self.suspended = True
      else:
        self.username = name
        send_ok(self.socket, 'Username ' + name + ' accepted. Send create/join a chatroom')
      return

    def check_chatroom(self, tries=5):
      if self.suspended
        return
      msg = decode_data(recv_data(self.socket))
      option = msg[0].tolower()
      if option == 'create':  # Create chatroom - check chatroom name
        send_ok(self.socket, 'Specify a chatroom name to create.')
        self.create_chatroom()
      elif option == 'join':  # Join existing chatroom - Send list of availables.
        send_ok(self.socket, 'Here is a list of chatrooms you can join.')
        send_list(self.socket, self.chatrooms)
        self.join_chatroom()
      else:
        if tries > 0:
          send_err(self.socket, 'Sorry, specify join/create to join or create a chatroom')
          self.check_chatroom(tries-1)
        else:
          send_err(self.socket, 'Sorry, max tries exceeded. Aborting.')
          self.suspended = True

    def create_chatroom(self, tries=5):
      # Create chatroom, send OK to client. Inform other clients/servers.
      if self.suspended:
        return
      msg = decode_data(recv_data(self.socket))
      name, names = msg[0], [i.name for i in self.server.chatrooms]
      if name in names:
        if tries > 0:
          send_err(self.socket, 'Sorry, chatroom name already taken. Please try again.')
          self.create_chatroom(tries - 1)
        else:
          send_err(self.socket, 'Sorry, max tries exceeded. Aborting.')
          self.suspended = True
      else:
        new_room = ChatRoom(self.server, name, self.client_id)
        self.server.chatrooms.append(new_room)
        send_ok(self.socket, 'Chatroom ' + name + ' created.')


    def join_chatroom(self, tries=5):
      if self.suspended
        return
      msg = decode_data(recv_data(self.socket))
      name = msg[0]
      for room in self.server.chatrooms:
        if name == room.name:
          room.broadcast('INFO| New user ' + self.username + ' has joined', 'Server')                      )
          room.clients.append(self.client_id)
          send_ok(self.socket, 'You have joined chatroom - ' + name)
          return

      if tries > 0:
        send_err(self.socket, 'Sorry, chatroom name not found. Please try again.')
        self.join_chatroom(tries - 1)
      else:
        send_err(self.socket, 'Sorry, max tries exceeded. Aborting.')
        self.suspended = True

    def execute(self):
      self.accept_login()
      while not self.suspended:
      # TODO
      return False


  # Server class functions follow

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

  def execute(self):
    self.go_online()
    while True:
      ds, addr = self.s.accept()
      client = ClientNode(self, addr, ds, len(self.clients))
      self.clients.append(client)
      print 'Incoming connection from', addr
      thread.start_new_thread(client.execute())


s1 = Server()
s1.execute()
