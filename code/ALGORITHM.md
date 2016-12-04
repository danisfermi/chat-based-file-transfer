```python
class ChatRoom(object):
  """
  Class object for holding chatroom specific info
  """

  def __init__(self, server_reference, name, username, password=None):
    """
    ChatRoom ID is auto generated from server's room count history.
    :param server_reference: Pointer to server object that instantiated this class
    :param name: Chatroom name
    :param username: Client that created the room, to be added to list of clients.
    """

  def get_password(self):
    """
    Return the password for this chatroom.
    """

  def remove_client(self, username):
    """
    Remove username from list of usernames in chatroom
    """

  def get_client(self, username):
    """
    Method to verify if a given client is a part of the chatroom
    :param username:
    :return: pointer to the client object if found in chatroom, else - None.
    """

  def get_usernames(self):
    """
    Returns a list of all active client usernames in chatroom
    """

  def broadcast(self, msg, source=None):
    """
    Function to broadcast a message from some source to all other clients in chatroom
    :param msg: Raw message to be sent
    :param source: Add a from source field to message and send to all other clients
    """



class Client(object):
  """
  Class object that stores peer information
  """
  def __init__(self, start=50000, tries=10):
    """
    Connect to server: Server uses some port between 50000 and 50009
    """

  def get_args(self):

  def usage(self):
    """
    Print the help message
    """

  def set_global_share(self, boolean):
    """
    Configure global share to the boolean input
    """

  def set_share(self, filename, boolean):
    """
    Mark the filename as share enabled/disabled
    :param filename: File name for which to set share enable/disable
    :param boolean: Boolean for enable/disable
    """

  def sync_file_folder(self):
    """
    Keep file_share dictionary in sync with files that are actually there in folder.
    """

  def check_file(self, filename):
    """
    iterate over file-folder and check if the filename is available.
    Availability is also dependent on whether its share variable and global share variable are both set.
    """

  def get_share_status(self):
    """
    Print the global share status and file specific share statuses.
    """
    
  def set_window_size(self, N):
    """
    Set the window size used by Go Back N protocol to 'N'
    """

  def handle_user_commands(self, instr, arg=None):
    """
    Check instr for user commands and call the required functions
    """

  def handle_exit_commands(self, msg):
    """
    Handle exit/quit and kill commands received from server.
    """

  def listen_to_server(self):
    """
    Until client is suspended, keep listening to messages from server and perform necessary actions.
    Server commands to handle include: ['kill', 'exit', 'quit', 'whohas', 'getfile',
    'setshare', 'clrshare', 'setglobalshare', 'clrglobalshare', 'getsharestatus']
    """

  def listen_to_user(self):
    """
    Until client is suspended, keep listening to inputs from user and forward the message to the server.
    Also, on sensing a 'getfile' input, send IP and port details to destination, and start a udpclient thread.
    """

  def execute(self):
    """
    Keep listening to messages from server and inputs from user in parallel. Exit when suspended.
    """


c1 = Client()
c1.execute()
 
class ClientNode(object):
  """
  Class object for holding client related information
  """

  def __init__(self, server_reference, ip, socket):
    """
    :param ip: IP address of client.
    :param socket: Socket at server used to communicate with client.
    """

  def execute(self):
    """
    This is the main per-client execution thread for the server.
    Enable a client to login and proceed to listen to, and forward, its messages.
    """

  def accept_login(self):
    """
    Establish the clients username and create a new chatroom, or add it to an existing one.
    """

  def check_username(self, tries=5):
    """
    Try tries number of times to get a unique username from client.
    """

  def create_or_join(self, tries=5):
    """
    Check if client wants to create a new chatroom or join an existing one.
    """

  def create_chatroom(self, tries=5):
    """
    Create chatroom - Add client as first user of room when a unique name is received
    :param tries: Retry 'tries' number of times to get a unique chatroom name.
    """

  def passwd_protect_chatroom(self, room_name, tries=5):
    """

    :param room_name: Name of chatroom being joined.
    :param tries:
    :return:
    """

  def join_chatroom(self, tries=5):
    """
    Join chatroom - Add client to client list of room when request is received
    :param tries: Retry 'tries' number of times to get an existent chatroom name.
    """

  def check_password(self, room, tries=5):

  def accept_message(self):
    """
    Check the destination field in a message and unicast it to the destination or,
    broadcast if destination is 'all'. Edit message to include source instead of destination
    Messages with destination as 'server' may be an exit or quit message.
    """

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


class Server(object):
  """
  Class object that stores all server related info.
  """
  def __init__(self):
    """
    self.clients is a list of all client objects instantiated by the server.
    Objects are not deleted once they are disconnected, so that indexing is maintained.
    However, the client object has a self.suspended field to check if the client is active.
    """

  def remove_client(self, username):
    """
    Remove username from dictionary of clients.
    """

  def get_chatrooms(self):
    """
    Return a list of chatroom names.
    """

  def go_online(self, start=50000, tries=10):
    """
    Bind to a connection port and start listening on it.
    :param start: Try binding to port numbers starting at this value
    :param tries: Try binding 'tries' number of times till port = start+tries-1
    """

  def broadcast(self, msg):
    """
    Send a message to all clients connected to server
    """

  def get_user_input(self):
    """
    TODO Parse user input on server and take action
    """

  def execute(self):
    """
    This is the main server thread. Go online and start listening for connections.
    Accept client connections and start a new client thread using its execute method.
    """


s1 = Server()
s1.execute()


class UDPClient(object):
  """
  Class object for client that receives a file from a peer
  """

  def __init__(self, parent, msg, s, cp):
    """
    Init method for udpserver object.
    :param parent: Pointer to the client that invoked this thread
    :param msg: Incoming message from client that requested for file
    :param s: UDP socket to receive files from
    :param cp: Client port that the socket is bound to
    """

  def udp_send(self, msg):
    """
    Send msg via the udp socket initialized in __init__ method.
    """

  def udp_recv(self, size=2048):
    """
    Receive msg from the udp socket initialized in __init__ method.
    The incoming message is decoded and split to a list before bing returned.
    :param size: Max receive size
    """

  def write_filename(self, filename):
    """
    Get filename to write to
    :param filename: File name that was requested
    :return: Modified filename to write to
    """

  def execute(self):
    """

    :return:
    """

class UDPServer(object):
  """
  Class object for client that sends a file to a peer
  """

  def __init__(self, parent, msg):
    """
    Init method for udpserver object.
    :param parent: Pointer to the client that invoked this thread
    :param msg: Incoming message from client that requested for file
    """

  def udp_send(self, msg):
    """
    Send msg via the udp socket initialized in __init__ method.
    """

  def udp_recv(self, size=2048):
    """
    Receive msg from the udp socket initialized in __init__ method.
    The incoming message is decoded and split to a list before bing returned.
    :param size: Max receive size
    """

  def execute(self):
    """
    Comes here when a file is requested.
    Msg from UDPServer is in format: #FROM|getfile|filename|udpserver_IP|udpserver_port
    """

  def connect(self):
    """
    Connect to server ip and port from a random client port cport = random.randrange(something)
    Save c-port in self. Bind to cport and connect to server.
    """

  def send_file(self):
    """

    :return:
    """
    
  def get_index(self,ack_no):
    """

    :param ack_no:
    :return:
    """
    
  def rec_ack(self,tries=10):
    """

    :param tries:
    :return:
    """

  def transfer(self):
    """
    Transfer the filename in our folder/filename to the server.
    """

  def send_pkt(self, send_msg, tries=10):
    """
    Send msg to socket. Receive an ACK from other side that has format #FROM|(N)ACK
    retry send if NACK, else return.
    """
```
