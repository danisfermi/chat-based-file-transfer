#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
from time import time
import random
import os


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
    self.parent = parent
    self.socket = s
    self.udp_clientname = msg[0][1:]
    self.sip, self.sport = '', 0
    self.cip, self.cport = self.parent.ip, cp
    self.filename = msg[2]
    self.suspended = False
    self.buffered_msgs = []
    self.prev_ack = -1

  def udp_send(self, msg):
    """
    Send msg via the udp socket initialized in __init__ method.
    """
    self.socket.sendto(msg.encode(), (self.sip, self.sport))

  def udp_recv(self, size=2048):
    """
    Receive msg from the udp socket initialized in __init__ method.
    The incoming message is decoded and split to a list before bing returned.
    :param size: Max receive size
    """
    msg, saddr = self.socket.recvfrom(size)
    msg = str(msg)
    return msg

  def write_filename(self, filename):
    """
    Get filename to write to
    :param filename: File name that was requested
    :return: Modified filename to write to
    """
    if self.parent.check_file(filename):
      return self.write_filename('1' + filename)
    else:
      return filename

  def execute(self):
    """

    :return:
    """
    msg = self.udp_recv()
    if msg[:5] == 'ERROR':  # Peer rejects connection or File not found on peer
      print msg
      self.suspended = True
      return
    elif msg[:2] == 'OK':  # Save peer ip and port details, bind a port and send that
      print msg
      msg = msg.split("|")
      self.sip = msg[2]
      self.sport = int(msg[3])
      print self.sip, self.sport
    else:
      return
    new_name = self.write_filename(self.filename)
    f = open('folder/' + new_name, 'w')
    self.seqNo =0
    self.count = 0
    neg_ack = 0
    start = time()
    while not self.suspended:
      msg = self.udp_recv()
      #self.udp_send('ACK')
      if msg[:3] == 'EOF':
        self.suspended = True
        for i in self.buffered_msgs:
           f.write(i)
        stop = time()
        f.close()
        print stop, start
        print "Completed file transfer in " + str(stop - start) + " seconds."
      elif msg[:3] == 'END':
        neg_ack = 0
      else:
        msg = msg.split("|*)")
        self.count = random.randint(1,self.parent.Err)
        #print "hshshsh client  msg seq no and expected seq no %s %s" %(msg[0],self.seqNo)
        
        if self.count==3 and not neg_ack:
          self.udp_send(str(self.prev_ack)+'|ACK')
          #print " NACK client ack %d" %self.prev_ack
          self.buffered_msgs = []
          #print " client ********** NACK"
          neg_ack = 1
          msg = self.udp_recv()
          while msg[:3] != 'STA':
            #print " ********client  msg seq no and expected seq no %s %s" %(msg[0],self.seqNo)
            msg = self.udp_recv()
          self.seqNo = self.prev_ack+1
          self.seqNo %= self.parent.N
          continue
        elif msg[0]== str(self.seqNo):
          ack = msg[0]+'|'+'ACK'
          if random.randint(1,800)>500 or self.seqNo ==self.parent.N-1 or neg_ack:
            self.udp_send(ack)
            #print " client ack %s" %msg[0]
            self.prev_ack = (self.seqNo+1)%self.parent.N -1
            #write all the pending msgs
            for i in self.buffered_msgs:
              f.write(i)
            self.buffered_msgs = []
            f.write(msg[1])
          else:
            self.buffered_msgs.append(msg[1])
            
          #print "msg %s" %msg[1]
          #print " client  msg seq no and expected seq no %s %s" %(msg[0],self.seqNo)
          self.seqNo += 1
          self.seqNo %= self.parent.N
        else:
          self.udp_send(str(self.prev_ack)+'|ACK')
          self.seqNo += self.prev_ack+1
          self.seqNo %= self.parent.N
          #print " err client ack %d" %self.prev_ack
          
          #self.suspended = True
          #f.close()
        # print msg
        #os.rename('folder/' + new_name, 'folder' + self.filename)
        # print "Client all close"
