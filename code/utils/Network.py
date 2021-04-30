"""
In this module, we build some useful functions for the blockchain network
"""

import socket as sk
import threading as th
import linecache
import time

def sk_send(IP_dst, port_dst):
    """
    Build a connection with IP_dst:port_dst, using protocol TCP
    """
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM, proto=sk.getprotobyname('tcp'))
    sock.connect((IP_dst, port_dst))
    return sock

def sk_listen(IP_listen, port_listen):
    """
    Listen for others' connection, using protocol TCP
    """
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM, proto=sk.getprotobyname('tcp'))
    sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    sock.bind((IP_listen, port_listen))
    sock.listen(10)
    return sock

def sendMsg(msg,IP_dst, port_dst):
    """
    Send a string message using socket
    """
    sock = sk_send(IP_dst, port_dst)
    sock.send(msg.encode('utf-8'))

def sendFile(sock,path):
    """
    Send a file using socket
    """
    with open(path,'r') as f:
        for data in f:
            sock.send(data.encode('utf-8'))
            time.sleep(0.1)
    f.close()

def requestNonce(IP_dst, port_dst,IP_user,port_user):
    """
    Ask a nounce from center for login 
    """
    msg = (0,IP_user,port_user).__str__()
    thread = th.Thread(target=sendMsg, name="messenger_receiver", args=[msg,IP_dst,port_dst])
    thread.start()
    thread.join()

def sendback(msg,IP_dst, port_dst):
    """
    Send a nounce to node(user)
    """
    thread = th.Thread(target=sendMsg, name="messenger_receiver", args=[msg, IP_dst, port_dst])
    thread.start()
    thread.join()

def getAddressCenter(path):
    """
    This function is for center to get the address information of itself and all the nodes 
    """
    lines = linecache.getlines(path)
    nodes = []
    IP_center = ''
    PORT_center = 5001
    for index in range(len(lines)):
        if lines[index][:-1] == '[center]':
            IP_center = lines[index + 1].split('=')[1][:-1]
            PORT_center = int(lines[index + 2].split('=')[1][:-1])
        elif lines[index][:-1]=='[nodes]':
            n = 1
            while 1:
                try:
                    node = []
                    node.append(lines[index + n].split(',')[0])
                    node.append(lines[index + n].split(',')[1])
                    node.append(int(lines[index + n].split(',')[2][:-1]))
                    nodes.append(node)
                    n += 1
                except:
                    break
    return IP_center,PORT_center,nodes

def getAddress(path):
    """
    This function is for nodes to get address information of itself, of center and of its neighboors
    """
    IP_user = ''
    PORT_user,PORT_center = 5001,5001
    IP_center = ''
    lines = linecache.getlines(path)
    neighbours = []
    for index in range(len(lines)):
        if lines[index][:-1]=='[node]':
            IP_user = lines[index+1].split('=')[1][:-1]
            PORT_user = int(lines[index+2].split('=')[1][:-1])
        elif lines[index][:-1]=='[center]':
            IP_center = lines[index + 1].split('=')[1][:-1]
            PORT_center = int(lines[index + 2].split('=')[1][:-1])
        elif lines[index][:-1]=='[neighbours]':
            n = 1
            while 1:
                try:
                    neighbour = []
                    neighbour.append(lines[index + n].split(',')[0])
                    neighbour.append(int(lines[index + n].split(',')[1][:-1]))
                    neighbours.append(neighbour)
                    n+=1
                except:
                    break
    return IP_user,PORT_user,IP_center,PORT_center,neighbours

def getUserinfo(id):
    """
    This function is for center to get information of users, such as username, password, etc
    """
    lines = linecache.getlines('config/center.dat')
    password = ''
    ip = ''
    port = 5001
    for line in lines:
        linesplit = line.split(',')
        if linesplit[0]==id:
            password = linesplit[1]
            ip = linesplit[2]
            port = int(linesplit[3][:-1])
    return password, ip, port

def copyFile(src_path,copy_path):
    """
    Copy a file from src_path to copy_path
    """
    source = open(src_path, "r", encoding="utf-8")
    copy = open(copy_path, "w", encoding="utf-8")
    while True:
        content = source.read(1024)
        if len(content) == 0:
            break
        copy.write(content)
    source.close()
    copy.close()
