#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG)

class UDPServer(object):
    """
    """
    def __init__(self, host, filename):
        self.parent = self
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.suspended = False
        self.udpport = random.randrange(50000,60000) 
        self.message = filename
        self.destname = host.lstrip('@')
        
    def execute(self):
        message = "@"+self.destname+"|"+self.parent.ip+"|"+self.udpport
        clientsend(self.parent.socket,message)
        data, ip = self.socket.recvfrom(4096)
        
        
    
    

        
        