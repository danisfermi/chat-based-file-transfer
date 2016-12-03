# Chat based Peer-to-peer File Transfer

The following project was implemented in partial compliance to the course requirements of CSC 573 Internet Protocols course, taken in Fall 2016 at North Carloina State University under Prof. Muhammad Shahzad.


Chat based peer-to-peer file transfer application. Lets clients create or connect to chat rooms hosted on a central server. The clients are interchangeably refered to as peers.  The application defines a template to send messages and the clients may leverage the same chat interface to request and recieve files from their peers.

## Features

* Peers (clients) can connect to a central server over a TCP connection. This enables them to create or join a chatroom.
* Chatroom creator (first client who created the chatroom) can decide whether to enforce password based authentication for connectin to chatrooms.
* Connected clients can chat with other peers present in the chatroom. He can send a broadcast message to all clients, or initiate a directed chat. He can also chat with the server.
* Server acts as a pseudo admin, monitoring all chat activities. Additionaly, the server has the power to kick misbehaving clients, regulate client messages, pull down existing chat rooms etc.
* Clients can broadcast a request for a specific file via chat. All receiving clients who have the requested file will respond. The client can then choose from among them, to initiate a file transfer via UDP connection. We have tested a variety of file formats including pdf, txt, mp3, jpg etc. We also implement an ACK based reliablity control on top of the unreliable UDP connection.
* Users have the freedom to choose whether to selectively disable/enable shareablity status of a file (or all files).
* Go-back-N method of ARQ is implemented, with the user having the freedom to choose the window size. This enables us to test various timing parameter by varying the window size and testing for various file formats.
Detailed description on how to go about implementing these features is present in [README](code/README.md)

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

Link to code/README.md

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
| Window Size     | File Size    | Throughput |
| ----------------|--------------|------------|
| 16              | 21.76MB      | 1.046MBps  |
| 32              | 21.76MB      | 1.121MBps  |


## Future Work

This is a simple, albeit complete implementation of a chat based file transfer application. It has so much potential for enhancements and integration with additional features. Some of these features we expect to add in the near future include:-
* NAT Traversal: The ability to detect servers who are connected behind NATs. Our current application requires every device to be in the same network. We can overcome this limitation by using NAT traversal (universal plug-and-play).
* Multi-hop Multi Server: Ability to have 2 peering servers (we had planned to implement this as per the [Project Proposal](Proposal.md)). This gives us access to support more clients. The servers should be able to communicate with each other, facilitating exchange of messages between devices connected across the servers.

## Authors

* **Arjun Augustine** - *Initial work* - [arjunaugustine](https://github.com/arjunaugustine)
* **Eswar Kokkiligadda** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **Danis Fermi** - *Initial work* - [danisfermi](https://github.com/danisfermi)
* **Aparna Maleth** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors]() who participated in this project.

## License

This project is licensed under the GPLV3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments


* **Prof. Muhammad Shahzad** - [mshahza](http://www4.ncsu.edu/~mshahza/)
