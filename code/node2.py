"""
rf : node1.py
"""
import sys
sys.path.append('./utils')
sys.path.append('./config')
import utils
import os
import Network as net
import Interface as Interface
import threading as th
import Operationblock as op
import time
import sys
import hashlib


def hash256(password):
	sha = hashlib.sha256()
	sha.update(password.encode('utf-8'))
	return sha.hexdigest()

def user_receive(ip,port,block_path,neighbours):
    sock = net.sk_listen(ip, port)
    while True:
        connection, IP_address = sock.accept()
        flag_broad = False
        len_block = op.loadBlockchain(block_path)
        while True:
            data = connection.recv(102400)
            if flag_broad:
                if not data:
                    new_blockchain = op.loadBlockchain(block_path)
                    if op.checkBlockchain(new_blockchain) and len(new_blockchain)>len_block:
                        os.remove('../tempchain2.dat')
                        for addr in neighbours:
                            try:
                                msg = 'broad,'
                                sock2 = net.sk_send(addr[0], addr[1])
                                sock2.send(msg.encode('utf-8'))
                                time.sleep(0.1)
                                net.sendFile(sock2, block_path)
                                sock2.close()
                            except:
                                print(sys.exc_info())
                                print("Cannot connect to neighbour " + addr[0])
                        print('Finished\n')
                    elif len(new_blockchain)==len_block:
                        flag_broad = False
                        os.remove('../tempchain2.dat')
                        break
                    else:
                        net.copyFile('../tempchain2.dat',block_path)
                        os.remove('../tempchain2.dat')
                        print('Neighbour\'s chain is not correct, updating failure')
                    flag_broad = False
                    break
                f = open(block_path, 'a')
                f.write(data.decode('utf-8'))
                f.close()
            if data.decode('utf-8').split(',')[0] == 'broad':
                len_block = len(op.loadBlockchain(block_path))
                net.copyFile(block_path,'../tempchain2.dat')
                flag_broad = True
                f = open(block_path, 'w')
                f.close()

            if data.decode('utf-8').split('&')[0] == 'mining':
                global MINING
                MINING = data.decode('utf-8').split('&')[3]

            if data.decode('utf-8').split(',')[0] == 'update':
                try:
                    msg = 'broad,' + ip +','+ str(port)
                    sock4 = net.sk_send(data.decode('utf-8').split(',')[1], int(data.decode('utf-8').split(',')[2]))
                    sock4.send(msg.encode('utf-8'))
                    time.sleep(0.1)
                    net.sendFile(sock4, block_path)
                    sock4.close()
                except:
                    print("Cannot connect to " + data.decode('utf-8').split(',')[1])
            if not data:
                break

def operation(listBlockchain,id,neighbours,IP_user,port_user,idList,path_blockchain):
    while True:
        option = Interface.option()
        balance = op.accountBalance(listBlockchain, id)
        if option == '1':
            listBlockchain = op.loadBlockchain(path_blockchain)
            balance = op.accountBalance(listBlockchain, id)
            print('username:'+id)
            print('account balance:'+str(balance))
        elif option == '2':
            amount, payee = Interface.inputTrasfer()
            listBlockchain = op.loadBlockchain(path_blockchain)
            if payee not in idList:
                print('Payee inexistant')
                continue
            elif int(amount)>balance:
                print('Insufficient funds')
                continue
            else:
                block = op.newBlock(listBlockchain[-1], id, int(amount), payee)
                blockString = block.blockToString()
                for addr in neighbours:
                    try:
                        msg = 'mining&'+IP_user+'&'+str(port_user)+'&'+blockString
                        sock2 = net.sk_send(addr[0], addr[1])
                        sock2.send(msg.encode('utf-8'))
                        sock2.close()
                        print("Mining request sent to " + addr[0])
                    except:
                        print(sys.exc_info())
                        print("Cannot connect to neighbour " + addr[0])
        elif option == '3':
            listBlockchain = op.loadBlockchain(path_blockchain)
            for i in listBlockchain:
                i.printBlock()
        elif option == '4':
            print('updating...')
            for addr in neighbours:
                try:
                    msg  = 'update,'+IP_user+','+str(port_user)
                    sock4 = net.sk_send(addr[0], addr[1])
                    sock4.send(msg.encode('utf-8'))
                    sock4.close()
                    time.sleep(0.1)
                    print('Update from '+addr[0])
                    break
                except:
                    print("Cannot connect to neighbour " + addr[0])
        elif option == '5':
            print('Waiting for mining:')
            MiningFlag = True
            while(MiningFlag):
                global MINING
                if len(MINING)>0:
                    listBlockchain = op.loadBlockchain(path_blockchain)
                    block = op.stringToBlock(MINING)
                    if(block.index == listBlockchain[-1].index):
                        MINING = ""
                    else:
                        print('Begin mining')
                        block.mining()
                        listBlockchain = op.loadBlockchain(path_blockchain)
                        if len(listBlockchain) == int(block.index):
                            block.saveBlock(path_blockchain)
                            print('Mined block:\n')
                            block.printBlock()
                            MiningFlag = False
                            for addr in neighbours:
                                try:
                                    msg = 'broad,'+IP_user+','+str(port_user)
                                    sock2 = net.sk_send(addr[0], addr[1])
                                    sock2.send(msg.encode('utf-8'))
                                    time.sleep(0.1)
                                    net.sendFile(sock2, path_blockchain)
                                    sock2.close()
                                except:
                                    print(sys.exc_info())
                                    print("Cannot connect to neighbour " + addr[0])
                        else:
                                print('Current block is already mined by others.')
                        MINING = ""
             
                    
        elif option == 'q':
            os._exit(0)
        else:
            print('Please enter a correct option')

flag_nonce = False
flag_login = False
flag_send_id = False

def login(IP_user,PORT_user,IP_center, PORT_center):
    nonce_index = -1
    global flag_nonce, flag_login, flag_send_id
    try:
        sock = net.sk_listen(IP_user,PORT_user)
    except:
        print("Connection fail")
    if not flag_nonce:
        net.requestNonce(IP_center, PORT_center,IP_user,PORT_user)
    while True:
        connection, IP_address = sock.accept()
        numloop = False
        while True:
            data = connection.recv(1024)
            if flag_nonce == False and flag_login == False:
                noncetuple = tuple(eval(data.decode('utf-8')))
                if noncetuple[0] =='nonce':
                    nonce = noncetuple[1]
                    nonce_index = noncetuple[2]
                    flag_nonce = True
                    continue
                elif numloop:
                    print('Get nonce fail')
                    option = input('y for try again, others to exit:')
                    if option == 'y':
                        break
                    else:
                        os._exit(0)
                numloop = True
            elif flag_nonce == True and flag_login == False and flag_send_id == False:
                id,password = Interface.login()
                cipher = ('login',id,hash256(password+nonce),nonce_index).__str__()
                net.sendback(cipher,IP_center,PORT_center)
                flag_send_id =True
            elif flag_nonce == True and flag_login == False and flag_send_id == True:
                feedbackTuple = tuple(eval(data.decode('utf-8')))
                if feedbackTuple[0] =='loginok':
                    flag_login == True
                    idList = feedbackTuple[1]
                    print('Login successful')
                    sock.close()
                    return True, id,idList
                elif feedbackTuple[0]=='noid':
                    print('Username does not exist')
                    id, password = Interface.login()
                    cipher = ('login', id, hash256(password + nonce), nonce_index).__str__()
                    net.sendback(cipher, IP_center, PORT_center)
                else:
                    print('username or password isn\'t correct')
                    option = input('y for try again, others to exit:')
                    if option == 'y':
                        id, password = Interface.login()
                        cipher = ('login', id, hash256(password + nonce), nonce_index).__str__()
                        net.sendback(cipher, IP_center, PORT_center)
                    else:
                        os._exit(0)
            elif flag_nonce == True and flag_login == True and flag_send_id == True:
                print('bigin to work')
            break

MINING = "" 

def user(path_ini,path_blockchain):
    IP_user, PORT_user, IP_center, PORT_center, neighbours = net.getAddress(path_ini)
    
    flag_login, id,idList = login(IP_user, PORT_user,IP_center, PORT_center)
    listBlockchain = op.loadBlockchain(path_blockchain)
    checkChain = op.checkBlockchain(listBlockchain)
    
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(listBlockchain[-1].timestamp / 1000))
    print('Checking blockchain: '+str(checkChain))
    print('Latest block: '+date)
    if flag_login == True:
        thread_listen = th.Thread(target=user_receive, name="", args=[IP_user,PORT_user,path_blockchain,neighbours])
        thread_listen.start()
        thread_operation = th.Thread(target=operation, name="", args=[listBlockchain,id,neighbours,IP_user,PORT_user,idList,path_blockchain])
        thread_operation.start()

def main():
    user('config/host2.ini','data/blockchain2.dat')

if __name__ =='__main__':
    main()
