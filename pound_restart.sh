#!/bin/sh


function HELP_PRINT {
    echo
    echo "      Usage : $0 [ stop | start | restart ]"
    echo
}


############ argument check 
if [ $# -ne 1 ]; then
    HELP_PRINT
    exit
fi


case "$1" in
    start)
        echo "start"
        /usr/local/pound/sbin/pound -f /usr/local/pound/etc/pound.cfg
        ;;
    stop)
        echo "stop"
        pkill pound
        ;;
    restart)
        echo "restart"
        pkill pound
        sleep 2
        /usr/local/pound/sbin/pound -f /usr/local/pound/etc/pound.cfg
        ;;
    *)
        HELP_PRINT
        exit 2
esac
