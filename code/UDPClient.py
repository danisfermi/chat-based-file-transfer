#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging


logging.basicConfig(filename='server.log', level=logging.DEBUG)


class UDPClient(object):
    """
    """
    def __init__(self, parent, msg):
        self.parent = parent
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.suspended = False
        self.cport
        
    def connect(self, sip, sport)
        """
        Connect to server ip and port from a random client port cport = random.randrange(something)
        Save c-port in self. Bind to cport and connect to server.
        """
        
    def transfer(self, filename)
        """
        Transfer the filename in our folder/filename to the server.
        """
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.suspended = False
    #    self.cport = 0
        self.sip = null
        self.sport = 0
        
    # def connect(self, sip, sport)
    #     """
    #     Connect to server ip and port from a random client port cport = random.randrange(something)
    #     Save c-port in self. Bind to cport and connect to server.
    #     """
    #     self.cport = random.randrange(20000,50000,10) 
    #     self.socket.bind(('', self.cport))
    #     self.socket.connect((sip, sport))
    def send_pkt(self, msg)
        """
        Send msg to socket. Receive an ACK from other side that has format #FROM|(N)ACK
        retry send if NACK, else return.
        """
        self.socket.sendto(msg, (sip, sport))
        msg_list = client_recv(self.socket)
        while msg_list[2] == 'NACK' :
            self.socket.sendto(msg, (sip, sport))
            msg_list = client_recv(self.socket)    
        
    def transfer(self, filename):
        """
        Transfer the filename in our folder/filename to the server.
        """
        #TODO::take buffer size from an ip
        buff = 4096
        f = open(filename)
        msg = f.read(buff)
        while msg:
            send_pkt(msg)
            msg = f.read(buff)
        f.close()

    
    def execute(self, msg, msg):
        """
        Comes here when a file is requested.
        Msg from UDPServer is in format: #FROM|getfile|filename|udpserver_IP|udpserver_port
        """
        self.connect(msg[3], int(msg[4]))
        self.transfer(msg[2])