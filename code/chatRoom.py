#! /usr/bin/python

from library import *
from socket import *
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)


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

