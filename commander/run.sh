#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
RUN_TYPE=$1

eval $(/bin/cat /home/pi/conf/.env | /bin/sed 's/^/export /')

if [ "$RUN_TYPE" = "server" ]
then
    /sbin/iptables -I INPUT -p tcp --dport $HTTP_PORT -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
    /sbin/iptables -I OUTPUT -p tcp --sport $HTTP_PORT -m conntrack --ctstate ESTABLISHED -j ACCEPT
fi

if [ "$RUN_TYPE" = "client" ]
then
    /sbin/iptables -I INPUT -i tun0 -p tcp --dport $HTTP_PORT -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
    /sbin/iptables -I OUTPUT -o tun0 -p tcp --sport $HTTP_PORT -m conntrack --ctstate ESTABLISHED -j ACCEPT
fi

echo "Starting HTTP server on port: $HTTP_PORT"
/usr/bin/python $SCRIPTPATH/listener.py $1