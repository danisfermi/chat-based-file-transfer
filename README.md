# chat-based-file-transfer

a. Environment settings

Make sure that Python version 2.7 is installed on the device. Also make sure that Environment Path variables for Python have been set up from the command line.
Make sure that the following Python Libraries are present.
* Sockets
Copy the contents of the zip file and paste it on a convenient location.

b. How to run the code

On the device we wish to execute the server, run the server.py code as sudo. Note the ip address of this device as the server IP.
We need to give this as the input to the client.py.
On the device we wish to execute the client, run client.py. Client.py takes as arguments the following:-
-h --help: for printing this help message
-s --share: followed by integer 0 or 1 to clear or set global file share
-p --parallel: followed by integer to restrict the number of parallel file shares
--ip: specify the server ip to connect to
--port: specify the server port number to connect to: 50000-50009 (by default)
-w --window: select window size n for GO-BACK-N protocol

c. How to interpret the results

Test cases included inside the project report.

d. Any sample input and output files

Sample screen shots included inside the project report.
