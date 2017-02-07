
# refer this for writing class decorator
# https://andrefsp.wordpress.com/2012/08/23/writing-a-class-decorator-in-python/

import datetime
from app import oauth, db
from app.models import Grant, AccessToken
from functools import wraps


def authroize_token(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: Check for correct token here
        access_token = AccessToken.query.get()
        if access_token:
            return function(True, *args, **kwargs)
        return function(*args, **kwargs)
    return decorated_function


