from . import db
import re
from hashlib import md5
from sqlalchemy.orm import validates

################ relationship table (many to many relationships) ###############

user_film_industry = db.Table('user_film_industry',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id')),
    db.Column('film_industry_id', db.Integer, db.ForeignKey('film_industry.id'))
)

user_favourite_actor = db.Table('user_favourite_actor',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

# user_favourite_actoress = db.Table('user_favourite_actoress',
#     db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id')),
#     db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
# )

user_favourite_movies = db.Table('user_favourite_movies',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
)

user_favourite_tv_series = db.Table('user_favourite_tv_series',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id')),
    db.Column('tv_series_id', db.Integer, db.ForeignKey('tv_series.id'))
)

user_favourite_videos = db.Table('user_favourite_videos',
    db.Column('user_preferences_id', db.Integer, db.ForeignKey('user_preferences.id')),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'))
)

################ User and User Preference related data ############




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    location = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username,first_name, last_name, password, location, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.location = location
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
    # favourite_actress = db.relationship('Actor',
    #     secondary = user_favourite_actoress,
    #     # primaryjoin = (tv_series_actors.c.actor_id == id),
    #     # secondaryjoin = (tv_series_actors.c.tv_series_actors_id == id),
    #     backref = db.backref('UserPreferences', lazy = 'dynamic'),
    #     # lazy = 'dynamic'
    #     )
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
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('tv_series_id', db.Integer, db.ForeignKey('tv_series.id'))
)


video_actors = db.Table('videos_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'))
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
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('award_id', db.Integer, db.ForeignKey('award.id')),

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
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),

)

actor_videos = db.Table('actor_video',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id')),

)

actor_tvseries = db.Table('actor_tvseries',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('tv_series_id', db.Integer, db.ForeignKey('tv_series.id')),

)

actor_awards = db.Table('actor_awards',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('award_id', db.Integer, db.ForeignKey('award.id')),

)

actor_relationship = db.Table('actor_relationship',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),

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
    

