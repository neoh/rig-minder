from lib import utilities
from values import config

def tplink_plug_details():
    print "test"
    
def list_connections():
    dnsmasq_leases = open('/var/lib/misc/dnsmasq.leases', 'r').read().split('\n')
    connections = []
    
    for lease in dnsmasq_leases:
        if len(lease) > 0:
            data = lease.split(' ')

            connections.append({
                'mac': data[1],
                'local_address': data[2],
                'hostname': data[3],
                'vendor': utilities.get_manuf(data[1])
            })

    return connections
    
def gateway_info():
    #return hostname and vendor
    return 'test'