# Chat based Peer-to-peer File Transfer

The following project was implemented in partial compliance to the course requirements of CSC 573 Internet Protocols course, taken in Fall 2016 at North Carloina State University under Prof. Muhammad Shahzad.


Chat based peer-to-peer file transfer application. Lets clients create or connect to chat rooms hosted on a central server. The clients are interchangeably refered to as peers.  The application defines a template to send messages and the clients may leverage the same chat interface to request and recieve files from their peers.

## Features

* 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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


* Inspiration
* etc
