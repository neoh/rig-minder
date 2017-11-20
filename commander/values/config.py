import os

ACC_ID = os.environ['TWILIO_ACC_ID']
PORT = os.environ['HTTP_PORT'] if 'HTTP_PORT' in os.environ else 8081
FROM_ADDRESS = os.environ['TWILIO_FROM']
AUTH_USER = os.environ['TWILIO_USER']
AUTH_PASS = os.environ['TWILIO_PASS']
RECIPIENTS = os.environ['RECIPIENTS'].split(',')
ACCESS_KEY = os.environ['ACCESS_KEY']
CWD = os.getcwd()