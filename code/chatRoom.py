#! /usr/bin/python

from library import *
from socket import *


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
    self.server = server_reference
    self.name = name
    self.clients = [username]
    self.password = password

  def get_password(self):
    """
    Return the password for this chatroom.
    """
    return self.password

  def remove_client(self, username):
    """
    Remove username from list of usernames in chatroom
    """
    try:
      self.clients.remove(username)
    except ValueError:
      print 'Client not in chatroom.clients[]'

  def get_client(self, username):
    """
    Method to verify if a given client is a part of the chatroom
    :param username:
    :return: pointer to the client object if found in chatroom, else - None.
    """
    # Do not access server dictionary directly since this would bypass checking chatroom if username is a member.
    for name in self.clients:
      client = self.server.clients.get(name, None)
      if client is not None and not client.suspended and name == username:
        return client
    return None

  def get_usernames(self):
    """
    Returns a list of all active client usernames in chatroom
    """
    return self.clients

  def broadcast(self, msg, source=None):
    """
    Function to broadcast a message from some source to all other clients in chatroom
    :param msg: Raw message to be sent
    :param source: Add a from source field to message and send to all other clients
    """
    if source is None:
      for name in self.clients:
        client = self.server.clients.get(name, None)
        if client:
          send_data(client.socket, msg)
        else:
          print 'Client not present in server.clients{}'
    else:
      for name in self.clients:
        if source != name:
          client = self.server.clients.get(name, None)
          if client:
            send_data(client.socket, msg)
          else:
            print 'Client not present in server.clients{}'
