import logging

from functools          import wraps
from flask              import request
from jose               import jwt
from jose.exceptions    import ExpiredSignatureError

public_key  = ''
client_app  = ''
user_pool   = ''

def jwt_needed(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'Authorization' in request.headers.keys():
            try:
                decoded = jwt.decode(
                    request.headers['Authorization'].split(' ')[1],
                    public_key, algorithms = ['RS256'],
                    audience = client_app,
                    issuer = user_pool,
                    options = {
                        'require': [ 'aud', 'iss' ],
                        'verify_iss' : 'verify_signature'
                    }
                )
                username = decoded['cognito:username']
                logging.info(f'Token has been decoded successfully!')

            except ExpiredSignatureError as error:
                logging.error(f'Something happened: \n{error}')
                return {
                    "msg": "Token is missing!"
                }, 500

        else:
            return {
                "msg": "Unauthorized!"
            }, 401

        return func(username = username, *args, **kwargs)
        
    return wrapper
