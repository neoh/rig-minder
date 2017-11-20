#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
CONF=$SCRIPTPATH/conf
replacer=$SCRIPTPATH/standalone/replace.py

if [ "$1" = "finish" ]
then
    systemctl enable openvpn@client
    echo "VPN enabled. Check the below IP matches your VPN."
    curl ipinfo.io/ip
    exit
fi

ifconfig

echo "Please choose an interface from above for connecting to the internet: (e.g. wlan0)"
read input_interface

echo "Please choose an interface from above for allowing clients to connect through: (e.g. eth0)"
read output_interface

python $replacer $CONF/interfaces $CONF/compiled/interfaces "<input_interface>,<output_interface>" "$input_interface,$output_interface"
python $replacer $CONF/iptables.sh $CONF/compiled/iptables.sh "<input_interface>,<output_interface>,<path>" "$input_interface,$output_interface,$SCRIPTPATH"
cp $CONF/compiled/interfaces /etc/network/interfaces

echo "Interfaces set"

echo "Will you be connecting via WiFi? (Y/N)"
read has_wifi

if [ "$has_wifi" = "Y" ]
then
    echo "WiFi network name: (e.g. o2-WLAN-1)"
    read network_name
    echo "Password: (e.g. myrouterpass)"
    read network_pass
    
    python $replacer $CONF/wpa_supplicant.conf $CONF/compiled/wpa_supplicant.conf "<username>,<password>" "$network_name,$network_pass"
    cp $CONF/compiled/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
    #TEST SUPPLICANT
    #wpa_supplicant -Dwext -iwlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf

fi

echo "Please change your password"
passwd

systemctl enable ssh

# Remove some uneeded libs that could cause issues
apt-get -y purge plymouth*
apt-get -y purge raspberrypi-ui-mods*
apt-get -y autoremove

apt-get -y update
apt-get -y upgrade
apt-get -y install fail2ban openvpn python-requests # python-argparse
#apt-get -y install rpi-update && rpi-update
# Make them change hostname
#raspi-config

# Copy openvpn config
cp $CONF/client.ovpn /etc/openvpn/client.conf

# Install cron jobs
python $replacer $CONF/crontab $CONF/compiled/crontab "<path>" $SCRIPTPATH
crontab $CONF/compiled/crontab

# Always require password
sh -c "echo \"pi ALL=(ALL) PASSWD: ALL\" > '/etc/sudoers.d/010_pi-nopasswd'"

echo "Finished. Please reboot and run this script again like this: sudo ./provision.sh finish"