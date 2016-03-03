__author__ = 'chitrankdixit'
from app import db, ma
from .models import User, UserPreferences, Genre, FilmIndustry, Movie, Video, TVSeries, Award ,Actor


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
        fields = ('id','name', 'location')


class ActorSchema(ma.Schema):
    class Meta:
        model = Actor
        fields = ('id','name', 'gender', 'age','date_of_birth')


class MovieSchema(ma.Schema):
    class Meta:
        model = Movie
        fields = ('id','film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema)


class VideoSchema(ma.Schema):
    class Meta:
        model = Video
        fields = ('id','film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema)


class TVSeriesSchema(ma.Schema):
    class Meta:
        model = TVSeries
        fields = ('id','film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema)


class AwardsSchema(ma.Schema):
    class Meta:
        model = TVSeries
        fields = ('id', 'name', 'awarded_to')

    awarded_to = ma.Nested(ActorSchema)