#! /usr/bin/python

from library import *
from socket import *
from chatRoom import *
import logging
import random
MAX_SIZE = 16
import os
logging.basicConfig(filename='server.log', level=logging.DEBUG)


class UDPClient(object):
  """
  """

  def __init__(self, parent, msg, s, cp):
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
    self.socket.sendto(msg.encode(), (self.sip, self.sport))

  def udp_recv(self, size=2048):
    msg, saddr = self.socket.recvfrom(size)
    # try:
    #   msg = msg
    # except TypeError:
    #   try:
    #     msg = msg.encode('utf-8')
    #   except UnicodeDecodeError:
    #     try:
    #       msg = msg.encode('latin-1')
    #     except TypeError:
    #       self.suspended = True
    #       return
    msg = str(msg)
    # if msg[-1:] == '\n':
    #   msg = msg[:-1]
    # print msg
    return msg

  def write_filename(self, filename):
    if self.parent.check_file(filename):
      return self.write_filename('1' + filename)
    else:
      return filename

  def execute(self):
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
    while not self.suspended:
      msg = self.udp_recv()
      #self.udp_send('ACK')
      if msg[:3] == 'EOF':
        self.suspended = True
        for i in self.buffered_msgs:
           f.write(i)
        f.close()
        print "Client all close"
      elif msg[:3] == 'END':
        neg_ack = 0
      else:
        msg = msg.split("|*)")
        self.count = random.randint(1,100)
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
          self.seqNo %= MAX_SIZE
          continue
        elif msg[0]== str(self.seqNo):
          ack = msg[0]+'|'+'ACK'
          if random.randint(1,1000)>500 or self.seqNo ==MAX_SIZE-1 or neg_ack:
            self.udp_send(ack)
            #print " client ack %s" %msg[0]
            self.prev_ack = (self.seqNo+1)%MAX_SIZE -1
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
          self.seqNo %= MAX_SIZE
        else:
          #print "GBN ERRORRRRRRRRRRRRR"
          self.udp_send(str(self.prev_ack)+'|ACK')
          #print " client ack %d" %self.prev_ack
          
          #self.suspended = True
          #f.close()
        # print msg
        #os.rename('folder/' + new_name, 'folder' + self.filename)
        # print "Client all close"
