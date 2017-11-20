SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

# List connected clients
if [ "$1" = "" ]
then
echo 'Usage: sudo ./helper.sh --command arg1 arg2 

Command list:
--clients                           List connected clients
--set-internet-iface <old> <new>    Replace internet connectivity interface
'
fi

# List connected clients
if [ "$1" = "--clients" ]
then
    cat /var/lib/misc/dnsmasq.leases
fi

# Set interface for connecting to the internet. 
# Default is eth0
# Example: sudo ./helper.sh --set-internet-iface eth0 wlan0
if [ "$1" = "--set-internet-iface" ]
then
    python ./standalone/replace.py /etc/network/interfaces $2 $3
fi

# View log files for a specific service
if [ "$1" = "--view-log" ]
then
    echo 1
fi

# Remove a ban related to failed logins to the SSH service
if [ "$1" = "--unban" ]
then
    fail2ban-client set sshd unbanip $2
fi

# Setup the notification server files on your vpn
# --setup-vpn root 127.0.0.1
if [ "$1" = "--setup-vpn" ]
then
    scp -r $SCRIPTPATH/commander $2@$3
fi