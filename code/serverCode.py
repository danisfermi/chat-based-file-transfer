#! /usr/bin/python

import library


class Server(object):

  def __init__(self):
    self.s = socket(AF_INET, SOCK_STREAM)
    self.sockets = []

  def go_online(self, tries=10, start=20000):
    flag = False

    # Bind to a connection port from start to start+tries-1.
    for listen_port in xrange(start, start+tries-1):
      if library.bind_to_port(self.s, listen_port):
        flag = True
        break

    if not flag:
      print "Couldn't bind to connection port. Aborting..."
      sys.exit()

    self.s.listen(25)
    print 'Server is listening'
    # data_port = library.bind_to_random(tries)  # bind to a random port for data
    return listen_port  # , data_port

  def client_thread(self):
    return False

  def execute(self):
    self.go_online()
    while 1:
      ds, addr = self.s.accept()
      self.sockets.append((ds, addr))
      print 'Incoming connection from', addr
      thread.start_new_thread(self.client_thread(), ())


s1 = Server()
s1.execute()
