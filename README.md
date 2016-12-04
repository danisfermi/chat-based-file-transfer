# Chat based Peer-to-peer File Transfer

The following project was implemented in partial compliance to the course requirements of CSC 573 Internet Protocols course, taken in Fall 2016 at North Carloina State University under Prof. Muhammad Shahzad.


Chat based peer-to-peer file transfer application, lets users create or connect to chat rooms hosted on a central server. Users (interchangeably refered to as peers or clients), can send messages to other individual peers in the chatroom, or broadcast it to the entire chatroom, using a template defined by the application. The server parses messages and forwards them to the requested destination(s). Messages can also be sent to self or the server although this is typically to send a set of pre-defined commands to use various features. These pre-defined commands, among others, leverage the same chat interface to facilitate requesting and recieving files from their peers. All message passing happens using TCP via server, but file transfers happen directly from peer to peer via UDP protocol for better performance. The application implements Go-Back-N protocol for UDP communications for reliability.

## Features

* Users can connect to a central server and create or join a chatroom.
* A user who creates a chatroom can decide whether to keep it private and enforce password based authentication for access or make it public where other users can freely join.
* A user needs to select a unique username while logging in. Incoming messages are directed at this username. 
* After login, the user is presented with a list of usernames of peers who are active in the chatroom. The server also notifies when peers join or leave a chatroom. And in addition, the client can ask the server to provide a list of all active users in that chatroom. 
* The user can use these usernames to send messages to peers. A message with '@all' in place of username becomes a broadcast message and '@server' in place of username gets directed to the server. '@me' messages get routed back to self.
* The server replaces '@\<destination username>' field in the message with source username in format '#\<source username>'
* The server can kick misbehaving clients, pull down existing chat rooms and send info messages to individual clients, or all users.
* Users can disable or enable file sharing for all files altogether, or individual files, using '@me' messages followed by proper commands.
* Clients can use an '@all' message with 'whohas' command to check which users have a particular file. a request for a specific file via chat. All receipients who have the requested file which is share-enabled will respond automatically.
* The client can then choose from a list of responders, to initiate a file transfer using 'getfile' command directed at the selected responder. We have tested a variety of file formats including pdf, txt, mp3, jpg etc.
* Go-back-N method of ARQ is implemented, with the user having the freedom to configure window sizes during run time. This enables us to test various timing parameter by varying the window size and testing for various file formats.
* A user can restrict the number of parallel outgoing file transfers after which, further requests will be blocked.
* All operations take place in parallel. No message passing or file sharing tasks block normal usage until they are over.
Detailed description on how to go about utilizing these features is present in [README.md](code/README.md)

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

Refer to [README.md](code/README.md)

## Running the tests

Refer to [README.md](code/README.md)

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example

```

## Results

Here is a sample use case we have implemented.
We run server on the server PC using the terminal as sudo ./server.py.
Then in the clients, we run the client code as sudo ./client.py -w 16 -p 100.
The clients connect to the server. They enter their usernames and choose to connect to the chat room named chatroom chatroom.
Once inside, we send some messages and request a file. We verify that the file has been successfully transferred to our folder.

| Window Size   | File Size     | Throughput  |
|:-------------:|:-------------:|:-----------:|
| 16            | 21.76MB       | 1.046MBps   |
| 32            | 21.76MB       | 1.121MBps   |

## Future Work

This is a simple, albeit complete implementation of a chat based file transfer application. It has so much potential for enhancements and integration with additional features. Some of these features we expect to add in the near future include:-
* NAT Traversal: The ability to detect servers who are connected behind NATs. Our current application requires every device to be in the same network. We can overcome this limitation by using NAT traversal (universal plug-and-play).
* Multi-hop Multi Server: Ability to have 2 peering servers (we had planned to implement this as per the [Project Proposal](Proposal.md)). This gives us access to support more clients. The servers should be able to communicate with each other, facilitating exchange of messages between devices connected across the servers.

## Contributing

1. Fork it!
2. Create your feature branch: git checkout -b my-new-feature
3. Commit your changes: git commit -am 'Add some feature'
4. Push to the branch: git push origin my-new-feature
5. Submit a pull request :D

## Authors

* **Arjun Augustine** - *Initial work* - [arjunaugustine](https://github.com/arjunaugustine)
* **Eswar Kokkiligadda** - *Initial work* - [PurpleBooth]()
* **Danis Fermi** - *Initial work* - [danisfermi](https://github.com/danisfermi)
* **Aparna Maleth** - *Initial work* - [aparnamaleth](https://github.com/aparnamaleth)

See also the list of [contributors]() who participated in this project.

## License

This project is licensed under the GPLV3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments


* **Prof. Muhammad Shahzad** - [mshahza](http://www4.ncsu.edu/~mshahza/)
