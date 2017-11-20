# Shutdown interface incase anything passes through after flushing
/sbin/ifdown <output_interface>

#Flush current rules
/sbin/iptables -F

# Use dmesg to view iptables logs
/sbin/iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7 #Logging denies

# Killswitch if VPN goes down
/sbin/iptables -A FORWARD -i <input_interface> -o <output_interface> -j DROP
/sbin/iptables -A FORWARD -i <input_interface> -o <output_interface> -m state --state RELATED,ESTABLISHED -j DROP

# Allow nicehash servers through
/bin/bash <path>/server-whitelist/output/whitelist-rules.sh

#Route traffic through VPN
/sbin/iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE #used just for dnsmasq network
/sbin/iptables -A FORWARD -i tun0 -o <output_interface> -m state --state RELATED,ESTABLISHED -j DROP
/sbin/iptables -A FORWARD -i tun0 -o <output_interface> -j DROP

/bin/bash -c "iptables-save > /etc/iptables/rules.v4"

/sbin/ifup <output_interface>