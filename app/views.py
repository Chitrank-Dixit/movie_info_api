import random
from flask import session, request, redirect, render_template
from flask.ext.restful import Resource
from app import api, app, auth,db, oauth
from app import marshal
from flask.json import jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_restful import reqparse, Resource
from app.decorators import authroize_token
from .models import User, UserPreferences, FilmIndustry, Genre, Movie, TVSeries, Video , Award ,Actor, Application, \
    Grant, AccessToken, RefreshToken
from .serializers import UserSchema , UserPreferencesSchema, GenreSchema, FilmIndustrySchema, MovieSchema, TVSeriesSchema,VideoSchema, AwardsSchema, ActorSchema, \
    ApplicationSchema, GrantSchema
from werkzeug.security import gen_salt
import datetime
# # refer microblog app by miguelgrinberg to make models and views flask, just take care this
# # time we are building the API server not just a basic site and take care to use only class based
# # views only

############### Users and Login API resource ##################


class UsersListCreateAPI(Resource):
    # decorators = [auth.login_required]
    #decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='No username provided',
                                   location='json')
        self.reqparse.add_argument('first_name', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('last_name', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('address', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('password', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='No email provided',
                                   location='json')

        super(UsersListCreateAPI, self).__init__()

    def get(self):
        users = User.query.all()
        users_schema = UserSchema(many=True)
        result = users_schema.dump(users)
        return {"users_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        user = User(str(args['username']) , str(args['first_name']), str(args['last_name']), str(args['password']), str(args['address']), str(args['email']) )
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        result = user_schema.dump(user)

        return {"data": result.data ,"message":  "data inserted" }, 201





class UsersAPI(Resource):
    #decorators = [auth.login_required]
    #decorators = [oauth.require_oauth]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('address', type=str, location='json')
        # self.reqparse.add_argument('password', type=bool, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(UsersAPI, self).__init__()

    def get(self, id):
        user = User.query.get(id)
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return {"users_detail": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        user = User.query.get(id)
        user.username = args['username']
        user.first_name = args['first_name']
        user.last_name = args['last_name']
        user.address = args['address']
        user.email = args['email']
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'data deleted'}

api.add_resource(UsersListCreateAPI, '/movie_recommend/api/v1/users/', endpoint='users')
api.add_resource(UsersAPI, '/movie_recommend/api/v1/users/<int:id>/', endpoint='user_settings')


############### UserPreferences API resource ##################

class UserPreferencesListCreateAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, required=True,
                                   help='No user_id provided',
                                   location='json')
        self.reqparse.add_argument('film_industry', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('favourite_actor', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('favourite_movies', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('favourite_tv_series', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('favourite_videos', type=list, default=[],
                                   location='json')

        super(UserPreferencesListCreateAPI, self).__init__()

    def get(self):
        user_preferences = UserPreferences.query.all()
        user_preferences_schema = UserPreferencesSchema(many=True)
        result = user_preferences_schema.dump(user_preferences)
        return {"users_preferences_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.get(args['user_id'])
        user_preferences = UserPreferences(user.id)

        for item in args['film_industry']:
            try:
                film_industry = FilmIndustry.query.get(item)
                if film_industry is not None:
                    user_preferences.film_industry.append(film_industry)
            except Exception,e:
                db.session.rollback()

        for item in args['favourite_actor']:
            try:
                actor = Actor.query.get(item)
                if actor is not None:
                    user_preferences.favourite_actor.append(actor)
            except Exception, e:
                db.session.rollback()

        for item in args['favourite_movies']:
            try:
                movie = Movie.query.get(item)
                if movie is not None:
                    user_preferences.favourite_movies.append(movie)
            except Exception,e:
                db.session.rollback()

        for item in args['favourite_videos']:
            try:
                video = Video.query.get(item)
                if video is not None:
                    user_preferences.favourite_videos.append(video)
            except Exception,e:
                db.session.rollback()

        for item in args['favourite_tv_series']:
            try:
                tvseries = TVSeries.query.get(item)
                if tvseries is not None:
                    user_preferences.favourite_tv_series.append(tvseries)
            except Exception,e:
                db.session.rollback()

        db.session.add(user_preferences)
        db.session.commit()
        user_preferences_schema = UserPreferencesSchema()
        result = user_preferences_schema.dump(user_preferences)

        return {"data": result.data ,"message":  "data inserted" }, 201


class UserPreferencesAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, location='json')
        self.reqparse.add_argument('film_industry', type=list, default=[],location='json')
        self.reqparse.add_argument('favourite_actor', type=list, default=[],location='json')
        self.reqparse.add_argument('favourite_movies', type=list, default=[],location='json')
        self.reqparse.add_argument('favourite_tv_series', type=list, default=[],location='json')
        self.reqparse.add_argument('favourite_videos', type=list, default=[],location='json')
        super(UserPreferencesAPI, self).__init__()

    def get(self, id):
        user_preferences = UserPreferences.query.get(id)
        user_preferences_schema = UserPreferencesSchema()
        result = user_preferences_schema.dump(user_preferences)
        return {"users_preferences_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        user_preferences = UserPreferences.query.get(id)
        user_preferences.user_id = (User.query.get(args['user_id'])).id


        for item in args['film_industry']:
            try:
                film_industry = FilmIndustry.query.get(item)
                if film_industry is not None:
                    user_preferences.film_industry.append(film_industry)
            except Exception,e:
                db.session.rollback()


        for item in args['favourite_actor']:
            try:
                actor = Actor.query.get(item)
                if actor is not None:
                    user_preferences.favourite_actor.append(actor)
            except Exception, e:
                db.session.rollback()

        for item in args['favourite_movies']:
            try:
                movie = Movie.query.get(item)
                if movie is not None:
                    user_preferences.favourite_movies.append(movie)
            except Exception,e:
                db.session.rollback()

        for item in args['favourite_videos']:
            try:
                video = Video.query.get(item)
                if video is not None:
                    user_preferences.favourite_videos.append(video)
            except Exception,e:
                db.session.rollback()

        for item in args['favourite_tv_series']:
            try:
                tvseries = TVSeries.query.get(item)
                if tvseries is not None:
                    user_preferences.favourite_tv_series.append(tvseries)
            except Exception,e:
                db.session.rollback()


        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        user_preferences = UserPreferences.query.get(id)
        db.session.delete(user_preferences)
        db.session.commit()
        return {'message': 'data deleted'}



api.add_resource(UserPreferencesListCreateAPI, '/movie_recommend/api/v1/user_preferences/', endpoint='user_preferences')
api.add_resource(UserPreferencesAPI, '/movie_recommend/api/v1/user_preferences/<int:id>/', endpoint='user_preferences_settings')


############### FilmIndustry API resource ##################


class FilmIndustryListCreateAPI(Resource):
    # decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name provided',
                                   location='json')
        self.reqparse.add_argument('location', type=str, default="",
                                   location='json')
        super(FilmIndustryListCreateAPI, self).__init__()

    def get(self):
        film_industries = FilmIndustry.query.all()
        film_industries_schema = FilmIndustrySchema(many=True)
        result = film_industries_schema.dump(film_industries)
        return {"film_industries_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        film_industry = FilmIndustry(str(args['name']),str(args['location']))
        db.session.add(film_industry)
        db.session.commit()
        film_industry_schema = FilmIndustrySchema()
        result = film_industry_schema.dump(film_industry)

        return {"data": result.data ,"message":  "data inserted" }, 201





class FilmIndustryAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        super(FilmIndustryAPI, self).__init__()

    def get(self, id):
        film_industry = FilmIndustry.query.get(id)
        film_industry_schema = FilmIndustrySchema()
        result = film_industry_schema.dump(film_industry)
        return {"film_industry_detail": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        film_industry = FilmIndustry.query.get(id)
        film_industry.name = args['name']
        film_industry.location = args['location']
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        film_industry = FilmIndustry.query.get(id)
        db.session.delete(film_industry)
        db.session.commit()
        return {'message': 'data deleted'}

api.add_resource(FilmIndustryListCreateAPI, '/movie_recommend/api/v1/film_industries/', endpoint='film_industries')
api.add_resource(FilmIndustryAPI, '/movie_recommend/api/v1/film_industries/<int:id>/', endpoint='film_industries_settings')




# ############### Movie API resource ##################

class MovieListCreateAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, required=True,
                                   help='No film industry provided',
                                   location='json')
        self.reqparse.add_argument('name', type=str,
                                   location='json')
        self.reqparse.add_argument('genre_id', type=int,
                                   location='json')
        self.reqparse.add_argument('actor', type=list, default=[],
                                   location='json')
        super(MovieListCreateAPI, self).__init__()

    def get(self):
        movies = Movie.query.all()
        movies_schema = MovieSchema(many=True)
        result = movies_schema.dump(movies)
        return {"movies_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        # read this for foreign key  and many to many: http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship
        film_industry = FilmIndustry.query.get(args['film_industry_id'])
        genre = Genre.query.get(args['genre_id'])
        movie = Movie(film_industry.id, str(args['name']), genre.id)
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                movie.actor.append(actor)
        db.session.add(movie)
        db.session.commit()
        movie_schema = MovieSchema()
        result = movie_schema.dump(movie)

        return {"data": result.data ,"message":  "data inserted" }, 201


class MovieAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('genre_id', type=int, location='json')
        self.reqparse.add_argument('actor', type=list, location='json')
        super(MovieAPI, self).__init__()

    def get(self, id):
        movie = Movie.query.get(id)
        movie_schema = MovieSchema()
        result = movie_schema.dump(movie)
        return {"movie_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        movie = Movie.query.get(id)
        movie.film_industry_id = (FilmIndustry.query.get(args['film_industry_id'])).id
        movie.name = args['name']
        movie.genre_id = (Genre.query.get(args['genre_id'])).id
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                movie.actor.append(actor)
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        movie = Movie.query.get(id)
        db.session.delete(movie)
        db.session.commit()
        return {'message': 'data deleted'}


api.add_resource(MovieListCreateAPI, '/movie_recommend/api/v1/movies/', endpoint='movies')
api.add_resource(MovieAPI, '/movie_recommend/api/v1/movies/<int:id>/', endpoint='movies_settings')


############### TvSeries API resource ##################

class TVSeriesListCreateAPI(Resource):
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, required=True,
                                   help='No film industry provided',
                                   location='json')
        self.reqparse.add_argument('name', type=str,
                                   location='json')
        self.reqparse.add_argument('genre_id', type=int,
                                   location='json')
        self.reqparse.add_argument('actor', type=list, default=[],
                                   location='json')
        super(TVSeriesListCreateAPI, self).__init__()

    def get(self):
        tvseries = TVSeries.query.all()
        tvseries_schema = TVSeriesSchema(many=True)
        result = tvseries_schema.dump(tvseries)
        return {"tvseries_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        # read this for foreign key  and many to many: http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship
        film_industry = FilmIndustry.query.get(args['film_industry_id'])
        genre = Genre.query.get(args['genre_id'])
        tvseries = TVSeries(film_industry.id, str(args['name']), genre.id)
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                tvseries.actor.append(actor)
        db.session.add(tvseries)
        db.session.commit()
        tvseries_schema = TVSeriesSchema()
        result = tvseries_schema.dump(tvseries)

        return {"data": result.data ,"message":  "data inserted" }, 201



class TVSeriesAPI(Resource):
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('genre_id', type=int, location='json')
        self.reqparse.add_argument('actor', type=list, location='json')
        super(TVSeriesAPI, self).__init__()

    def get(self, id):
        tvseries = TVSeries.query.get(id)
        tvseries_schema = TVSeriesSchema()
        result = tvseries_schema.dump(tvseries)
        return {"tvseries_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        tvseries = TVSeries.query.get(id)
        tvseries.film_industry_id = (FilmIndustry.query.get(args['film_industry_id'])).id
        tvseries.name = args['name']
        tvseries.genre_id = (Genre.query.get(args['genre_id'])).id
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                tvseries.actor.append(actor)
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        tvseries = TVSeries.query.get(id)
        db.session.delete(tvseries)
        db.session.commit()
        return {'message': 'data deleted'}


api.add_resource(TVSeriesListCreateAPI, '/movie_recommend/api/v1/tv_series/', endpoint='tv_series')
api.add_resource(TVSeriesAPI, '/movie_recommend/api/v1/tv_series/<int:id>/', endpoint='tv_series_settings')

############### Video API resource ##################

class VideoListCreateAPI(Resource):
    # decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, required=True,
                                   help='No film industry provided',
                                   location='json')
        self.reqparse.add_argument('name', type=str,
                                   location='json')
        self.reqparse.add_argument('genre_id', type=int,
                                   location='json')
        self.reqparse.add_argument('actor', type=list, default=[],
                                   location='json')
        super(VideoListCreateAPI, self).__init__()

    def get(self):
        videos = Video.query.all()
        videos_schema = VideoSchema(many=True)
        result = videos_schema.dump(videos)
        return {"videos_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        # read this for foreign key  and many to many: http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship
        film_industry = FilmIndustry.query.get(args['film_industry_id'])
        genre = Genre.query.get(args['genre_id'])
        video = Video(film_industry.id, str(args['name']), genre.id)
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                video.actor.append(actor)
        db.session.add(video)
        db.session.commit()
        video_schema = VideoSchema()
        result = video_schema.dump(video)

        return {"data": result.data ,"message":  "data inserted" }, 201


class VideoAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('genre_id', type=int, location='json')
        self.reqparse.add_argument('actor', type=list, location='json')
        super(VideoAPI, self).__init__()

    def get(self, id):
        video = Video.query.get(id)
        video_schema = VideoSchema()
        result = video_schema.dump(video)
        return {"video_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        video = Video.query.get(id)
        video.film_industry_id = (FilmIndustry.query.get(args['film_industry_id'])).id
        video.name = args['name']
        video.genre_id = (Genre.query.get(args['genre_id'])).id
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                video.actor.append(actor)
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        video = Video.query.get(id)
        db.session.delete(video)
        db.session.commit()
        return {'message': 'data deleted'}

api.add_resource(VideoListCreateAPI, '/movie_recommend/api/v1/videos/', endpoint='videos')
api.add_resource(VideoAPI, '/movie_recommend/api/v1/videos/<int:id>/', endpoint='videos_settings')

############### Awards API resource ##################

class AwardsListCreateAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name added',
                                   location='json')
        self.reqparse.add_argument('awarded_to', type=list, default=[],
                                   location='json')
        super(AwardsListCreateAPI, self).__init__()

    def get(self):
        awards = Award.query.all()
        awards_schema = AwardsSchema(many=True)
        result = awards_schema.dump(awards)
        return {"awards_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        award = Award(str(args['name']))
        for item in args['awarded_to']:
            actor = Actor.query.get(item)
            if actor is not None:
                award.awarded_to.append(actor)
        db.session.add(award)
        db.session.commit()
        award_schema = AwardsSchema()
        result = award_schema.dump(award)

        return {"data": result.data ,"message":  "data inserted" }, 201




class AwardsAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('awarded_to', type=list, location='json')
        super(AwardsAPI, self).__init__()

    def get(self, id):
        award = Award.query.get(id)
        award_schema = AwardsSchema()
        result = award_schema.dump(award)
        return {"awards_detail": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        award = Award.query.get(id)
        award.name = args['name']
        for item in args['actor']:
            actor = Actor.query.get(item)
            if actor is not None:
                award.awarded_to.append(actor)
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        award = Award.query.get(id)
        db.session.delete(award)
        db.session.commit()
        return {'message': 'data deleted'}


api.add_resource(AwardsListCreateAPI, '/movie_recommend/api/v1/awards/', endpoint='awards')
api.add_resource(AwardsAPI, '/movie_recommend/api/v1/awards/<int:id>/', endpoint='awards_settings')

############### Actors API resource ##################

class ActorsListCreateAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name provided',
                                   location='json')
        self.reqparse.add_argument('gender', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('age', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('date_of_birth', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('movies', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('tv_series', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('videos', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('awards', type=list, default=[],
                                   location='json')
        self.reqparse.add_argument('in_family_relations', type=[], default=[],
                                   location='json')
        super(ActorsListCreateAPI, self).__init__()

    def get(self):
        actors = Actor.query.all()
        actors_schema = ActorSchema(many=True)
        result = actors_schema.dump(actors)
        return {"actors_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        date_of_birth = datetime.datetime.strptime(str(args['date_of_birth']),"%Y-%m-%d").date()
        actor = Actor(str(args['name']), str(args['gender']), str(args['age']), date_of_birth)

        for item in args['movies']:
            try:
                movie = Movie.query.get(item)
                if movie is not None:
                    actor.movies.append(movie)
            except Exception,e:
                pass

        for item in args['tv_series']:
            try:
                tv_series = TVSeries.query.get(item)
                if tv_series is not None:
                    actor.tv_series.append(tv_series)
            except Exception, e:
                pass

        for item in args['videos']:
            try:
                video = Video.query.get(item)
                if video is not None:
                    actor.videos.append(video)
            except Exception,e:
                pass

        for item in args['awards']:
            try:
                award = Award.query.get(item)
                if award is not None:
                    actor.awards.append(award)
            except Exception,e:
                pass

        for item in args['in_family_relations']:
            try:
                in_family = Actor.query.get(item)
                if in_family is not None:
                    actor.in_family_relation.append(in_family)
            except Exception,e:
                pass

        db.session.add(actor)
        db.session.commit()
        actor_schema = ActorSchema()
        result = actor_schema.dump(actor)

        return {"data": result.data ,"message":  "data inserted" }, 201



class ActorsAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('gender', type=str, location='json')
        self.reqparse.add_argument('age', type=int, location='json')
        self.reqparse.add_argument('date_of_birth', type=str, location='json')
        self.reqparse.add_argument('movies', type=list, location='json')
        self.reqparse.add_argument('tv_series', type=list, location='json')
        self.reqparse.add_argument('videos', type=list, location='json')
        self.reqparse.add_argument('awards', type=list, location='json')
        self.reqparse.add_argument('in_family_relations', type=list, location='json')


        super(ActorsAPI, self).__init__()

    def get(self, id):
        actor = Actor.query.get(id)
        actor_schema = ActorSchema()
        result = actor_schema.dump(actor)
        return {"actor_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        actor = Actor.query.get(id)
        actor.name = str(args['name'])
        actor.gender = str(args['gender'])
        actor.age = str(args['age'])
        actor.date_of_birth = datetime.datetime.strptime(str(args['date_of_birth']),"%Y-%m-%d").date()

        for item in args['movies']:
            movie = Movie.query.get(item)
            if movie is not None:
                actor.movies.append(movie)

        for item in args['tv_series']:
            tv_series = TVSeries.query.get(item)
            if tv_series is not None:
                actor.tv_series.append(tv_series)

        for item in args['videos']:
            video = Video.query.get(item)
            if video is not None:
                actor.videos.append(video)

        for item in args['awards']:
            award = Award.query.get(item)
            if award is not None:
                actor.awards.append(award)

        for item in args['in_family_relations']:
            in_relation = Actor.query.get(item)
            if in_relation is not None:
                actor.in_family_relation.append(in_relation)
        db.session.commit()
        return {"message":  "data updated" }


    def delete(self, id):
        actor = Actor.query.get(id)
        db.session.delete(actor)
        db.session.commit()
        return {'message': 'data deleted'}


api.add_resource(ActorsListCreateAPI, '/movie_recommend/api/v1/actors/', endpoint='actors')
api.add_resource(ActorsAPI, '/movie_recommend/api/v1/actors/<int:id>/', endpoint='actors_settings')

############### Genre API resource ##################

class GenreListCreateAPI(Resource):
    #decorators = [auth.login_required]
    #decorators=[oauth.require_oauth('email')]
    decorators = [authroize_token]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name Provided',
                                   location='json')
        super(GenreListCreateAPI, self).__init__()

    def get(self):
        genres = Genre.query.all()
        genre_schema = GenreSchema(many=True)
        result = genre_schema.dump(genres)
        return {"genre_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        genre = Genre(str(args['name']))
        db.session.add(genre)
        db.session.commit()
        genre_schema = GenreSchema()
        result = genre_schema.dump(genre)

        return {"data": result.data ,"message":  "data inserted" }, 201



class GenreAPI(Resource):
    #decorators = [auth.login_required]
    decorators=[oauth.require_oauth('email')]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        super(GenreAPI, self).__init__()

    def get(self, id):
        genre = Genre.query.get(id)
        genre_schema = GenreSchema()
        result = genre_schema.dump(genre)
        return {"genre_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        genre = Genre.query.get(id)
        genre.name = args['name']
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        genre = Genre.query.get(id)
        db.session.delete(genre)
        db.session.commit()
        return {'message': 'data deleted'}

api.add_resource(GenreListCreateAPI, '/movie_recommend/api/v1/genres/', endpoint='genres')
api.add_resource(GenreAPI, '/movie_recommend/api/v1/genres/<int:id>/', endpoint='genre_settings')

############ Token Authentication specification #################

class ApplicationListCreateAPI(Resource):


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        #'name', 'client_id', 'client_secret', 'user'
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name Provided',
                                   location='json')

        self.reqparse.add_argument('client_type', type=int, required=True,
                                   help='No name Provided',
                                   location='json')


        self.reqparse.add_argument('authorization_grant_type', type=int, required=True,
                                       help='No name Provided',
                                       location='json')


        # self.reqparse.add_argument('client_id', type=str, required=True,
        #                            help='No client_id Provided',
        #                            location='json')
        #
        # self.reqparse.add_argument('client_secret', type=str, required=True,
        #                            help='No client_secret Provided',
        #                            location='json')

        self.reqparse.add_argument('user_id', type=int, required=True,
                                   help='No user_id Provided',
                                   location='json')

        super(ApplicationListCreateAPI, self).__init__()

    def get(self):
        applications = Application.query.all()
        application_schema = ApplicationSchema(many=True)
        result = application_schema.dump(applications)
        return {"genre_list": result.data}

    def post(self):
        args = self.reqparse.parse_args()
        client_id = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(40))
        client_secret = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(128))
        user = User.query.get(args['user_id'])
        application = Application(str(args['name']), client_id, client_secret, args['client_type'], args['authorization_grant_type'], user)
        db.session.add(application)
        db.session.commit()
        application_schema = ApplicationSchema()
        result = application_schema.dump(application)

        return {"data": result.data ,"message":  "data inserted" }, 201


class ApplicationAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('client_type', type=int, location='json')
        self.reqparse.add_argument('authorization_grant_type', type=int, location='json')
        # self.reqparse.add_argument('client_id', type=str, location='json')
        # self.reqparse.add_argument('client_secret', type=str, location='json')
        self.reqparse.add_argument('user_id', type=int, location='json')
        super(ApplicationAPI, self).__init__()

    def get(self, id):
        application = Application.query.get(id)
        application_schema = ApplicationSchema()
        result = application_schema.dump(application)
        return {"genre_details": result.data}

    def put(self, id):
        args = self.reqparse.parse_args()
        user = User.query.get(args['user_id'])
        application = Application.query.get(id)
        application.name = args['name']
        application.client_type = args['client_type']
        application.authorization_grant_type = args['authorization_grant_type']
        application.client_id = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(40))
        application.client_secret = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(128))
        application.user = user
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        application = Application.query.get(id)
        db.session.delete(application)
        db.session.commit()
        return {'message': 'data deleted'}

api.add_resource(ApplicationListCreateAPI, '/movie_recommend/api/v1/applications/', endpoint='applications')
api.add_resource(ApplicationAPI, '/movie_recommend/api/v1/application/<int:id>/', endpoint='application_settings')

# get the grant (code to make request from the other ends)

class CreateTokenAPI(Resource):
    """
        Create the create token api
    """

    def __init__(self):
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('grant_type', type=str, location='json')
        self.regparse.add_argument('username', type=str, location='json')
        self.regparse.add_argument('password', type=str, location='json')
        self.regparse.add_argument('client_id', type=str, location='json')
        self.regparse.add_argument('client_secret', type=str, location='json')
        super(CreateTokenAPI).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        application = Application.query.get(client_id=str(args['client_id']), client_secret=str(args['client_secret']))
        token = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(30))
        refresh_token = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(30))
        user = User.query.get(username=args['username'])
        expiry = None # time of expiration of the Token
        _scope = "read write"
        access_token = AccessToken(user, application, str(args['grant_type']), token, expiry, _scope)
        db.session.add(access_token)
        db.session.commit()
        refresh_token_instance = RefreshToken(user, application, access_token, str(args['grant_type']), refresh_token, expiry, _scope)
        db.session.add(refresh_token_instance)
        db.session.commit()
        return {'access_token': token, 'refresh_token': refresh_token, 'scope': _scope, 'token_type': "Bearer", 'expires': expiry}


api.add_resource(CreateTokenAPI, '/movie_recommend/api/v1/create-token/', endpoint='create_token_settings')

class RefreshTokenAPI(Resource):
    """
        Refresh Token API
    """

    def __init__(self):
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('refresh_token', type=str, location='json')
        super(CreateTokenAPI).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        refresh_token = RefreshToken.query.get(token=str(args['refresh_token']))
        application = refresh_token.access_token.application.id
        #application = Application.query.get(client_id=str(args['client_id']), client_secret=str(args['client_secret']))
        token = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(30))
        refresh_token = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in xrange(30))
        user = User.query.get(username=args['username'])
        expiry = None # time of expiration of the Token
        _scope = "read write"
        access_token = AccessToken(user, application, str(args['grant_type']), token, expiry, _scope)
        db.session.add(access_token)
        db.session.commit()
        refresh_token_instance = RefreshToken(user, application, access_token, str(args['grant_type']), refresh_token, expiry, _scope)
        db.session.add(refresh_token_instance)
        db.session.commit()
        return {'access_token': token, 'refresh_token': refresh_token, 'scope': _scope, 'token_type': "Bearer", 'expires': expiry}


api.add_resource(RefreshTokenAPI, '/movie_recommend/api/v1/refresh-token/', endpoint='refresh_token_settings')







class GrantAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=str, location='json')
        super(GrantAPI, self).__init__()

    def get(self, user_id):
        grant = Grant.query.filter_by(user_id=user_id)
        grant_schema = GrantSchema()
        result = grant_schema.dump(grant)
        return {"grant_details": request.data}

api.add_resource(GrantAPI, '/movie_recommend/api/v1/grant/<int:user_id>/', endpoint='grant_settings')

# def current_user():
#     if 'id' in session:
#         uid = session['id']
#         return User.query.get(uid)
#     return None
#
#
# @app.route('/', methods=('GET', 'POST'))
# def home():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             user = User(username=username)
#             db.session.add(user)
#             db.session.commit()
#         session['id'] = user.id
#         return redirect('/')
#     user = current_user()
#     return render_template('home.html', user=user)
#
#
# @app.route('/client')
# def client():
#     user = current_user()
#     if not user:
#         return redirect('/')
#     item = Client(
#         client_id=gen_salt(40),
#         client_secret=gen_salt(50),
#         _redirect_uris=' '.join([
#             'http://localhost:8000/authorized',
#             'http://127.0.0.1:8000/authorized',
#             'http://127.0.0.1:8000/authorized',
#             'http://127.0.0.1:8000/authorized',
#             ]),
#         _default_scopes='email',
#         user_id=user.id,
#     )
#     db.session.add(item)
#     db.session.commit()
#     return jsonify(
#         client_id=item.client_id,
#         client_secret=item.client_secret,
#     )
#
# @oauth.clientgetter
# def load_client(client_id):
#     return Client.query.filter_by(client_id=client_id).first()
#
#
# @oauth.grantgetter
# def load_grant(client_id, code):
#     return Grant.query.filter_by(client_id=client_id, code=code).first()
#
#
# @oauth.grantsetter
# def save_grant(client_id, code, request, *args, **kwargs):
#     # decide the expires time yourself
#     expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
#     grant = Grant(
#         client_id=client_id,
#         code=code['code'],
#         redirect_uri=request.redirect_uri,
#         _scopes=' '.join(request.scopes),
#         user=current_user(),
#         expires=expires
#     )
#     db.session.add(grant)
#     db.session.commit()
#     return grant
#
#
# @oauth.tokengetter
# def load_token(access_token=None, refresh_token=None):
#     if access_token:
#         return Token.query.filter_by(access_token=access_token).first()
#     elif refresh_token:
#         return Token.query.filter_by(refresh_token=refresh_token).first()
#
#
# @oauth.tokensetter
# def save_token(token, request, *args, **kwargs):
#     toks = Token.query.filter_by(
#         client_id=request.client.client_id,
#         user_id=request.user.id
#     )
#     # make sure that every client has only one token connected to a user
#     for t in toks:
#         db.session.delete(t)
#
#     expires_in = token.pop('expires_in')
#     expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
#
#     tok = Token(
#         access_token=token['access_token'],
#         refresh_token=token['refresh_token'],
#         token_type=token['token_type'],
#         _scopes=token['scope'],
#         expires=expires,
#         client_id=request.client.client_id,
#         user_id=request.user.id,
#     )
#     db.session.add(tok)
#     db.session.commit()
#     return tok
#
#
# @app.route('/oauth/token', methods=['GET', 'POST'])
# @oauth.token_handler
# def access_token():
#     return None
#
#
# @app.route('/oauth/authorize', methods=['GET', 'POST'])
# @oauth.authorize_handler
# def authorize(*args, **kwargs):
#     user = current_user()
#     if not user:
#         return redirect('/')
#     if request.method == 'GET':
#         client_id = kwargs.get('client_id')
#         client = Client.query.filter_by(client_id=client_id).first()
#         kwargs['client'] = client
#         kwargs['user'] = user
#         return jsonify(client_id=kwargs["client_id"], scope=kwargs["scopes"], response_type=kwargs["response_type"], redirect_uri=kwargs["redirect_uri"])
#         #return render_template('authorize.html', **kwargs)
#
#     confirm = request.form.get('confirm', 'no')
#     return confirm == 'yes'
#
#
# @app.route('/api/me')
# @oauth.require_oauth()
# def me():
#     user = request.oauth.user
#     return jsonify(username=user.username)