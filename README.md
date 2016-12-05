# Chat based peer-to-peer file transfer

The following project was implemented in partial compliance to the course requirements of CSC 573 Internet Protocols course, taken in Fall 2016 at North Carloina State University under Prof. Muhammad Shahzad.


Chat based peer-to-peer file transfer application, lets users create or connect to chat rooms hosted on a central server. Users (interchangeably refered to as peers or clients), can send messages to other individual peers in the chatroom, or broadcast it to the entire chatroom, using templates defined by the application. The server parses messages and forwards them to the requested destination(s). Messages can also be sent to self or the server although this is typically to send a set of pre-defined commands to use various features. These pre-defined commands, among others, leverage the same chat interface to facilitate requesting and recieving files from their peers. All message passing happens using TCP via server, but file transfers happen directly from peer to peer via UDP protocol for better performance. The application implements Go-Back-N protocol for UDP communications for reliability.

![alt tag](https://github.com/arjunaugustine/chat-based-file-transfer/blob/master/bin/Fig%201%20System%20Functionality.png)

Figure shows how clients connect to server in the application

## Features

* Users connect to a central server, and create or join a chatroom, to send messages to peers in the room or to receive and transfer files.
* Chatrooms can be private, that enforce password based authentication for access, or public, where other users can freely join. This option is chosen while creating the chatroom, and a password is requested from the creator if private is chosen.
* A unique username is required of each client while logging in. Messages are directed at these usernames.
* After login, the user is presented with a list of usernames of active peers in the chatroom. The server also notifies when peers join or leave a chatroom. And in addition, the user can ask the server to provide a list of all active users in that chatroom. 
* Message fields are delimited using an '|' symbol. A message from 'bob' in the format '@alice|Hello!' gets directed to alice. The server replaces '@\<destination username>' field in the message with source username in format '#\<source username>'. Alice gets the message as '#bob|Hello'. Bob gets an error message from server if Alice was not found in the chatroom.
* A message with '@all' in place of username becomes a broadcast message and '@server' in place of username gets directed to the server. '@me' messages get routed back to self.
* The server can kill misbehaving clients, pull down chat rooms, or send info messages to individual or all clients.
* Users can disable or enable file sharing for all files altogether, or individual files, either using command line arguments, or at run-time, using '@me' messages followed by proper commands.
* Clients can use an '@all' message with 'whohas' command to check which users have a particular file. All receipients who have the requested file which is share-enabled will respond automatically.
* The client can then choose from a list of responders, to initiate a file transfer using 'getfile' command directed at the selected responder. We have tested a variety of file formats including pdf, txt, mp3, jpg etc.
* The client that received a file prints the file transfer time onto its console automatically.
* A user can restrict the number of parallel outgoing file transfers, after which, further requests will be blocked.
* All operations happen in parallel. No message passing or file sharing tasks block normal use of other features.
* Go-back-N protocol is implemented, with the user having the freedom to configure window sizes during run time. This enables us to test various timing parameter by varying the window size and testing for various file formats.
Detailed description on how to go about utilizing these features is present in [code/README.md](code/README.md)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python 2.7 to run the application.
 
```
wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar -xzf Python-2.7.11.tgz  
cd Python-2.7.11
./configure  
make  
sudo make install 
```

### Installing

####Using Github

```
git clone git@github.com:arjunaugustine/chat-based-file-transfer.git
```

### How to use it

Refer to [code/README.md](code/README.md)


## Results

We have implemented all features planned in the [project proposal](Proposal.md) except for multi-server, multi-hop support. Over and above those mentioned in the proposal, we have also implemented private chatrooms, server console to send messages or kill client connections, support to control file sharing using a global and individual file disables, variable window length for Go-Back-N protocol, among others.


Here is a test result we performed to check the effect of varying window size on throughput.
We run server on the server PC using the terminal as sudo ./server.py.
Then in the clients, we run the client code as sudo ./client.py -w 16 -p 100.
The clients connect to the server. They enter their usernames and choose to connect to the chat room named chatroom chatroom.
Once inside, we send some messages and request a file. We verify that the file has been successfully transferred to our folder.

| Window Size   | File Size     | Time Taken    | Throughput    |
|:-------------:|:-------------:|:-------------:|:-------------:|
| 16            | 21.76 MB      | 20.92 sec     | 1.04 MBps     |
| 32            | 21.76 MB      | 19.42 sec     | 1.12 MBps     |

## Future Work

This is a simple, albeit complete implementation of a chat based file transfer application. It has so much potential for enhancements and integration with additional features. Some of these features we expect to add in the near future include:-
* NAT Traversal: The ability to detect servers who are connected behind NATs. Our current application requires every device to be in the same network. We can overcome this limitation by using NAT traversal (universal plug-and-play).
* Multi-hop, Multi Server: Multiple tier-2 servers can connect to a root server and each other to reduce load on a single server and support more clients. Users connect to the closest server indicated by the root server, and chatrooms are created on the server to which the creator is attached. Clients on other servers can connect to these chatrooms as well, and the message makes 2 hops on the source and destination servers before reaching the destination client. The servers communicate with each other (for passing chatroom or client information) only when absolutely necessary.

## How to contribute

1. Fork it!
2. Create your feature branch: git checkout -b my-new-feature
3. Commit your changes: git commit -am 'Add some feature'
4. Push to the branch: git push origin my-new-feature
5. Submit a pull request :D

## Authors

* **Arjun Augustine** - [arjunaugustine](https://github.com/arjunaugustine)
* **Eswar Kokkiligadda** - [eswark2911](https://github.com/eswark2911)
* **Danis Fermi** - [danisfermi](https://github.com/danisfermi)
* **Aparna Maleth** - [aparnamaleth](https://github.com/aparnamaleth)

See also the list of [contributors](Contributors.md) who participated in this project.

## License

This project is licensed under the GPLV3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* All thanks to our professor, **Prof. Muhammad Shahzad** - [mshahza](http://www4.ncsu.edu/~mshahza/)
* [Stackoverflow](www.stackoverflow.com)
* [Python 2.7 Official Documentation](https://docs.python.org/2.7/reference/)
* [Beej’s Blog on Socket Programming Using Python](http://beej.us/blog/)
