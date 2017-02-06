
# refer this for writing class decorator
# https://andrefsp.wordpress.com/2012/08/23/writing-a-class-decorator-in-python/

import datetime
from app import User, oauth, db
from app.models import Grant
from functools import wraps

def set_cookie(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        # TODO: Check for correct token here
        return f(*args, **kws)
    return decorated_function


