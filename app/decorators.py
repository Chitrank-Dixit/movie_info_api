
# refer this for writing class decorator
# https://andrefsp.wordpress.com/2012/08/23/writing-a-class-decorator-in-python/

import datetime
from app import oauth, db
from app.models import Grant, AccessToken
from functools import wraps
from flask import request, Response, jsonify, current_app
import json
from app.serializers import UserSchema

# make another admin user authorization (check that with user role as admin)

def authorize_token(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: Check for correct token here
        bearer, token = request.environ['HTTP_AUTHORIZATION'].split()
        access_token = AccessToken.query.filter_by(token=token).first()
        if access_token:
            # user_schema = UserSchema()
            # result = user_schema.dump(access_token.user)
            # return jsonify({"user": result})
            # content = json.dumps({"user": "sdf"})
            # return current_app.response_class(content, mimetype="application/json")
            kwargs['user'] = access_token.user
            return function(*args, **kwargs)

        js = json.dumps({"Unauthorized": "Invalid Token Provided"})
        return Response(js, 401, mimetype="application/json")
    return decorated_function


