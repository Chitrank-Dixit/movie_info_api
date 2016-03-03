from flask.ext.restful import Resource
from app import api, app, auth,db
from app import marshal
from flask.json import jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_restful import reqparse, Resource
from .models import User, UserPreferences, FilmIndustry, Genre, Movie, Actor
from .serializers import UserSchema , UserPreferencesSchema, GenreSchema, FilmIndustrySchema, MovieSchema

# # refer microblog app by miguelgrinberg to make models and views flask, just take care this
# # time we are building the API server not just a basic site and take care to use only class based
# # views only

############### Users and Login API resource ##################


class UsersListCreateAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='No username provided',
                                   location='json')
        self.reqparse.add_argument('first_name', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('last_name', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('location', type=str, default="",
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
        user = User(str(args['username']) , str(args['first_name']), str(args['last_name']), str(args['password']), str(args['location']), str(args['email']) )
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        result = user_schema.dump(user)

        return {"data": result.data ,"message":  "data inserted" }, 201





class UsersAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
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
        user.location = args['location']
        user.email = args['email']
        db.session.commit()
        return {'message': 'data updated'}

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'data deleted'}

api.add_resource(UsersListCreateAPI, '/movie_recommend/api/v1/users', endpoint='users')
api.add_resource(UsersAPI, '/movie_recommend/api/v1/users/<int:id>', endpoint='user_settings')


############### UserPreferences API resource ##################

class UserPreferencesListCreateAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(UserPreferencesListCreateAPI, self).__init__()

    def get(self):
        user_preferences = UserPreferences.query.all()
        user_preferences_schema = UserPreferencesSchema(many=True)
        result = user_preferences_schema.dump(user_preferences)
        return {"users_preferences_list": result.data}

    # def post(self):
    #     args = self.reqparse.parse_args()
    #     task = {
    #         'id': tasks[-1]['id'] + 1,
    #         'title': args['title'],
    #         'description': args['description'],
    #         'done': False
    #     }
    #     tasks.append(task)
    #     return {'task': marshal(task, task_fields)}, 201



# class UserPreferencesAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()
#
#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}
#
#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}
#
#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}
#
#

api.add_resource(UserPreferencesListCreateAPI, '/movie_recommend/api/v1/user_preferences', endpoint='user_preferences')
#api.add_resource(UsersAPI, '/movie_recommend/api/v1/user_preferences/<int:id>', endpoint='user_preferences_settings')


############### FilmIndustry API resource ##################


class FilmIndustryListCreateAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No username provided',
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
        film_industry = FilmIndustry(str(args['name']) ,str(args['location']) )
        db.session.add(film_industry)
        db.session.commit()
        film_industry_schema = FilmIndustrySchema()
        result = film_industry_schema.dump(film_industry)

        return {"data": result.data ,"message":  "data inserted" }, 201





class FilmIndustryAPI(Resource):
    #decorators = [auth.login_required]

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

api.add_resource(FilmIndustryListCreateAPI, '/movie_recommend/api/v1/film_industries', endpoint='film_industries')
api.add_resource(FilmIndustryAPI, '/movie_recommend/api/v1/film_industries/<int:id>', endpoint='film_industries_settings')




# ############### Movie API resource ##################

class MovieListCreateAPI(Resource):
    #decorators = [auth.login_required]

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
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('film_industry_id', type=int, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('genre_id', type=int, location='json')
        self.reqparse.add_argument('actor', type=list, location='json')
        super(MovieAPI, self).__init__()

    def get(self, id):
        movie = Movie.query.get(id)
        movie_schema = MovieSchema(many=True)
        result = movie_schema.dump(movie)
        return {"movies_list": result.data}

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


api.add_resource(MovieListCreateAPI, '/movie_recommend/api/v1/movies', endpoint='movies')



# ############### TvSeries API resource ##################
#
# class TVSeriesListCreateAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, required=True,
#                                    help='No task title provided',
#                                    location='json')
#         self.reqparse.add_argument('description', type=str, default="",
#                                    location='json')
#         super(TaskListAPI, self).__init__()
#
#     def get(self):
#         return {'tasks': [marshal(task, task_fields) for task in tasks]}
#
#     def post(self):
#         args = self.reqparse.parse_args()
#         task = {
#             'id': tasks[-1]['id'] + 1,
#             'title': args['title'],
#             'description': args['description'],
#             'done': False
#         }
#         tasks.append(task)
#         return {'task': marshal(task, task_fields)}, 201
#
#
# class TVSeriesAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()
#
#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}
#
#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}
#
#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}
#
# ############### Video API resource ##################
#
# class VideoListCreateAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, required=True,
#                                    help='No task title provided',
#                                    location='json')
#         self.reqparse.add_argument('description', type=str, default="",
#                                    location='json')
#         super(TaskListAPI, self).__init__()
#
#     def get(self):
#         return {'tasks': [marshal(task, task_fields) for task in tasks]}
#
#     def post(self):
#         args = self.reqparse.parse_args()
#         task = {
#             'id': tasks[-1]['id'] + 1,
#             'title': args['title'],
#             'description': args['description'],
#             'done': False
#         }
#         tasks.append(task)
#         return {'task': marshal(task, task_fields)}, 201
#
#
# class VideoAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()
#
#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}
#
#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}
#
#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}
#
# ############### Awards API resource ##################
#
# class AwardsListCreateAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, required=True,
#                                    help='No task title provided',
#                                    location='json')
#         self.reqparse.add_argument('description', type=str, default="",
#                                    location='json')
#         super(TaskListAPI, self).__init__()
#
#     def get(self):
#         return {'tasks': [marshal(task, task_fields) for task in tasks]}
#
#     def post(self):
#         args = self.reqparse.parse_args()
#         task = {
#             'id': tasks[-1]['id'] + 1,
#             'title': args['title'],
#             'description': args['description'],
#             'done': False
#         }
#         tasks.append(task)
#         return {'task': marshal(task, task_fields)}, 201
#
#
#
# class AwardsAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()
#
#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}
#
#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}
#
#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}
#
# ############### Actors API resource ##################
#
# class ActorsListCreateAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, required=True,
#                                    help='No task title provided',
#                                    location='json')
#         self.reqparse.add_argument('description', type=str, default="",
#                                    location='json')
#         super(TaskListAPI, self).__init__()
#
#     def get(self):
#         return {'tasks': [marshal(task, task_fields) for task in tasks]}
#
#     def post(self):
#         args = self.reqparse.parse_args()
#         task = {
#             'id': tasks[-1]['id'] + 1,
#             'title': args['title'],
#             'description': args['description'],
#             'done': False
#         }
#         tasks.append(task)
#         return {'task': marshal(task, task_fields)}, 201
#
#
#
# class ActorsAPI(Resource):
#     decorators = [auth.login_required]
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()
#
#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}
#
#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}
#
#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}
#
#

############### Genre API resource ##################

class GenreListCreateAPI(Resource):
    #decorators = [auth.login_required]

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

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        super(GenreAPI, self).__init__()

    def get(self, id):
        genre = Genre.query.get(id)
        genre_schema = GenreSchema(many=True)
        result = genre_schema.dump(genre)
        return {"genre_list": result.data}

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

api.add_resource(GenreListCreateAPI, '/movie_recommend/api/v1/genres', endpoint='genres')
api.add_resource(GenreAPI, '/movie_recommend/api/v1/genres/<int:id>', endpoint='genre_settings')