"""
In this module we define 
"""
import utils
import utils.Network as net
import random
import hashlib

def hash256(password):
    """
    Compute the hase value of a string using SHA256
    """
    sha = hashlib.sha256()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()

def center():

    IP_center, PORT_center,nodes = net.getAddressCenter('config/center.ini') # get informations of center and nodes
    idList = [] # list of username of users

    for node in nodes:
        idList.append(node[0])
    
    nonceList = []
    
    try: # listen for others' login connections
        sock1 = net.sk_listen(IP_center,PORT_center)
    except:
        print("Connection fail")
    
    while True: 
        flag_addr = True
        connection1, IP_address = sock1.accept()
        # If nodes connected, verify the correction of username and password
        while True:
            """
            Receive login data from nodes
            """
            data = connection1.recv(1024)
            datatuple = tuple(eval(data.decode('utf-8')))
            if flag_addr and type(datatuple[2])==int:
                IP_user = datatuple[1]
                PORT_user = datatuple[2]
                flag_addr = False
            if datatuple[0]==0:
                """
                Send nounce to user for login
                """
                nonce = str(random.randint(0,99999999)).zfill(8)
                nonceList.append(nonce)
                nonceback=('nonce',nonce,len(nonceList)).__str__()
                net.sendback(nonceback,IP_user,PORT_user)
            elif datatuple[0]=='login':
                """
                Verification of username and hash value recevied
                """
                if datatuple[1] not in idList:
                    feedback = ("noid",).__str__()
                    net.sendback(feedback, IP_user, PORT_user)
                else:					
                    password,ip,port = net.getUserinfo(datatuple[1])
                    if datatuple[2]==hash256(password+nonceList[datatuple[3]-1]):
                        tuplefeedback = ('loginok',idList)
                        feedback = tuplefeedback.__str__()
                        net.sendback(feedback,ip,port)
                    else:
                        feedback = ('loginfail',).__str__()
                        net.sendback(feedback, ip, port)
            break

def main():
    center()

if __name__ =='__main__':
    main()
