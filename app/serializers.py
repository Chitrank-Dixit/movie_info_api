__author__ = 'chitrankdixit'
from app import db, ma
from .models import User, UserPreferences, Genre, FilmIndustry, Movie, Video, TVSeries, Award ,Actor, Application, \
    Grant


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','email','address')


class GenreSchema(ma.Schema):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class FilmIndustrySchema(ma.Schema):
    class Meta:
        model = FilmIndustry
        fields = ('id', 'name', 'location')


class ActorSchema(ma.Schema):
    class Meta:
        model = Actor
        fields = ('id','name', 'gender', 'age','date_of_birth')


class MovieSchema(ma.Schema):
    class Meta:
        model = Movie
        fields = ('id', 'film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema, many=True)


class VideoSchema(ma.Schema):
    class Meta:
        model = Video
        fields = ('id', 'film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema, many=True)


class TVSeriesSchema(ma.Schema):
    class Meta:
        model = TVSeries
        fields = ('id', 'film_industry', 'name', 'genre', 'actor')

    film_industry = ma.Nested(FilmIndustrySchema)
    genre = ma.Nested(GenreSchema)
    actor = ma.Nested(ActorSchema, many=True)


class AwardsSchema(ma.Schema):
    class Meta:
        model = Award
        fields = ('id', 'name', 'awarded_to')

    awarded_to = ma.Nested(ActorSchema)


class UserPreferencesSchema(ma.Schema):
    class Meta:
        model = UserPreferences
        fields = ('id', 'user', 'film_industry','favourite_actor','favourite_movies','favourite_tv_series','favourite_videos' )

    user = ma.Nested(UserSchema)
    film_industry = ma.Nested(FilmIndustrySchema, many=True)
    favourite_actor = ma.Nested(ActorSchema, many=True)
    favourite_movies = ma.Nested(MovieSchema, many=True)
    favourite_tv_series = ma.Nested(TVSeriesSchema, many=True)
    favourite_videos = ma.Nested(VideoSchema, many=True)


class ApplicationSchema(ma.Schema):
    class Meta:
        model = Application
        fields = ('id', 'name', 'client_id', 'client_secret', 'user')
    # required if you need to support client credential

    user = ma.Nested(UserSchema)




class GrantSchema(ma.Schema):
    class Meta:
        model = Grant
        fields = ('code', '_scopes')