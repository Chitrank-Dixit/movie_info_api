__author__ = 'chitrankdixit'
from app import db, ma
from .models import User, UserPreferences, Genre, FilmIndustry, Movie


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','email')


class UserPreferencesSchema(ma.Schema):
    class Meta:
        model = UserPreferences
        fields = ('id', 'user')


class GenreSchema(ma.Schema):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class FilmIndustrySchema(ma.Schema):
    class Meta:
        model = FilmIndustry
        fields = ('name', 'location')

class MovieSchema(ma.Schema):
    class Meta:
        model = Movie
        fields = ('film_industry', 'name', 'genre', 'actor')