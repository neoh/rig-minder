import controllers
from lib import utilities

strings = utilities.pull_strings() # ;)

server = {
    '/h': {
        'content': strings['help']['content'],
        'type': 'private'
    },
    '/s': {
        'content': controllers.server.summary,
        'type': 'private'
    },
    '/n': {
        'content': controllers.server.gateway_list,
        'type': 'private'
    },
    '/c': {
        'content': controllers.server.client_list,
        'type': 'private'
    }
}

client = {
    '/clients': {
        'controller':  controllers.client.list_connections
    }
}