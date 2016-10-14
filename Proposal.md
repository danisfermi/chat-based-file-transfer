#Project Proposal

##Project Objectives

  * One always on server
  * Peers connect to server to get access into the chat room. We can have multiple chat rooms based on IDs too.
  * Server gives a list of peers to new peer on connection, and an update on every peer addition/switch off.
  * One-on-one messages are routed to destination via server using TCP protocol.
  * @all messages (including messages to check who has a file) are broadcast to all peers via server and responses unicasted to origin.
  * A peer who has a file can open a socket on a port and add this info to return message, so that the origin peer can connect directly to this port to do a UDP transfer for the file.
  * File transfers are UDP selective repeat based for reliability.

![alt tag](https://github.com/arjunaugustine/chat-based-file-transfer/blob/master/Screen%20Shot%202016-10-14%20at%201.07.26%20AM.png)
[](.com)
