

#!flask/bin/python

"""Movie Recommender API"""

from flask import Flask, jsonify, abort, make_response
from flask.ext.login import LoginManager
from flask_script import Manager
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_oauthlib.provider import OAuth2Provider
from flask_migrate import Migrate, MigrateCommand
from flask_oauth import OAuth

# flask-jwt can also be used it is also straight forward and easy to use , just supply username and password
# and ready to be used
# https://pythonhosted.org/Flask-JWT/
# also this can be used: https://github.com/vimalloc/flask-jwt-extended












app = Flask(__name__, static_url_path="")
admin = Admin(app, name='Movie Recommender', template_mode='bootstrap3')
#admin.add_view(ModelView(Post, db.session))
# oauth provider
# done using : https://github.com/lepture/example-oauth2-server
# read more to implement oauthlib from here: http://lepture.com/en/2013/create-oauth-server
oauth = OAuth2Provider()
oauth.init_app(app)

# social oauth providers
# social_oauth = OAuth()
#
#
# # twitter
# twitter = social_oauth.remote_app('twitter',
#     base_url='https://api.twitter.com/1/',
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     access_token_url='https://api.twitter.com/oauth/access_token',
#     authorize_url='https://api.twitter.com/oauth/authenticate',
#     consumer_key='<your key here>',
#     consumer_secret='<your secret here>'
# )
#
#
# # facebook
#
# facebook = social_oauth.remote_app('facebook',
#     base_url='https://graph.facebook.com/',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key="",
#     consumer_secret="",
#     request_token_params={'scope': 'email'}
# )

api = Api(app)
auth = HTTPBasicAuth()
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
# https://flask-migrate.readthedocs.io/en/latest/


# manager = Manager(app)
# manager.add_command('db', MigrateCommand)



from app import views, models
from app.models import User, UserPreferences, Movie, Video, TVSeries, FilmIndustry, Award, Actor, Genre, Application, Grant, AccessToken, RefreshToken
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPreferences, db.session))
admin.add_view(ModelView(Movie, db.session))
admin.add_view(ModelView(Video, db.session))
admin.add_view(ModelView(TVSeries, db.session))
admin.add_view(ModelView(FilmIndustry, db.session))
admin.add_view(ModelView(Award, db.session))
admin.add_view(ModelView(Actor, db.session))
admin.add_view(ModelView(Genre, db.session))
admin.add_view(ModelView(Application, db.session))
admin.add_view(ModelView(Grant, db.session))
admin.add_view(ModelView(AccessToken, db.session))
admin.add_view(ModelView(RefreshToken, db.session))





