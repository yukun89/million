#!/bin/bash

stop(){
    pid=`ps aux | grep main | grep python3 | grep -v grep | awk '{print $2}'`
    kill -9 $pid
    redis-cli -h localhost -p 6379 expire record 1
    #echo "" > log/trading.log
}

start() {
    python3 src/main.py -g1&
}

case "$1" in
    start)
        stop
        start
        echo "Done!"
        ;;
    stop)
        stop
        ;;
esac
