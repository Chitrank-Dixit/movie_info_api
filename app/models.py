from . import db
import re
from hashlib import md5
from enum import Enum
from sqlalchemy.orm import validates
from sqlalchemy_utils.types.choice import ChoiceType

################ relationship table (many to many relationships) ###############

user_film_industry = db.Table('user_film_industry',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id'), nullable=True),
    db.Column('film_industry_id', db.Integer, db.ForeignKey('film_industry.id'), nullable=True)
)

user_favourite_actor = db.Table('user_favourite_actor',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id'), nullable=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True)
)

user_favourite_movies = db.Table('user_favourite_movies',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id'), nullable=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id') , nullable=True)
)

user_favourite_tv_series = db.Table('user_favourite_tv_series',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id'), nullable=True),
    db.Column('tv_series_id', db.Integer, db.ForeignKey('tv_series.id'), nullable=True)
)

user_favourite_videos = db.Table('user_favourite_videos',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id'), nullable=True),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), nullable=True)
)

################ User and User Preference related data ############




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    address = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username,first_name, last_name, password, address, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.address = address
        self.email = email

    # @validates('email')
    # def validate_email(self, email):
    #     assert '@' in self.email
    #     return self.email

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


    def __repr__(self):  # pragma: no cover
        return '<User %r>' % self.username


class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user_preferences')
    film_industry = db.relationship('FilmIndustry',
        secondary = user_film_industry,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('UserPreferences', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    favourite_actor = db.relationship('Actor',
        secondary = user_favourite_actor,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('UserPreferences', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    favourite_movies = db.relationship('Movie',
        secondary = user_favourite_movies,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('UserPreferences', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    favourite_tv_series = db.relationship('TVSeries',
        secondary = user_favourite_tv_series,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('UserPreferences', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    favourite_videos = db.relationship('Video',
        secondary = user_favourite_videos,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('UserPreferences', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )


    def __init__(self, user_id):
        self.user_id = user_id





################ relationship table (many to many relationships) ###############

tv_series_actors = db.Table('tv_series_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('tv_series_id', db.Integer, db.ForeignKey('tv_series.id'), nullable=True)
)


video_actors = db.Table('videos_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), nullable=True)
)


movie_actors = db.Table('movie_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), nullable=True)
)


########################### Film Industry ,Tv Series, Movie ,Video , Genre related data ###############

class FilmIndustry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __str__(self):
        pass



class TVSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_industry_id = db.Column(db.Integer, db.ForeignKey('film_industry.id'))
    film_industry = db.relationship('FilmIndustry', backref='tv_series')
    name = db.Column(db.String(80))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship('Genre', backref='tv_series')
    actor = db.relationship('Actor',
        secondary = tv_series_actors,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('TVSeries', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )

    def __init__(self, film_industry_id, name, genre_id):
        self.film_industry_id = film_industry_id
        self.name = name
        self.genre_id = genre_id

    def __str__(self):
        pass

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_industry_id = db.Column(db.Integer, db.ForeignKey('film_industry.id'))
    film_industry = db.relationship('FilmIndustry', backref='videos')
    name = db.Column(db.String(80))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship('Genre', backref='videos')
    actor = db.relationship('Actor',
        secondary = video_actors,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Video', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )

    def __init__(self, film_industry_id, name, genre_id):
        self.film_industry_id = film_industry_id
        self.name = name
        self.genre_id = genre_id

    def __str__(self):
        pass


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_industry_id = db.Column(db.Integer, db.ForeignKey('film_industry.id'))
    film_industry = db.relationship('FilmIndustry', backref='movies')
    name = db.Column(db.String(80))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship('Genre', backref='movies')
    actor = db.relationship('Actor',
        secondary = movie_actors,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Movie', lazy = 'dynamic'),
        # lazy = 'dynamic',
        )

    def __init__(self, film_industry_id, name, genre_id):
        self.film_industry_id = film_industry_id
        self.name = name
        self.genre_id = genre_id

    def __str__(self):
        pass


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self,name):
        self.name = name

    def __str__(self):
        pass


################ relationship table (many to many relationships) ###############

awarded_actors = db.Table('awarded_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'),nullable=True),
    db.Column('award_id', db.Integer, db.ForeignKey('award.id'), nullable=True),

)


###################### Awards , Awardsname related data ###################


class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    awarded_to = db.relationship('Actor',
        secondary = awarded_actors,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Award', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )

    def __init__(self,name):
        self.name = name

    def __str__(self):
        pass


################ relationship table (many to many relationships) ###############

actor_movies = db.Table('actor_movies',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), nullable=True),

)

actor_videos = db.Table('actor_video',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), nullable=True),

)

actor_tvseries = db.Table('actor_tvseries',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('tv_series_id', db.Integer, db.ForeignKey('tv_series.id'), nullable=True),

)

actor_awards = db.Table('actor_awards',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('award_id', db.Integer, db.ForeignKey('award.id'), nullable=True),

)

actor_relationship = db.Table('actor_relationship',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), nullable=True),

)

##################### Actor related data ##################

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    age = db.Column(db.Integer)
    date_of_birth = db.Column(db.DateTime)
    movies = db.relationship('Movie',
        secondary = actor_movies,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Actor', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    videos = db.relationship('Video',
        secondary = actor_videos,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Actor', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    tv_series = db.relationship('TVSeries',
        secondary = actor_tvseries,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Actor', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    awards = db.relationship('Award',
        secondary = actor_awards,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Actor', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )
    in_family_relation = db.relationship('Actor',
        secondary = actor_relationship,
        # primaryjoin = (tv_series_actors.c.actor_id == id),
        # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
        backref = db.backref('Actor', lazy = 'dynamic'),
        # lazy = 'dynamic'
        )

    def __init__(self,name, gender, age, date_of_birth):
        self.name = name
        self.gender = gender
        self.age = age
        self.date_of_birth = date_of_birth

    def __str__(self):
        pass
    

################### Token Authentication Model ##########################


class ClientType(Enum):
    Confidential = 1
    Public = 2

class AuthorizationGrantType(Enum):
    AuthorizationCode = 1
    Implicit = 2
    ResourceOwnerPasswordBased = 3
    ClientCredentials = 4


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(128), unique=True, index=True,
                              nullable=False)
    client_type = db.Column(ChoiceType(ClientType, impl=db.Integer()))
    authorization_grant_type = db.Column(ChoiceType(AuthorizationGrantType, impl=db.Integer()))

    # creator of the client, not required
    user_id = db.Column(db.ForeignKey('user.id'))
    # required if you need to support client credential
    user = db.relationship('User')

    # def generate_client_id(self):
    #     generated_client_id = self.client_id
    #     return generated_client_id
    #
    # def generate_client_secret(self):
    #     generated_client_secret = self.client_secret
    #     return generated_client_secret

    # @property
    # def client_type(self):
    #     if self.is_confidential:
    #         return 'confidential'
    #     return 'public'
    #
    # @property
    # def redirect_uris(self):
    #     if self._redirect_uris:
    #         return self._redirect_uris.split()
    #     return []
    #
    # @property
    # def default_scopes(self):
    #     if self._default_scopes:
    #         return self._default_scopes.split()
    #     return []


    # authorization_grant_type =
    # redirect_uris =


# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # human readable name, not required
#     name = db.Column(db.String(40))
#
#     # human readable description, not required
#     description = db.Column(db.String(400))
#
#     # creator of the client, not required
#     user_id = db.Column(db.ForeignKey('user.id'))
#     # required if you need to support client credential
#     user = db.relationship('User')
#
#     client_id = db.Column(db.String(40))
#     client_secret = db.Column(db.String(55), unique=True, index=True,
#                               nullable=False)
#
#     # public or confidential
#     is_confidential = db.Column(db.Boolean)
#
#     _redirect_uris = db.Column(db.Text)
#     _default_scopes = db.Column(db.Text)
#
#     @property
#     def client_type(self):
#         if self.is_confidential:
#             return 'confidential'
#         return 'public'
#
#     @property
#     def redirect_uris(self):
#         if self._redirect_uris:
#             return self._redirect_uris.split()
#         return []
#
#     @property
#     def default_redirect_uri(self):
#         return self.redirect_uris[0]
#
#     @property
#     def default_scopes(self):
#         if self._default_scopes:
#             return self._default_scopes.split()
#         return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    # client_id = db.Column(
    #     db.String(40), db.ForeignKey('client.client_id'),
    #     nullable=False,
    # )
    # client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    application_id = db.Column(db.ForeignKey('application.id'))
    application = db.relationship('Application')

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []





# class Token(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     client_id = db.Column(
#         db.String(40), db.ForeignKey('client.client_id'),
#         nullable=False,
#     )
#     client = db.relationship('Client')
#
#     user_id = db.Column(
#         db.Integer, db.ForeignKey('user.id')
#     )
#     user = db.relationship('User')
#
#     application_id = db.Column(
#         db.Integer, db.ForeignKey('application.id')
#     )
#     application = db.relationship('Application')
#
#     # currently only bearer is supported
#     token_type = db.Column(db.String(40))
#
#     access_token = db.Column(db.String(40), unique=True)
#     refresh_token = db.Column(db.String(40), unique=True)
#     expires = db.Column(db.DateTime)
#     _scopes = db.Column(db.Text)
#
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
#         return self
#
#     @property
#     def scopes(self):
#         if self._scopes:
#             return self._scopes.split()
#         return []


class AccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    application_id = db.Column(
        db.Integer, db.ForeignKey('application.id')
    )
    application = db.relationship('Application')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    token = db.Column(db.String(30), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    application_id = db.Column(
        db.Integer, db.ForeignKey('application.id')
    )
    application = db.relationship('Application')

    access_token_id = db.Column(
        db.Integer, db.ForeignKey('access_token.id')
    )

    access_token = db.relationship('AccessToken')
    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    token = db.Column(db.String(40), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []