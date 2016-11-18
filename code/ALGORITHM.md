Client:

  * Contact tier-1 server-1/server-2 whose IPs are hard-coded.
    * Have a list of 2 servers and maybe pre-defined 10 IPs where servers can listen. Iterate over all 20 combinations to try for a connection.
  * Get IP and port number of server to connect to. // Not implemented now
  * Login to that server - // Not implemented now. Login to any tier-1 server and connect to a chat room
    * Option 1 - Create a chatroom:
      * Send username, specify new chatroom name
      * Get chatroom ID, and confirmation whether chatroom name was accepted. Else, loop till 10 retries.
    * Option 2 - Join a chatroom:
      * Send username, specify join
      * Get comma separated list of chatrooms

Server (Tier-1):

  * Bind to and listen on one of the 10 pre-defined ports for connections and one random port for data.
  * Fork into two
  * One part - Listen to new incoming connections.
    * Accept connections from new clients, reply with its own IP, and data port number.
    * Later - Need to tell client to connect to its closest server instead.
  * Second part - Listen to data 
    * Accept message
      * Server is destination: (New login) - 
        * Get username, join/new-chatroom-name
        * Reply with chatroom ID (confirmation) or supply list of chatroom IDs to join to.
      * Client is destination: 
        * forward to relevant client(s).
     
