#!/bin/sh

SVC_VIP=`hostname -i`
SVC_PORT=80


while(true)
do
    clear
    echo "Pound status               " [ $SVC_VIP : $SVC_PORT ]
    echo "----------------------------------------------------"
    echo

    netstat -antp | grep pound | grep -v LISTEN | awk '{print $4,$5}'

    #NETSTAT=`netstat -atnp`
    #echo $NETSTAT


    exit

    echo "[Out -> In]"
    #netstat -atnp | grep $SVC_VIP:$SVC_PORT | grep -v LISTEN | sort -k5 | awk '{print $4,$5}'  | awk -F':' '{print $2, $1}' | awk '{print $2, $3, $4}' | uniq -c
    #netstat -atnp | grep $SVC_VIP:$SVC_PORT | grep -v LISTEN | sort -k5 | awk '{print $5}'  | awk -F':' '{print $1}' | uniq -c

    netstat -atnp | grep 210.120.128.20:80 | grep -v LISTEN | sort -k5 | awk '{print $4,$5}'  | awk -F':' '{print $2," ----> ", $1}'  | awk '{print $2, $3, $4}' | uniq -c

    echo "----------------------------------------------------"

    echo "[In -> Distribute]"
    netstat -atnp | grep 192.168 | sort -k5 | awk '{print $4,$5}' | awk -F':' '{print $1," ----> ", $2}' | awk '{print $1, $2, $4}' | uniq -c

    sleep 2
done
