"""
In this module, we define functions for operation on block and blockchain
"""

import utils
from utils.Blockchain import Blockchain
import time
import operator

def checkBlockchain(chain):
    """
        Check the correction of the chain: whether previousHash of genesis block is 0
                                           whether its a chain of hash value
    """
    block_index = operator.attrgetter('index')
    chain.sort(key=block_index)
    for index in range(len(chain)):
        if index ==0:
            if not (chain[index].index==0 and chain[index].previousHash=='0'):
                return False
            else:
                return True
        else:
            if not (chain[index].previousHash==chain[index-1].hash and chain[index].index ==chain[index-1].index+1):
                return False
            else:
                return True

def loadBlockchain(path):
    """
    Read a blockchain file and store blocks into a list
    """
    list = []
    filename = Blockchain(0, '0', 0, 0, 0).getFilename()
    f = open(path)
    for line in f:
        if line == '\n':
            continue
        linesplit = line[:-1].split(';')
        b = Blockchain(int(linesplit[0]), linesplit[1], int(linesplit[2]), int(linesplit[3]) ,linesplit[4])
        list.append(b)
    f.close()
    return list

def stringToBlock(strBlock):
    """
    Convert a block in string to a block object
    """
    blocksplit = strBlock.split(';')
    block = Blockchain(int(blocksplit[0]), blocksplit[1], int(blocksplit[2]), int(blocksplit[3]) ,blocksplit[4])
    return block

def genesisBlock():
    """
    Creation of genesisBlock
    """
    timestamp = int(round(time.time() * 1000))
    data = ('0', 0, '0').__str__()
    return Blockchain(0, data, timestamp, 0, 0).mining()

def newBlock(preBlock, remitter, number, payee):
    """
    Creat a block for a trascation
    """
    index = preBlock.index + 1
    timestamp = int(round(time.time() * 1000))
    data = (remitter, number, payee).__str__()
    previousHash = preBlock.hash
    nounce = 0
    return Blockchain(index, data, timestamp, nounce, previousHash)

def accountBalance(blockchain,id):
    """
    Account the balance of user
    """
    balance = 0
    for block in blockchain:
        tupleblock = tuple(eval(block.data))
        if tupleblock[0] == id:
            balance -= tupleblock[1]
        if tupleblock[2] == id:
            balance += tupleblock[1]
    return balance
