# Chat-room
A Simple Network Chat (SNC) built in C programming language. The program has two files - <b>server.c</b> and <b>client.c</b>. The program uses multithreading for handling multiple clients.

# Compile the program
Just simply run the Makefile using this command. <br/>
$ make Makefile compile

# Run the Server
The server can be run using below command. <br/>
$ ./server <maximum number of clients> <maximum idle time>

Maximum number of clients - Should be in range of 1 to 10
Maximum idle time - Should be in range of 1 to 300 seconds

eg:-  $ ./server 5 200

# Run the Client
The client can be run using below command. <br/>
$ ./client <Server's IP address> <port>

In here server IP is set to be - 127.0.0.1 and port is set to be 4444

eg:-  $ ./client 127.0.0.1 4444
