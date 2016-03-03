

#!flask/bin/python

"""Movie Recommender API"""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView




app = Flask(__name__, static_url_path="")
admin = Admin(app, name='Movie Recommender', template_mode='bootstrap3')
#admin.add_view(ModelView(Post, db.session))
api = Api(app)
auth = HTTPBasicAuth()
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import views, models
from app.models import User, UserPreferences, Movie, Video, TVSeries, FilmIndustry, Award, Actor, Genre
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPreferences, db.session))
admin.add_view(ModelView(Movie, db.session))
admin.add_view(ModelView(Video, db.session))
admin.add_view(ModelView(TVSeries, db.session))
admin.add_view(ModelView(FilmIndustry, db.session))
admin.add_view(ModelView(Award, db.session))
admin.add_view(ModelView(Actor, db.session))
admin.add_view(ModelView(Genre, db.session))




