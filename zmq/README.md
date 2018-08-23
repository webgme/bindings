# Getting started with ZeroMQ
This directory contains some sample files in javascript and python
for trying out zeromq. [The tutorial here](http://zguide.zeromq.org/page:all)
is a good start to get familiar with zeromq before attempting to create an API in another language.

## Setting up Ubuntu 16.04

#### Nodejs bindings
1. Install zeromq https://gist.github.com/katopz/8b766a5cb0ca96c816658e9407e83d00
2. Make sure python 2.7 is installed and available at `python`

```
sudo apt-get update
```

```
sudo apt-get install python
```

3. Clone this repository and set as cwd.
4. Install node-modules
```
npm install
```
5. Link zeromq to the installed libzmq
```
npm install zeromq --zmq-external
```

6. Make sure that it works. In two separate shells, first launch the server
```
node tutorial_server.js
```
and then the client.
```
node tutorial_client.js
```

If successful it should print out somethings along the lines of:

Server:
```
Listening on 5555…
Received request: [ Hello ]
Received request: [ Hello ]
...
```

Client:
```
Sending request 0 …
Sending request 1 …
...
Received reply 0 : [ World ]
Received reply 1 : [ World ]
...
```

#### Python bindings
Make sure to complete Nodejs bindings above first.

1. Install python (see above)
2. Install pip
```
sudo apt-get install python-pip python-dev build-essential
```
3. Upgrade pip to latest (this was tested with pip 10.0.1)
```
sudo pip install --upgrade pip
```
4. Install [pyzmq](http://zeromq.org/bindings:python)
```
pip install pyzmq
```
5. Now make sure it's working. In two separate shells, first launch the server (.js)
```
node tutorial_server.js
```
and then the client.
```
python tutorial_client.py
```

Similar output as above should been seen..