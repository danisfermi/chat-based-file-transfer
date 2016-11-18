Client:

  * Contact server 1/ server 2 whose IPs are hard-coded.
  * Login to a application -
    * Option 1 - Create a chatroom:
      * Send username, specify chatroom name
      * Get chatroom ID, and confirmation whether chatroom name was accepted. Else, loop till 10 retries.
    * Option 2 - Join a chatroom:
      * Send username, specify join
      * Get comma separated list of chatrooms
