import json
import requests
from values import config

def build_endpoint(address, path):
    return ''.join(['http://', address, ':', config.PORT, path])
    
def client_request(endpoint, data=False):
    headers = {
        "Server-Access-Key": config.ACCESS_KEY
    }
    
    if not data:
        response = requests.get(endpoint, headers=headers)
    else:
        response = requests.post(endpoint, data=data, headers=headers)
        
    return response.json()