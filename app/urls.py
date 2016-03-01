from app import api
from views import UsersListCreateAPI #MovieAPI, MovieListCreateAPI

api.add_resource(UsersListCreateAPI, '/movie_recommend/api/v1/users')
# api.add_resource(MovieAPI, '/movie_recommend/api/v1.0/movies/<int:id>', endpoint='movie')