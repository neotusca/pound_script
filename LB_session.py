#!/usr/bin/python

import pwd
import os
import sys
import re
import glob
import time

PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }
PUBLIC_IP = '210.120.128.20'
PRIVATE_IP = '192.168.10.20'
UID = 'pound'

####################################################################
def _load():
    ''' Read the table of tcp connections & remove header  '''
    with open(PROC_TCP,'r') as f:
        content = f.readlines()
        content.pop(0)
    return content

def _remove_empty(array):
    return [x for x in array if x !='']

def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port)

def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)

def _hex2dec(s):
    return str(int(s,16))

def _aaaa(session):
    ''' counting list of session '''
 
    tmp_list = []
    unique_list = []

    for line in session:
        if tmp_list.count(line) == 0:
            tmp_list.append(line)

    for line in tmp_list:
        unique_list.append([line, session.count(line)])

    return unique_list

def _print_status(incoming, distribute):

    print ""
    print "                                   --------------------------"

    cnt=1
    for n in incoming:
        print "[%2d][%15s][%2d] ------> | %s           |" % (cnt,n[0], n[1], PUBLIC_IP)
        cnt+=1

    print "                                  |                          |"

    cnt=1
    for n in distribute:
        print "                                  |            %s | ------> [%2d][%15s][%2d]" % (PRIVATE_IP, cnt,n[0], n[1])
        cnt+=1
    
    print "                                   --------------------------"

    return None


####################################################################


def session_view():

    result = []
    for line in _load():
        line_array = _remove_empty(line.split(' '))     # Split lines and remove empty spaces.
        l_host,l_port = _convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
        r_host,r_port = _convert_ip_port(line_array[2]) 
        uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID.

        if uid == UID:
            nline = [r_host, l_host]
            result.append(nline)
    result.sort()

    a=time.localtime()
    print ""
    print ""
    print '####################################################################################################'
    print " Network Session Total Count : %3d                                              %s.%s.%s %s:%s:%s" % (len(result), a[0],a[1],a[2],a[3],a[4],a[5])

    '''
    To divide to external connection and internal connection from total network session by uid
    '''
  
    incoming = []
    distribute = []

    for line in result:
        if line[1] == PUBLIC_IP:
            incoming.append(line[0])
        elif line[1] == PRIVATE_IP:
            distribute.append(line[0])

    uniq_incoming = _aaaa(incoming)
    uniq_distribute = _aaaa(distribute)

    print " INCOMING COUNT : %d" % len(incoming)
    print " DISTRIBUTE COUNT : %d" % len(distribute)
    print '###############################################'

    _print_status(uniq_incoming, uniq_distribute)

    return None


#################################################
if __name__ == '__main__':

    while(1):
        #print netstat()
        try:
            session_view()
            time.sleep(2)
        except KeyboardInterrupt:
            break


