"""
In this module we design an User Interface for users
"""

def login():
    id = input('username: ')
    password = input('password: ')
    return id, password

def option():
    print('\n')
    print('1: Account information')
    print('2: Make transfer')
    print('3: Display the blockchain')
    print('4: Update the blockchain')
    print('5: Mining')
    print('q: Quit')
    option = input('Please input your option: ')
    print('\n')	
    return option

def inputTrasfer():
    payee = input('Please enter the username of payee:')
    number = input('Please enter the transfer amount:')
    return number, payee
