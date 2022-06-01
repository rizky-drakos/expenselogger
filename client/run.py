'''
Usage: 
    run.py login --username USERNAME --password PASSWORD --clientid CLIENTID
    run.py perform ACTION

Options:
    --help                  Show help message.
    --username USERNAME     The username for signing in.
    --password PASSWORD     The corresponding password for your username.
    --clientid CLIENTID    The app client ID.
'''
import os
import logging
import requests

from docopt import docopt
from boto3  import client

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

if __name__ == '__main__':
    args = docopt(__doc__)

    if args['login']:
        cognito_idp = client('cognito-idp')
        response = cognito_idp.initiate_auth(
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters = {
                'USERNAME': args['--username'],
                'PASSWORD': args['--password']
            },
            ClientId = args['--clientid']
        )
        logging.info(f'Successfully logged-in!')
        logging.info(f'{response["AuthenticationResult"]["IdToken"]}')

    if args['perform']:
        if not os.getenv('ID_TOKEN'):
            logging.info('Please log-in!')

        else:
            logging.info(f'Action: {args["ACTION"]}')
            response = requests.get(
                'http://localhost:5000/items',
                headers = { 'Authorization': "Bearer {}".format(os.getenv('ID_TOKEN')) }
            )
            logging.info(response)
