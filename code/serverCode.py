#! /usr/bin/python

import library


def go_online(tries=10, start=20000):
  flag = False
  # Bind to a connection port from start to start+tries-1.
  for connection_port in xrange(start, start+tries-1):
    if library.bind_to_port(connection_port):
      flag = True
      break
    else:
      continue
  if not flag:
    print "Couldn't bind to connection port. Aborting..."
    sys.exit()

  data_port = library.bind_to_random(tries)  # bind to a random port for data
  return connection_port, data_port

