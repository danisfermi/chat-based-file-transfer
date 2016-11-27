#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
from clientNode import *
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
    self.clients = {}
    self.chatrooms = {}

  # Server class functions follow

  def remove_client(self, username):
    """
    Remove username from dictionary of clients.
    """
    try:
      self.clients.pop(username)
    except KeyError:
      print 'Client not in server.clients{}'

  def get_chatrooms(self):
    """
    Return a list of chatroom names.
    """
    return list(self.chatrooms)

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
      client = ClientNode(self, addr, ds)
      # self.clients.append(client)  # Now happens after username is verified in clientNode.py
      print 'Incoming connection from', addr
      empty_tuple = ()
      thread.start_new_thread(client.execute, empty_tuple)


s1 = Server()
s1.execute()
