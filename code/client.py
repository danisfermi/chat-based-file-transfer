#! /usr/bin/python
from library import *
from udpclient import *
from udpserver import *
import fnmatch
import os
import getopt
import threading


class Client(object):
  """
  Class object that stores peer information
  """
  def __init__(self, start=50000, tries=10):
    """
    Connect to server: Server uses some port between 50000 and 50009
    """
    self.socket = socket(AF_INET, SOCK_STREAM)
    self.suspended = False
    self.pport = bind_to_random(self.socket)
    self.ip = gethostbyname(gethostname())
    self.N = 16
    self.Err = 100
    self.file_share = dict()
    for filename in os.listdir('folder'):
      self.file_share[filename] = True
    self.global_share = True
    self.max_share_count = 2
    self.iplist = ['0.0.0.0', '127.0.0.1']  # 2 server IP's to be added here
    self.portlist = [i for i in xrange(start, start+tries-1)]
    self.max_conn_lock = threading.Lock()
    self.get_args()
    self.conn_left = self.max_share_count  # Counter to increment decrement inside locked code.

    #  Try connecting to server IPs in iplist at port numbers in portlist. Exit on failure.
    for ip in self.iplist:
      for port in self.portlist:
        try:
          self.socket.connect((ip, port))
          return
        except error:
          self.socket.close()
          self.socket = socket(AF_INET, SOCK_STREAM)
    sys.exit('Cannot connect to server')

  def get_args(self):
    try:
      opts, args = getopt.getopt(sys.argv[1:], "hs:p:w:e:", ["help", "share=", 'parallel=', 'ip=', 'port=', 'window=','errprob'])
    except getopt.GetoptError as err:
      # print help information and exit:
      print str(err)  # will print something like "option -a not recognized"
      self.usage()
      sys.exit(2)

    for opt, arg in opts:
      if opt in ("-h", "--help"):
        self.usage()
        sys.exit()
      elif opt in ("-s", "--share"):
        self.set_global_share(int(arg))
      elif opt in ("-p", "--parallel"):
        self.max_share_count = int(arg)
      elif opt in "--window":
        self.N = int(arg)
      elif opt in "--errprob":
        self.Err = int(arg)
      elif opt in "--ip":
        self.iplist = [arg] + self.iplist
      elif opt in "--port":
        self.portlist.append(int(arg))
      else:
        self.usage()
        sys.exit()

  def usage(self):
    """
    Print the help message
    """
    print "Welcome to Chat Based File Transfer Client..."
    print "Please use the following options while running:"
    print "-h  --help: For printing this message"
    print "-s  --share: Followed by integer 0 or 1 to clear or set global file share"
    print "-p  --parallel: Followed by integer to restrict number of parallel file shares. Not configurable in run-time"
    print "--ip: Specify the server IP address to connect to"
    print "--port: Specify the server port # to connect to. Default: 50000 to 50009"
    print "-w  --window: Followed by integer select window size N for Go-Back-N protocol"
    return

  def set_global_share(self, boolean):
    """
    Configure global share to the boolean input
    """
    try:
      self.global_share = bool(boolean)
    except ValueError:
      print "Cant set global share to a non integer value"
    enabled = 'enabled' if boolean else 'disabled'
    print 'Sharing ' + enabled

  def set_share(self, filename, boolean):
    """
    Mark the filename as share enabled/disabled
    :param filename: File name for which to set share enable/disable
    :param boolean: Boolean for enable/disable
    """
    self.sync_file_folder()
    if not filename not in list(self.file_share):
      print "File " + filename + " not found in folder"
    else:
      self.file_share[filename] = boolean
      enabled = 'enabled' if boolean else 'disabled'
      print 'Sharing ' + enabled + ' on file ' + filename

  def sync_file_folder(self):
    """
    Keep file_share dictionary in sync with files that are actually there in folder.
    """
    actual_file_list = os.listdir('folder')
    stored_file_list = list(self.file_share)
    new_files = list(set(actual_file_list) - set(stored_file_list))
    old_files = list(set(stored_file_list) - set(actual_file_list))
    for new_file in new_files:
      self.file_share[new_file] = True
    for old_file in old_files:
      del self.file_share[old_file]

  def check_file(self, filename):
    """
    iterate over file-folder and check if the filename is available.
    Availability is also dependent on whether its share variable and global share variable are both set.
    """
    self.sync_file_folder()
    for file in os.listdir('folder'):
      share = self.file_share.get(file, None)
      if fnmatch.fnmatch(file, filename):
        return share and self.global_share
    return False

  def get_share_status(self):
    """
    Print the global share status and file specific share statuses.
    """
    self.sync_file_folder()
    print 'Global share status: ', self.global_share
    print 'File share status:'
    print self.file_share
    
  def set_window_size(self, N):
    """
    Set the window size used by Go Back N protocol to 'N'
    """
    self.N = N

  def handle_user_commands(self, instr, arg=None):
    """
    Check instr for user commands and call the required functions
    """
    if instr == 'setshare':
      self.set_share(arg, True)
    elif instr == 'clrshare':
      self.set_share(arg, False)
    elif instr == 'setglobalshare':
      self.set_global_share(True)
    elif instr == 'clrglobalshare':
      self.set_global_share(False)
    elif instr == 'getsharestatus':
      self.get_share_status()
    elif instr == 'setwindowsize':
      self.set_window_size(int(arg))

  def handle_exit_commands(self, msg):
    """
    Handle exit/quit and kill commands received from server.
    """
    if msg[0].lower() in ['exit', 'quit']:
      print "Thank You for using our chatroom. Press enter to continue."
      self.suspended = True
    elif msg[0].lower() in ['kill']:
      print "Server has suspended operation. Thank You for using our chatroom. Press enter to continue."
      client_send(self.socket, '@server|exit')
      self.suspended = True

  def listen_to_server(self):
    """
    Until client is suspended, keep listening to messages from server and perform necessary actions.
    Server commands to handle include: ['kill', 'exit', 'quit', 'whohas', 'getfile',
    'setshare', 'clrshare', 'setglobalshare', 'clrglobalshare', 'getsharestatus']
    """
    while not self.suspended:
      msg = client_recv(self.socket)
      self.handle_exit_commands(msg)
      if not self.suspended and len(msg) > 1:
        if msg[1].lower() in ['whohas', 'getfile', 'setshare', 'clrshare'] and len(msg) < 3:
          client_send(self.socket, '@' + msg[0][1:] + '|ERROR: Please specify filename')
          continue
        if msg[1].lower() in ['whohas'] and self.check_file(msg[2]):
          client_send(self.socket, '@' + msg[0][1:] + '|ME')
        elif msg[1].lower() in ['getfile']:
          msg += client_recv(self.socket)[1:]  # add cip and cport sent from client
          udpserver = UDPServer(self, msg)
          empty_tuple = ()
          thread.start_new_thread(udpserver.execute, empty_tuple)
        elif msg[0].lower() == '#me':
          arg = None if len(msg) < 3 else msg[2].lower()
          self.handle_user_commands(msg[1].lower(), arg)

  def listen_to_user(self):
    """
    Until client is suspended, keep listening to inputs from user and forward the message to the server.
    Also, on sensing a 'getfile' input, send IP and port details to destination, and start a udpclient thread.
    """
    while not self.suspended:
      user_input = raw_input()
      client_send(self.socket, user_input)
      user_input = user_input.rstrip('\n')
      user_input = user_input.split("|")
      if len(user_input) > 2 and user_input[1] == 'getfile':
        s = socket(AF_INET, SOCK_DGRAM)
        cp = bind_to_random(s)
        client_send(self.socket, '|'.join([user_input[0], str(self.ip), str(cp)]))
        empty_tuple = ()
        udpclient = UDPClient(self, user_input, s, cp)
        thread.start_new_thread(udpclient.execute, empty_tuple)

  def execute(self):
    """
    Keep listening to messages from server and inputs from user in parallel. Exit when suspended.
    """
    empty_tuple = ()
    thread.start_new_thread(self.listen_to_server, empty_tuple)
    self.listen_to_user()
    self.socket.close()


c1 = Client()
c1.execute()
