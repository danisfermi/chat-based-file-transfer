# chat-based-file-transfer

## a. Environment settings

Clone the library from git as follows:-
```
git clone git@github.com:arjunaugustine/chat-based-file-transfer.git
```
Navigate inside code directory. This is our working directory, where all the run-time code is stored.

## b. Understanding how the code works:

Here is a block diagram showing how clients connect to a specific chatroom on a server in the application:
<p align="center">
  <img src="../bin/Block%20Diagram%20General.png?raw=true" alt="Sublime's custom image" width=600/>
</p>

Following is a flow chart that depicts working of a server:
<p align="center">
  <img src="../bin/Algorithm%20for%20Server-to-Client.png?raw=true" alt="Sublime's custom image" width=600/>
</p>

Following is a flow chart that depicts file transfer between two peers:
<p align="center">
  <img src="../bin/Peer%20to%20peer%20File%20Transfer%20Algorithm.png?raw=true" alt="Sublime's custom image" width=600/>
</p>

For a detailed list of all classes, functions and their descriptions, please see [ALGORITHM.md](ALGORITHM.md)


## c. How to run the code

### Start

On the device we wish to run the server on, open a terminal windows and obtain the IP address.
```
ifconfig
```
Navigate inside the code directory and run server.py as admin(sudo because we need to open sockets).
```
sudo ./server.py
```
The console will display the port number on which the server is listening. They will range from 5000 to 50009 by default.

Next, on the device we need to start the client, run the client can be run with command line arguments. The options made available to us are:-

| Argument       | Description                                              |
|:---------------|:---------------------------------------------------------|
| -h --help      | Print help options                                       |
| -s --share     | 0/1 to clear/set global file share (default 1)           |
| -p --parallel  | Int argument to define parallel connections (default 2)  |
| --ip           | Server IP (tries 0.0.0.0, 127.0.0.1 by default)          |
| --port         | Server Port (50000-50009 by default)                     |
| -w --window    | Window Size for Go-Back-N (default is 16)                |

Example to start client:-

To display the help/usage message that lists all acceptable command line arguments to client.py:
```
sudo ./client.py -h
```


By default, the client looks for server at IP addresses '0.0.0.0', and '127.0.0.1', at ports in range(50000, 50009). To connect to a server on a different IP or port number, use the --port and --ip command line arguments to let the client know where the server is. For example:
```
sudo ./client.py --ip=192.168.0.100 --port=50505
```


To start a client with Go-Back-N window size 32 and a limit of 10 parallel file transfer connections:
```
sudo ./client.py -w 32 -p 10
```


### Chat Options

Chat commands made available to the user:-

| Command                    | Description                                                      |
|:---------------------------|:-----------------------------------------------------------------|
| `@username|chat`           | Sends a message 'chat' to 'username'                             |
| `@all|chat`                | Sends a message 'chat' to all users in chatroom                  |
| `@server|chat`             | Sends a message 'chat' to server (admin)                         |
| `@all|whohas|file`         | Sends broadcast message to see who has file with filename 'file' |
| `@user|getfile|file`       | Sends a message to 'user' to start UDP peer-to-peer file transfer|
| `@server|get_rooms`        | Get a list of chat rooms avaialable with server                  |
| `@server|get_peers`        | Get a list of connected peers in chatroom                        |
| `@server|exit`             | Clean exit chat room                                             |
| `@me|setwindowsize|n`      | Sets Go-Back-N window size to 'n'                                |
| `@me|setshare|file`        | Enable sharing of filename: 'file'                               |
| `@me|clrshare|file`        | Disable sharing of filename: 'file'                              |
| `@me|setglobalshare`       | Enable sharing all files                                         |
| `@me|clrglobalshare`       | Disable sharing any files                                        |
| `@me|getsharestatus`       | Get global share status, as well as individual file share status |

Commands made available to the server:-

| Command              | Description                                                      |
|:---------------------|:-----------------------------------------------------------------|
| `@username|chat`     | Sends a message 'chat' to 'username'                             |
| `@all|chat`          | Sends a message 'chat' to all users in all chatroom              |
| `@server|chat`       | Sends a message 'chat' to self                                   |
| `exit`               | Kill all client connections and exit application gracefully      |

## d. How to interpret the results

1. Chat         : Check for chat messages in terminal (Format: #sender|message from user)
1. File Transfer: Check for file existance inside [folder](code/folder) or Check for terminal output
1. Go-Back-N    : Results included in [README.md](README.md)


## e. Any sample input and output files

Sample screen shots included inside the project report.
