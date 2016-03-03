__author__ = 'chitrankdixit'
from app import db, ma
from .models import User, UserPreferences, Genre, FilmIndustry, Movie, Video, TVSeries,Actor


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


class ActorSchema(ma.Schema):
    class Meta:
        model = Actor
        fields = ('name', 'gender', 'age')


class MovieSchema(ma.Schema):
    class Meta:
        model = Movie
        fields = ('film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema)


class VideoSchema(ma.Schema):
    class Meta:
        model = Video
        fields = ('film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema)


class TVSeriesSchema(ma.Schema):
    class Meta:
        model = TVSeries
        fields = ('film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema)
