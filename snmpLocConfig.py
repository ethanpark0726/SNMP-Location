import datetime
import time
import wexpect
import pprint
import getpass

def accessJumpBox(username, password):

    print('\n--- Attempting connection to ' + 'IS6 Server... ')
    ssh_newkey = 'Are you sure you want to continue connecting'
    session = wexpect.spawn('ssh ' + username + '@is6.hsnet.ufl.edu')

    idx = session.expect([ssh_newkey, 'word', wexpect.EOF])

    if idx == 0:
        session.sendline('yes')
        idx = session.expect([ssh_newkey, 'word', wexpect.EOF])

        if idx == 0:
            session.sendline(password)
    elif idx == 1:
        session.sendline(password)

    idx = session.expect(['$', wexpect.EOF])

    if idx == 0:
        print("--- Successful Login to JumpBox")
        return session
    else:
        print("--- Terminated program")
        exit()

def accessSwitches(session, switch, username, password):

    if 'SSH' in switch[3]:
        ssh_newkey = 'Are you sure you want to continue'
        session.sendline('ssh ' + switch[2])

        print('\n------------------------------------------------------')
        print('--- Attempting connection to: ' + switch[2])
        print('------------------------------------------------------\n')

        idx = session.expect([ssh_newkey, 'word', wexpect.EOF])

        if idx == 0:
            session.sendline('yes')
            time.sleep(.5)
            session.sendline(password)
        elif idx == 1:
            session.sendline(password)
        
    else:
        session.sendline('telnet ' + switch[2])
        
        print('\n------------------------------------------------------')
        print('--- Attempting connection to: ' + switch[2])
        print('------------------------------------------------------\n')

        idx = session.expect(['name', wexpect.EOF])

        if idx == 0:
            session.sendline(username)
            idx = session.expect(['word', wexpect.EOF])
            session.sendline(password)

        else:
            print('Something''s wrong!')
            print('--- Terminated Program!!')
            exit()
    idx = session.expect(['>', '#', wexpect.EOF])
    print('--- Success Login to: ', switch[2])
 
    if idx == 0:
        session.sendline('en')
        idx = session.expect(['word:', wexpect.EOF])
        
    if idx == 0:
        session.sendline(password)
        session.expect(['#', wexpect.EOF])
    
    return session

def commandExecute(session, os, cmd):

    command = ''

    session.sendline('term length 0')
    session.expect(['#', wexpect.EOF])

    session.sendline('conf t')
    session.expect(['#', wexpect.EOF])

    command += 'snmp-server location ' + cmd
        
    session.sendline(command)
    session.expect(['#', wexpect.EOF])

    session.sendline('end')
    session.expect(['#', wexpect.EOF])

    session.sendline('wr')

    if os == 'IOS':
        session.expect(['#', wexpect.EOF])
    else:
        session.expect(['complete.', wexpect.EOF])

    return session.before.splitlines()

def getDeviceList():
    deviceList = []

    file = open('0514.txt', 'r')

    for line in file:
        temp = line.split('\t')
        temp[-1] = temp[-1].replace('\n', '')
        deviceList.append(temp)
    file.close()

    return deviceList

if __name__ == '__main__':

    print()
    print('+-------------------------------------------------------------+')
    print('|    Cisco L2 switches SNMP Location Config tool...           |')
    print('|    Version 1.0.0                                            |')
    print('|    Compatible with C35xx, C37xx, C38xx, C65XX               |')
    print('|    Nexus 5K, 7K, 9K                                         |')
    print('|    Scripted by Ethan Park, June. 2020                        |')
    print('+-------------------------------------------------------------+')
    print()
    username = input("Enter your admin ID ==> ")
    password = getpass.getpass("Enter your password ==> ")
    print()

    switchList = getDeviceList()

    for elem in switchList:
        
        session = accessJumpBox(username, password)
        session = accessSwitches(session, elem, username, password)
        data = commandExecute(session, elem[1], elem[4])
        print(data)
        session.close()