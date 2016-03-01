

#!flask/bin/python

"""Movie Recommender API"""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import views, models



