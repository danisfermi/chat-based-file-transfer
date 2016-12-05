#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *



class ClientNode(object):
  """
  Class object for holding client related information
  """

  def __init__(self, server_reference, ip, socket):
    """
    :param ip: IP address of client.
    :param socket: Socket at server used to communicate with client.
    """
    self.server = server_reference
    self.ip = ip
    self.socket = socket
    self.username = None
    self.suspended = False
    self.chatroom = None

  def execute(self):
    """
    This is the main per-client execution thread for the server.
    Enable a client to login and proceed to listen to, and forward, its messages.
    """
    msg = 'Connected to ' + self.server.ip + ' at port ' + str(self.server.port)
    msg += '\nPlease enter your username\n'
    send_data(self.socket, msg)
    self.accept_login()
    if not self.suspended:
      msg = 'Welcome to ' + self.chatroom.name + '. You are all set to pass messages\n'
      send_data(self.socket, msg)
    while not self.suspended:
      self.accept_message()
    if not self.server.suspended:
      send_data(self.socket, 'exit')
      if self.chatroom is not None:
        self.chatroom.broadcast('INFO| User ' + self.username + ' has left\n', self.username)
        self.chatroom.remove_client(self.username)
      self.server.remove_client(self.username)
    self.socket.close()

  def accept_login(self):
    """
    Establish the clients username and create a new chatroom, or add it to an existing one.
    """
    self.check_username()
    self.create_or_join()

  def check_username(self, tries=5):
    """
    Try tries number of times to get a unique username from client.
    """
    msg = decode_data(recv_data(self.socket))
    name = msg[0]
    if name in list(self.server.clients) + ['server', 'all', 'root', 'me']:  # invalid usernames
      if tries > 0:
        send_err(self.socket, 'Username taken, kindly choose another.\n')
        self.check_username(tries - 1)
      else:
        send_err(self.socket, 'Max tries reached, closing connection.\n')
        self.suspended = True
    else:
      self.username = name
      self.server.clients[self.username] = self  # Add to dictionary in server.
      send_ok(self.socket, 'Username ' + name + ' accepted. Send create/join a chatroom\n')
    return

  def create_or_join(self, tries=5):
    """
    Check if client wants to create a new chatroom or join an existing one.
    """
    # logging.info('create_or_join')
    if self.suspended:
      return
    msg = decode_data(recv_data(self.socket))
    option = str(msg[0]).lower()
    if option == 'create':  # Create chatroom - check chatroom name
      send_ok(self.socket, 'Specify a chatroom name to create.\n')
      self.create_chatroom()
    elif option == 'join':  # Join existing chatroom - Send list of available peers.
      if len(self.server.chatrooms):
        send_ok(self.socket, 'Here is a list of chatrooms you can join.\n')
        send_list(self.socket, self.server.get_chatrooms())
        self.join_chatroom()
      else:  # There are no chatrooms to join
        if tries > 0:
          send_err(self.socket, 'There are no chatrooms to join now\n')
          self.create_or_join(tries - 1)
        else:
          send_err(self.socket, 'Max tries reached, closing connection.\n')
          self.suspended = True
    else:
      if tries > 0:
        send_err(self.socket, 'Sorry, specify join/create to join or create a chatroom\n')
        self.create_or_join(tries - 1)
      else:
        send_err(self.socket, 'Max tries reached, closing connection.\n')
        self.suspended = True

  def create_chatroom(self, tries=5):
    """
    Create chatroom - Add client as first user of room when a unique name is received
    :param tries: Retry 'tries' number of times to get a unique chatroom name.
    """
    # logging.info('Create_chatroom')
    if self.suspended:
      return
    msg = decode_data(recv_data(self.socket))
    name, names = msg[0], list(self.server.chatrooms)
    if name in names:
      if tries > 0:
        send_err(self.socket, 'Sorry, chatroom already taken. Please try again.\n')
        self.create_chatroom(tries - 1)
      else:
        send_err(self.socket, 'Max tries reached, closing connection.\n')
        self.suspended = True
    else:
      send_ok(self.socket, 'Chatroom ' + name + ' created. Do you want to password protect the room? [yes/no]\n')
      self.passwd_protect_chatroom(name)

  def passwd_protect_chatroom(self, room_name, tries=5):
    """

    :param room_name: Name of chatroom being joined.
    :param tries:
    :return:
    """
    if self.suspended:
      return
    msg = decode_data(recv_data(self.socket))
    if msg[0][:3].lower() == 'yes':
      send_ok(self.socket, 'Please enter password.\n')
      msg = decode_data(recv_data(self.socket))
      send_ok(self.socket, 'Password ' + msg[0] + ' accepted.\n')
      new_room = ChatRoom(self.server, room_name, self.username, msg[0])
    else:
      send_ok(self.socket, 'Chatroom has been made public.\n')
      new_room = ChatRoom(self.server, room_name, self.username)
    self.server.chatrooms[room_name] = new_room
    self.chatroom = new_room

  def join_chatroom(self, tries=5):
    """
    Join chatroom - Add client to client list of room when request is received
    :param tries: Retry 'tries' number of times to get an existent chatroom name.
    """
    # logging.info('join_chatroom')
    if self.suspended:
      return
    msg = decode_data(recv_data(self.socket))
    name = msg[0]
    for room_name in list(self.server.chatrooms):
      room = self.server.chatrooms[room_name]
      if name == room_name:
        self.check_password(room)
        if self.suspended:
          return
        room.broadcast('INFO| New user ' + self.username + ' has joined\n', self.username)
        send_ok(self.socket, 'You have joined chatroom - ' + name + '\n')
        self.chatroom = room
        if len(room.clients):
          send_data(self.socket, 'Here is a list of peers in the room:\n')
          send_list(self.socket, self.chatroom.get_usernames())
        else:
          send_data(self.socket, 'There are no peers in the room:\n')
        room.clients.append(self.username)
        return
    if tries > 0:
      send_err(self.socket, 'Sorry, chatroom name not found. Please try again.\n')
      self.join_chatroom(tries - 1)
    else:
      send_err(self.socket, 'Max tries reached, closing connection.\n')
      self.suspended = True

  def check_password(self, room, tries=5):
    if room.get_password() is None:
      return
    send_ok(self.socket, 'This chatroom is private. Please enter password.\n')
    msg = decode_data(recv_data(self.socket))
    if msg[0] != room.password:
      if tries > 1:
        send_err(self.socket, 'Sorry, incorrect password. You have ' + str(tries - 1) + ' tries left.\n')
        self.check_password(room, tries - 1)
      else:
        send_err(self.socket, 'Max tries reached, closing connection.\n')
        self.suspended = True
    else:
      send_ok(self.socket, 'Password accepted.\n')

  def accept_message(self):
    """
    Check the destination field in a message and unicast it to the destination or,
    broadcast if destination is 'all'. Edit message to include source instead of destination
    Messages with destination as 'server' may be an exit or quit message.
    """
    msg = decode_data(recv_data(self.socket))
    destination = msg[0]
    if destination[:1] != '@':
      send_err(self.socket, 'Sorry, first field in message should be @<destination>\n')
      return
    destination = destination[1:]
    msg[0] = '#me' if destination in [self.username, 'me'] else '#' + self.username
    if destination == 'all':
      self.chatroom.broadcast('|'.join(msg), self.username)
    elif destination == 'server':
      if len(msg) > 1:
        if msg[1].lower() in ['exit', 'quit']:
          self.suspended = True
        elif msg[1].lower() == 'get_peers':
          send_list(self.socket, self.chatroom.get_usernames())
        elif msg[1].lower() == 'get_rooms':
          send_list(self.socket, self.server.get_chatrooms())
        elif msg[1].lower() == 'get_passwd':
          message = self.chatroom.get_password()
          if message is None:
            message = 'This chatroom is public and has no password protection.'
          send_data(self.socket, message)
        else:  # Just deliver the message to server console
          print '|'.join(msg)
    else:
      dest_client = self.chatroom.get_client(destination) if destination != 'me' else self
      if dest_client is None:
        send_err(self.socket, 'Sorry, destination client not present in chatroom\n')
      else:
        send_list(dest_client.socket, msg)
