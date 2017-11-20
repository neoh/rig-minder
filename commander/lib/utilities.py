import subprocess
import json
from values import config
import manuf

def full_path(path):
    path = ''.join([config.CWD, path])
    return path
    
oui_lookup = manuf.MacParser(manuf_name='/home/pi/conf/manuf')

def shell(command, isJson=False):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        return False
        
    if json:
        output = json.loads(output)
        
    return output
    
def get_manuf(mac):
    return oui_lookup.get_manuf(mac)
    
def pull_strings():
    return json.load(open(full_path('/values/strings.json'), 'r'))