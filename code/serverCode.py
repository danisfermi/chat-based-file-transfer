#! /usr/bin/python

from library import *
from socket import *


class Server(object):

  def __init__(self):
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

    def broadcast(self, msg, source=None):
      """
      Function to broadcast a message from some source to all other clients in chatroom
      :param msg: Raw message to be sent
      :param source: Add a from source field to message and send to all other clients
      """
      flag = False
      if source:
        msg = 'FROM:' + source + '|' + msg
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
      self.chatroom_admin = False

    def execute(self):
      """
      This is the main per-client execution thread for the server.
      Enable a client to login and proceed to listen to, and forward, its messages.
      """
      self.accept_login()
      while not self.suspended:
      # TODO
      return False

    def accept_login(self):
      """
      Establish the clients username and create a new chatroom, or add it to an existing one.
      """
      self.check_username()
      self.check_chatroom()

    def check_username(self, tries=5):
      """
      Try tries number of times to get a unique username from client.
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
      """
      Check if client wants to create a new chatroom or join an existing one.
      """
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
      """
      Create chatroom - Add client as first user of room when a unique name is received
      :param tries: Retry 'tries' number of times to get a unique chatroom name.
      """
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
      """
      Join chatroom - Add client to client list of room when request is received
      :param tries: Retry 'tries' number of times to get an existent chatroom name.
      """
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
      client = ClientNode(self, addr, ds, self.client_count)
      self.client_count += 1
      self.clients.append(client)
      print 'Incoming connection from', addr
      thread.start_new_thread(client.execute())


s1 = Server()
s1.execute()
