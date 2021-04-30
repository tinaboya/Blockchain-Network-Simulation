"""
In this module, we create a class for block named Blockchain
"""

import hashlib
import time
import random

class Blockchain:
    index = 0
    data = ''
    timestamp = 0
    nounce = 0
    hash = ''
    previousHash = ''
    __filename = 'blockchain.dat'
    
    """
        index -> index of block
        data -> transaction data
        timestamp -> time of the transaction
        nounce -> random number added for PoW
        previousHash -> hash value of previous block
    """
    
    def __init__(self, index, data, timestamp, nounce, previousHash):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.nounce = nounce
        self.previousHash = previousHash
        self.hash = self.hashBlock()

    def hashBlock(self):
        """
        Compute the hash of a block using SHA256
        """
        sha = hashlib.sha256()
        forHash = str(self.index) + self.data + str(self.timestamp) + str(self.nounce) + str(self.previousHash)
        sha.update(forHash.encode('utf-8'))
        return sha.hexdigest()

    def saveBlock(self,path_block):
        """
        Write block to a flie (Add the block to a chain)
        """
        f = open(path_block, 'a', encoding='utf-8')
        f.write('\n')
        f.write(str(self.index))
        f.write(';')
        f.write(self.data.__str__())
        f.write(';')
        f.write(str(self.timestamp))
        f.write(';')
        f.write(str(self.nounce))
        f.write(';')
        f.write(str(self.previousHash))
        f.write(';')
        f.write(str(self.hash))
        f.close()
    
    def getFilename(self):
        return self.__filename

    def blockToString(self):
        """
        Convert a block object to a string
        """
        strBlock = str(self.index)+';'+self.data.__str__()+';'+str(self.timestamp)+';'+str(self.nounce)+';'+str(self.previousHash)+';'+str(self.hash)
        return strBlock

    def printBlock(self):
        """
        Print block information
        """
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp / 1000))
        data = tuple(eval(self.data))
        print('index:%d' % (self.index))
        print('data: from ' + data[0] + ' to ' + data[2] + ', amount:' + str(data[1]))
        print('time:' + date)
        print('nounce:%d' % (self.nounce))
        print('previous hash:' + self.previousHash)
        print('hash:' + self.hash)
        print('\r')


    def mining(self):
        """
        Add a random integer as nounce in block object to make its hash value begins with several number of '0'
        In our case it begins with six '0'
        """
        difficulty = 6
        nounce = random.randint(0, 999999999999)
        while self.hashBlock()[:difficulty] != "0"*difficulty:
            self.nounce = nounce
            nounce += 1
        self.hash = self.hashBlock()
        return self
