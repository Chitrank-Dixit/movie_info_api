from flask.ext.restful import Resource
from app import api, app, auth,db
from app import marshal
from flask.json import jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_restful import reqparse, Resource
from .models import User, UserPreferences, FilmIndustry
from .serializers import UserSchema

# # refer microblog app by miguelgrinberg to make models and views flask, just take care this
# # time we are building the API server not just a basic site and take care to use only class based
# # views only

# ############### Users and Login API resource ##################


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


api.add_resource(UsersListCreateAPI, '/movie_recommend/api/v1/users')


class UsersAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=bool, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('password', type=bool, location='json')
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
api.add_resource(UsersAPI, '/movie_recommend/api/v1/users/<int:id>', endpoint='user')
#
#
# ############### UserPreferences API resource ##################
#
# class UserPreferencesListCreateAPI(Resource):
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
#
#
# # ############### Movie API resource ##################
#
# class MovieListCreateAPI(Resource):
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
# class MovieAPI(Resource):
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
# ############### Genre API resource ##################
#
# class GenreListCreateAPI(Resource):
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
# class GenreAPI(Resource):
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
