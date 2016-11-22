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
    self.listen_port = 0
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
        if not client.suspended and client.username is username:
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
      flag = False
      if source:
        msg = '#' + source + '|' + msg
      for i in xrange(len(self.clients)):
        client_id = self.clients[i].client_id
        clients = self.server.clients
        if clients[client_id].name is not source:
          send_data(clients[client_id].socket, msg)
        else:
          flag = True
      if not flag:
        sys.exit('Source client not in chatroom client list')

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
      # TODO: Client ID cant be used to index clients array if previous clients have exitted.
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
      self.accept_login()
      while not self.suspended:
        self.accept_message()

    def accept_login(self):
      """
      Establish the clients username and create a new chatroom, or add it to an existing one.
      """
      self.check_username()
      self.check_chatroom()

    # def check_tries(self, tries, func, err_msg):
    #   """
    #   Function that repeats a func method if there are enough tries left.
    #   :param tries: Number of tries left
    #   :param func: Method to be repeated in case of an incoherent message.
    #   :param err_msg: Error message to be displayed, if there are tries left.
    #   """
    #   logging.info('Check_tries')
    #   if tries > 0:
    #     send_err(self.socket, err_msg)
    #     func(tries - 1)
    #   else:
    #     send_err(self.socket, 'Max tries reached, closing connection.')
    #     self.suspended = True

    def check_username(self, tries=5):
      """
      Try tries number of times to get a unique username from client.
      """
      logging.info('Check_username')
      msg = decode_data(recv_data(self.socket))
      name = msg[0]
      usernames = [i.username for i in self.server.clients]
      if name in usernames:
        if tries > 0:
          send_err(self.socket, 'Username taken, kindly choose another.')
          self.check_username(tries - 1)
        else:
          send_err(self.socket, 'Max tries reached, closing connection.')
          self.suspended = True
      else:
        self.username = name
        send_ok(self.socket, 'Username ' + name + ' accepted. Send create/join a chatroom')
      return

    def check_chatroom(self, tries=5):
      """
      Check if client wants to create a new chatroom or join an existing one.
      """
      logging.info('Check_chatroom')
      if self.suspended:
        return
      msg = decode_data(recv_data(self.socket))
      option = str(msg[0]).lower()
      if option == 'create':  # Create chatroom - check chatroom name
        send_ok(self.socket, 'Specify a chatroom name to create.')
        self.create_chatroom()
      elif option == 'join':  # Join existing chatroom - Send list of availables.
        if len(self.server.chatrooms):
          send_ok(self.socket, 'Here is a list of chatrooms you can join.')
          send_list(self.socket, self.server.chatrooms)
          self.join_chatroom()
        else:  # There are no chatrooms to join
          if tries > 0:
            send_err(self.socket, 'There are no chatrooms to join now')
            self.check_chatroom(tries - 1)
          else:
            send_err(self.socket, 'Max tries reached, closing connection.')
            self.suspended = True
      else:
        if tries > 0:
          send_err(self.socket, 'Sorry, specify join/create to join or create a chatroom')
          self.check_chatroom(tries - 1)
        else:
          send_err(self.socket, 'Max tries reached, closing connection.')
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
          send_err(self.socket, 'Sorry, chatroom already taken. Please try again.')
          self.create_chatroom(tries - 1)
        else:
          send_err(self.socket, 'Max tries reached, closing connection.')
          self.suspended = True
      else:
        new_room = self.server.ChatRoom(self.server, name, self.client_id)
        self.server.chatrooms.append(new_room)
        self.chatroom = new_room
        send_ok(self.socket, 'Chatroom ' + name + ' created.')

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
          room.broadcast('INFO| New user ' + self.username + ' has joined', 'Server')
          room.clients.append(self.client_id)
          self.chatroom = room
          send_ok(self.socket, 'You have joined chatroom - ' + name)
          send_data(self.socket, 'Here is a list of peers in the room:')
          send_list(self.socket, self.chatroom.get_usernames())
          return
      if tries > 0:
        send_err(self.socket, 'Sorry, chatroom name not found. Please try again.')
        self.join_chatroom(tries - 1)
      else:
        send_err(self.socket, 'Max tries reached, closing connection.')
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
      if destination[:1] is not '@':
        send_err(self.socket, 'Sorry, first field in message should be @<destination>')
        return
      destination = destination[1:]
      print destination
      msg[0] = '#' + self.username
      if destination is 'all':
        # TODO: Make sure 'all', 'server' is not a valid username
        self.chatroom.broadcast_msg('|'.join(msg))
      elif destination is 'server':
        # TODO: This piece of code may need more features
        if msg[1].lower() is 'exit' or 'quit':
          self.suspended = True
      else:
        dest_client = self.chatroom.get_client(destination)
        if dest_client is None:
          send_err(self.socket, 'Sorry, destination client not present in chatroom')
        else:
          send_list(dest_client.socket, msg)


  # Server class functions follow

  def go_online(self, start=20000, tries=10):
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
    self.listen_port = listen_port

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
      thread.start_new_thread(client.execute())


s1 = Server()
s1.execute()
