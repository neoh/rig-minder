from twilio import send_text
import json
import os
import types
from values import config
from values import routes

def server_router(address, command):
    if command in routes.server:
        reply = routes.server[command]
        
        if reply['type'] == "private" and address not in config.RECIPIENTS:
            print "Unauthorized request"
            return
        
        if callable(reply['content']):
            reply['content'] = reply['content']()
            
        if type(reply['content']) is types.ListType:
            reply['content'] = '\n'.join(reply['content'])
            
        print "Sending reply:\n", reply['content']
        send_text(address, reply['content'])
    else:
        print "Invalid command sent"
    
def client_router(path, data=False):
    if path in routes.client:
        return routes.client[path]['controller']()