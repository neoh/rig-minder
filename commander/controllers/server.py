from lib import utilities
import json
import requests
from lib import api

def gpu_list():
    return 

def client_list():
    gateways = gateway_list(raw=True)
    clients = []
    output = []

    for gateway in gateways:
        address = gateway['vpnet_ip']
        endpoint = api.build_endpoint(address, '/clients')
        response = api.client_request(endpoint)
        
        for client in response:
            clients.append(client)
            
            output.append(' '.join([
                'Rig:',
                client['hostname'],
                '- Vendor:', 
                client['vendor'],
                '- Address:',
                client['local_address'],
                '\n'
            ]))
        
    return output
    
    
def gateway_list(raw=False):
    vpn_status = utilities.shell('/usr/local/openvpn_as/scripts/sacli VPNStatus', isJson=True)
    clients = []
    iteration = 0
    
    while True:
        key = ''.join(['openvpn_', str(iteration)])
        
        if key in vpn_status:
            print "Client net found:", key
            client_container = vpn_status[key]
            client_list = client_container['client_list']
            
            if len(client_list) > 0:
                print "Clients found in this net"
                for client in client_list:
                    data = {
                        "profile": client[0],
                        "source_ip": client[1],
                        "vpnet_ip": client[2]
                    }
                    clients.append(data)
                    print "Adding client:", json.dumps(data)
        else:
            break
        
        iteration += 1
        
    if raw:
        return clients
        
    output = []
    
    for client in clients:
        line_value = ''.join([
            'Profile:', client['profile'], 
            ' - Source:', client['source_ip'], 
            ' - Local:', client['vpnet_ip'], 
            '\n'
        ])
        
        output.append(line_value)
        
    if len(output) < 1:
        output = 'No gateways found'
        
    return output


def summary():
    return 'This is the summary'