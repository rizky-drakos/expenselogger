'''
Usage: 
    run.py login --username USERNAME --password PASSWORD --clientid CLIENTID
    run.py perform list
    run.py perform (create|update) [ --date DATE ] --name NAME --price PRICE
    run.py perform delete [ --date DATE ] --name NAME

Options:
    --help                  Show help message.
    --username USERNAME     The username for signing in.
    --password PASSWORD     The corresponding password for your username.
    --clientid CLIENTID     The app client ID.
    --date DATE             The date of your item.
    --name NAME             The name of your item.
    --price PRICE           The price of your item.
'''
import json
import os
import sys
import logging
import requests

from docopt     import docopt
from boto3      import client
from datetime   import datetime
from common     import API_URL, TOKENS_FILE

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

TODAY = datetime.today().strftime('%Y-%m-%d')

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
        logging.info('Successfully logged-in!')
        with open(TOKENS_FILE, 'w') as tokensfile:
            json.dump(
                { 
                    'ID_TOKEN': response['AuthenticationResult']['IdToken'],
                    'ACCESS_TOKEN': response['AuthenticationResult']['AccessToken'],
                    'REFRESH_TOKEN': response['AuthenticationResult']['RefreshToken'],
                },
                tokensfile,
                indent=4
            )

    if args['perform']:

        if not os.path.isfile(TOKENS_FILE):
            logging.info('Please log-in!')
            sys.exit(0)
        
        tokens = dict()
        with open(TOKENS_FILE) as tokensfile:
            tokens = json.load(tokensfile)

        if 'ID_TOKEN' not in tokens.keys():
            logging.info('Please log-in!')
            sys.exit(0)

        else:
            if args['list'] :
                try:
                    response = requests.get(
                        API_URL + '/items/{}'.format(TODAY),
                        headers = { 'Authorization': "Bearer {}".format(tokens['ID_TOKEN']) }
                    )
                
                except requests.exceptions.RequestException as error:
                    logging.error('Something happened, details:\n' + error)

                else:
                    logging.info('RESULTS:\n' + json.dumps(response.json(), indent=4))

            elif args['create']:
                try:
                    response = requests.post(
                        API_URL + '/items',
                        headers = { 'Authorization': "Bearer {}".format(tokens['ID_TOKEN']) },
                        json = {
                            "date"  :   args['--date'] or TODAY,
                            "price" :   int(args['--price']),
                            "name"  :   args['--name']
                        }
                    )
                
                except requests.exceptions.RequestException as error:
                    logging.error('Something happened, details:\n' + error)

                else:
                    logging.info('RESULTS: {}'.format(response.status_code))


            elif args['update']:
                try:
                    response = requests.put(
                        API_URL + '/items',
                        headers = { 'Authorization': "Bearer {}".format(tokens['ID_TOKEN']) },
                        json = {
                            "date"  :   args['--date'] or TODAY,
                            "price" :   int(args['--price']),
                            "name"  :   args['--name']
                        }
                    )
                
                except requests.exceptions.RequestException as error:
                    logging.error('Something happened, details:\n' + error)

                else:
                    logging.info('RESULTS: {}'.format(response.status_code))

            elif args['delete']:
                try:
                    response = requests.delete(
                        API_URL + '/items',
                        headers = { 'Authorization': "Bearer {}".format(tokens['ID_TOKEN']) },
                        json = {
                            "date"  :   args['--date'] or TODAY,
                            "name"  :   args['--name']
                        }
                    )

                except requests.exceptions.RequestException as error:
                    logging.error('Something happened, details:\n' + error)

                else:
                    logging.info('RESULTS: {}'.format(response.status_code))

            else:
                logging.info(f'{args["ACTION"]} is not supported!')
