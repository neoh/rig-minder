import requests
from requests.auth import HTTPBasicAuth
import urllib
from values import config

message_endpoint = ''.join(['https://api.twilio.com/2010-04-01/Accounts/', config.ACC_ID, '/Messages.json'])

def send_text(address, body):
    data = {
        "To": address,
        "From": config.FROM_ADDRESS,
        "Body": body
    }
    
    response = requests.post(message_endpoint, data=data, auth=HTTPBasicAuth(config.AUTH_USER, config.AUTH_PASS))
    return response.content

