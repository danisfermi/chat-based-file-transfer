# chat-based-file-transfer

## a. Environment settings

Clone the library from git as follows:-
```
git clone git@github.com:arjunaugustine/chat-based-file-transfer.git
```
Navigate inside cde directory. This is our working directory, where all the run-time code is stored.

## b. How to run the code

### Start

On the device we wish to run the server on, open a terminal windows and obtain the IP address.
```
ifconfig
```
Navigate inside the code directory and run server.py as admin(sudo because we need to open sockets).
```
sudo ./server.py
```
Next, on the device we need to start the client, run the client can be run with command line arguments. The options made available to us are:-
| Argument       | Description                                     |
|:--------------:|:-----------------------------------------------:|
| -h --help      | Print help options                              |
| -s --share     | 0/1 to clear/set global file share              |
| -p --parallel  | Integer argument to define parallel connections |
| --ip           | Server IP                                       |
| --port         | Server Port (50000-50009 by default)            |
| -w --window    | Window Size for Go-Back-N (16/32 recommended)   |

Example to start client:-
```
sudo ./client.py -h
```
Displays the options aavailable to start client.
```
sudo ./client.py -w 32 -p 100
```
Starts client with Go-Back-N window size 32 and 100 parallel connection limit

### Chat Options

Chat commands made available to the user:-
| Argument       | Description                                     |
|:--------------:|:-----------------------------------------------:|
| -h --help      | Print help options                              |
| -s --share     | 0/1 to clear/set global file share              |
| -p --parallel  | Integer argument to define parallel connections |
| --ip           | Server IP                                       |
| --port         | Server Port (50000-50009 by default)            |
| -w --window    | Window Size for Go-Back-N (16/32 recommended)   |

### File Transfer Options



## c. How to interpret the results

Test cases included inside the project report.

## d. Any sample input and output files

Sample screen shots included inside the project report.
