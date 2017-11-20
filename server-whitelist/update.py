#!/usr/bin/env python
"""Update.py: Whitelists servers used for mining"""
import re
import subprocess
import os
import sys

def query_a_records(host):
    host = ''.join(['/usr/bin/host -t a ', host])
    process = subprocess.Popen(host.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return_output = []
    
    if not error:
        output = output.split('\n')
        
        for result in output:
            if len(result) == 0:
                continue
            
            matches = re.match(query_pattern, result)
            
            if matches != None:
                address = matches.group(2)
                return_output.append(address)
            
    return return_output
        
        
def iterate_algo_servers(callback):
    for line in algo_servers.split('\n'):
        split = line.split('<->')
        
        if len(split) < 2:
            print "Invalid line found"
            continue
        
        name = split[0]
        address = split[1]
        
        for location in locations:
            geo_address = address.replace('<LOCATION>', location)
            components = re.match(stratum_pattern, geo_address)
            full_address = components.group(0)
            host = components.group(1)
            port = components.group(2)
            callback(host, port, full_address)
        


if __name__ == '__main__':
    stratum_pattern = 'stratum\+tcp://([a-zA-Z0-9-.]+):([0-9]{4})'
    query_pattern = '([a-zA-Z0-9.]+) has address ([0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3})'
    location_arg = None
    current_path = sys.path[0]
    output_dir = "".join([current_path, "/output"])
    iprules_path = "".join([output_dir, "/whitelist-rules.sh"])
    algo_servers_path = "".join([current_path, "/../conf/servers.conf"])
    
    if len(sys.argv) > 1:
        location_arg = sys.argv[1].split(',')
        
    locations = location_arg or ['eu', 'usa', 'hk', 'jp', 'in', 'br']
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    host_map = {} # Could be useful some day
    unique_hosts = []
    iprules_file = open(iprules_path, "w")
    algo_servers = open(algo_servers_path, 'r').read()
    hosts_file = open('/etc/hosts', 'r+')
    iprules_file.seek(0)
    
    def iptable_iterator(address, port, full_address):
        records = query_a_records(address)
        
        for record in records:
            if address not in host_map:
                host_map[address] = []
                
            if record not in host_map[address]:
                host_map[address].append(record)
                
            if record not in unique_hosts:
                unique_hosts.append(record)
            
            
    iterate_algo_servers(iptable_iterator)
    
    content = hosts_file.read()
    hosts_file.seek(0)
    sections = content.split('\n#<-NH-SECTION->')
    original_start = sections[0]
    original_end = False
    
    if len(sections) == 3:
        original_end = sections[2]
    
    hosts_file.write(original_start)
    hosts_file.write('\n#<-NH-SECTION->\n\n')
    
    for key, value in enumerate(unique_hosts):
        host = ''.join(['whitelist-host-', str(key)])
        host_rule = ''.join([value, ' ', host, '\n'])
        hosts_file.write(host_rule)
        # TODO: add --dport support
        ip_rule = ''.join(['/sbin/iptables -A FORWARD -i tun0 -o eth0 -p tcp -s ', host, ' -j ACCEPT', '\n'])
        iprules_file.write(ip_rule)

    hosts_file.write('\n#<-NH-SECTION->')

    if original_end:
        hosts_file.write(original_end)

    hosts_file.truncate()
    hosts_file.close()
    iprules_file.truncate()
    iprules_file.close()
    
    print "\n/etc/hosts has been updated"
    print "./output/whitelist-rules.sh has been updated"
    print "\nFinished. Run `sudo bash iptables.sh` to apply."