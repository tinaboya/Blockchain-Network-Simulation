#Blockchain Project

In this project we design a simple blockchain network with one authetication center and six nodes.

##Getting started

If you want to test the whole network, you can open 7 terminals and run:

* python center.py
* python node1.py
* ...
* python node6.py

The username and password for nodeK.py are (clientK,123), with $K\in\[1,6\]$
>For example, for node1.py, (username, password) = (client1, 123)

If you want to make a trasaction, please make sure that there exists some miners (node with option = 5) in the neighboor of trasaction maker.
>For example, client1(node1) want to make a trasaction, then its neighboors, client2(node2), client3(node3) must in status of mining

And then you can operate refering the instructions on your screen.

The blockchain stored by node,...,node5 are stored as blockchain.dat,...,blockchain5.dat

Please note that, you can also test it with runing of part of nodes, like:

* python center.py
* python node1.py
* python node2.py
* python node3.py

You will see if you make a trasaction in node.py, then node1 and node2 will also receive it.

##File structure 

Filename                | Usage
-----                   | -----
blockchain[1-6].dat     | store the blockchain of client[1-6]
center.py               | authentication center
node[1-6].py            | node(users)[1-6]
config/host[1-6].ini    | address information for node[1-6]
config/center.ini       | address of center and all nodes
config/center.dat       | username and password of all users
utils/Blockchain.py     | class for blocks 
utils/Network.py        | functions for network connections
utils/Operationblock.py | functions for operation on blockchain
utils/Interface.py      | functions for User Interface

Please note that, the only difference between node[1-6].py is that the read different host[1-6].ini and blockchain[1-6].dat

## Exceptions
### Center: Connection fail
* UnboundLocalError: local variable 'sock1' referenced before assignment
 In this case, please use the command "sudo netstat -nlpte" and "kill -9 PID" to kill the existing python socket.
### Node: Mining too slow
If the mining procedure is too slow for you and you cannot wait for longtime, please modify config/Blockchain.py, in **mining()**, you can reduce **difficulty** to 3 or 4.

##Authors

 - WANG Zhaoxiang zhaoxiang.wang@ulb.be
 - ZHANG Boya boya.zhang@vub.be
 - ZHAI Peizhe peizhe.zhai@ulb.be
 - ZHANG Zheng zheng.zhang@ulb.be
