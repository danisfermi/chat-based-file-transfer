#! /usr/bin/python

from library import *
from socket import *
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)


class Server(object):

  def __init__(self):
    """
    self.clients is a list of all client objects instantiated by the server.
    Objects are not deleted once they are disconnected, so that indexing is maintained.
    However, the client object has a self.suspended field to check if the client is active.
    """
    self.s = socket(AF_INET, SOCK_STREAM)
    self.port = 0
    self.ip = gethostbyname(gethostname())
    self.clients = []
    self.chatrooms = []
    self.client_count = 0
    self.room_count = 0

  class ChatRoom(object):
    """
    Class object for holding chatroom specific info
    """

    def __init__(self, server_reference, name, client_id):
      """
      ChatRoom ID is auto generated from server's room count history.
      :param server_reference: Pointer to server object that instantiated this class
      :param name: Chatroom name
      :param client_id: ID of client that created the room, to be added to list of clients.
      """
      self.server = server_reference
      self.name = name
      self.id = server_reference.room_count
      self.clients = [client_id]

    def get_client(self, username):
      """
      Method to verify if a given client is a part of the chatroom
      :param username:
      :return: pointer to the client object if found in chatroom, else - None.
      """
      #TODO
      for id in self.clients:
        client = self.server.clients[id]
        if not client.suspended and client.username == username:
          return client
      return None

    def get_usernames(self):
      """
      Returns a list of all active client usernames in chatroom
      """
      client_list = []
      for id in self.clients:
        client = self.server.clients[id]
        if not client.suspended:
          client_list.append(client.username)
      return client_list

    def broadcast(self, msg, source=None):
      """
      Function to broadcast a message from some source to all other clients in chatroom
      :param msg: Raw message to be sent
      :param source: Add a from source field to message and send to all other clients
      """
      # TODO: There is something wrong with this function when source is not None.
      # source_verified = True if source is None else False
      # if source:
      #   msg = '#' + source + '|' + msg
      # for client_id in self.clients:
      #   clients = self.server.clients
      #   if source == clients[client_id].username:
      #     source_verified = True
      #   else:
      #     send_data(clients[client_id].socket, msg)
      # if not source_verified:
      #   print "Good Lord, why is this error coming?"
      #   sys.exit('Source client not in chatroom client list')

      # TODO: The following code seems to be working fine,
      # TODO: but there is a sendall data error triggered by send when lone client tries to broadcast
      # TODO: This is repeated on any subsequent broadcast, but doesnt come on a unicast.
      # if self.server.
      if source is None:
        for client_id in self.clients:
          clients = self.server.clients
          send_data(clients[client_id].socket, msg)
      else:
        for client_id in self.clients:
          clients = self.server.clients
          if source != clients[client_id].username:
            send_data(clients[client_id].socket, msg)

  class ClientNode(object):
    """
    Class object for holding client related information
    """

    def __init__(self, server_reference, ip, socket, client_id):
      """

      :param ip: IP address of client.
      :param socket: Socket at server used to communicate with client.
      :param client_id:
      """
      # TODO: Client ID cant be used to index clients array if previous clients have exited.
      # TODO: User cannot exit and relogin with same username if entry not deleted.
      self.server = server_reference
      self.ip = ip
      self.socket = socket
      self.client_id = client_id
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
      self.chatroom.clients.remove(self.client_id)
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
      logging.info('Check_username')
      msg = decode_data(recv_data(self.socket))
      name = msg[0]
      usernames = [i.username for i in self.server.clients]
      if name in usernames + ['server', 'all']:  # 'all', 'server' not valid usernames
        if tries > 0:
          send_err(self.socket, 'Username taken, kindly choose another.\n')
          self.check_username(tries - 1)
        else:
          send_err(self.socket, 'Max tries reached, closing connection.\n')
          self.suspended = True
      else:
        self.username = name
        send_ok(self.socket, 'Username ' + name + ' accepted. Send create/join a chatroom\n')
      return

    def create_or_join(self, tries=5):
      """
      Check if client wants to create a new chatroom or join an existing one.
      """
      logging.info('create_or_join')
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
      logging.info('Create_chatroom')
      if self.suspended:
        return
      msg = decode_data(recv_data(self.socket))
      name, names = msg[0], [i.name for i in self.server.chatrooms]
      if name in names:
        if tries > 0:
          send_err(self.socket, 'Sorry, chatroom already taken. Please try again.\n')
          self.create_chatroom(tries - 1)
        else:
          send_err(self.socket, 'Max tries reached, closing connection.\n')
          self.suspended = True
      else:
        new_room = self.server.ChatRoom(self.server, name, self.client_id)
        self.server.chatrooms.append(new_room)
        self.chatroom = new_room
        send_ok(self.socket, 'Chatroom ' + name + ' created.\n')

    def join_chatroom(self, tries=5):
      """
      Join chatroom - Add client to client list of room when request is received
      :param tries: Retry 'tries' number of times to get an existent chatroom name.
      """
      logging.info('join_chatroom')
      if self.suspended:
        return
      msg = decode_data(recv_data(self.socket))
      name = msg[0]
      for room in self.server.chatrooms:
        if name == room.name:
          room.broadcast('INFO| New user ' + self.username + ' has joined\n', self.username)
          send_ok(self.socket, 'You have joined chatroom - ' + name + '\n')
          if len(room.clients):
            send_data(self.socket, 'Here is a list of peers in the room:\n')
            send_list(self.socket, self.chatroom.get_usernames())
          else:
            send_data(self.socket, 'There are no peers in the room:\n')
          room.clients.append(self.client_id)
          self.chatroom = room
          return
      if tries > 0:
        send_err(self.socket, 'Sorry, chatroom name not found. Please try again.\n')
        self.join_chatroom(tries - 1)
      else:
        send_err(self.socket, 'Max tries reached, closing connection.\n')
        self.suspended = True

    def accept_message(self):
      """
      Check the destination field in a message and unicast it to the destination or,
      broadcast if destination is 'all'. Edit message to include source instead of destination
      Messages with destination as 'server' may be an exit or quit message.
      """
      # TODO
      msg = decode_data(recv_data(self.socket))
      destination = msg[0]
      if destination[:1] != '@':
        send_err(self.socket, 'Sorry, first field in message should be @<destination>\n')
        return
      destination = destination[1:]
      msg[0] = '#' + self.username
      if destination == 'all':
        self.chatroom.broadcast('|'.join(msg), self.username)
      elif destination == 'server':
        # TODO: This piece of code may need more features
        if len(msg) > 1:
          if msg[1].lower() in ['exit', 'quit']:
            self.suspended = True
          elif msg[1].lower() == 'get_peers':
            send_list(self.socket, self.chatroom.get_usernames())
          elif msg[1].lower() == 'get_rooms':
            send_list(self.socket, self.server.get_chatrooms())
          else:  # Just deliver the message to server console
            print '|'.join(msg)
      else:
        dest_client = self.chatroom.get_client(destination)
        if dest_client is None:
          send_err(self.socket, 'Sorry, destination client not present in chatroom\n')
        else:
          send_list(dest_client.socket, msg)


  # Server class functions follow

  def get_chatrooms(self):
    names = []
    for c in self.chatrooms:
      names.append(c.name)
    return names

  def go_online(self, start=50000, tries=10):
    """
    Bind to a connection port and start listening on it.
    :param start: Try binding to port numbers starting at this value
    :param tries: Try binding 'tries' number of times till port = start+tries-1
    """
    flag = False
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
    self.port = listen_port

  def execute(self):
    """
    This is the main server thread. Go online and start listening for connections.
    Accept client connections and start a new client thread using its execute method.
    """
    self.go_online()
    while True:
      ds, addr = self.s.accept()
      client = self.ClientNode(self, addr, ds, self.client_count)
      self.client_count += 1
      self.clients.append(client)
      print 'Incoming connection from', addr
      empty_tuple = ()
      thread.start_new_thread(client.execute, empty_tuple)


s1 = Server()
s1.execute()
