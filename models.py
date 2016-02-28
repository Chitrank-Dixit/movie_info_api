from app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

################ User and User Preference related data ############

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    location = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    film_industry = # multiple choice 'bollywood', 'hollywood' many to many 
    favourite_actor = # multiple choice 'bollywood', 'hollywood' many to many 
    favourite_actress = # multiple choice 'bollywood', 'hollywood' many to many 
    favourite_movies = # multiple choice 'bollywood', 'hollywood' many to many 
    favourite_tv_series = # multiple choice 'bollywood', 'hollywood' many to many 
    favourite_videos = # multiple choice 'bollywood', 'hollywood' many to many 




    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


########################### Tv Series, Movie and Video related data ###############

class TVSeries(db.class MODELNAME(models.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = # name of the movie
	genre = # genre of the movie
	actor = # many to many rel 




    class Meta:
        verbose_name = "MODELNAME"
        verbose_name_plural = "MODELNAMEs"

    def __str__(self):
        pass
    )

class Video(db.class MODELNAME(models.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = # name of the movie
	genre = # genre of the movie
	actor = # many to many rel 




    class Meta:
        verbose_name = "MODELNAME"
        verbose_name_plural = "MODELNAMEs"

    def __str__(self):
        pass
    )

class Movie(db.class MODELNAME(models.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = # name of the movie
	genre = # genre of the movie
	actor = # many to many rel 




    class Meta:
        verbose_name = "MODELNAME"
        verbose_name_plural = "MODELNAMEs"

    def __str__(self):
        pass
    )




###################### Awards , Awardsname related data ###################


class Awards(db.class MODELNAME(models.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = # name of the awards
	awarded_to = # many to many relationship with actor


    class Meta:
        verbose_name = "MODELNAME"
        verbose_name_plural = "MODELNAMEs"

    def __str__(self):
        pass
    )


##################### Actor related data ##################

class Actor(db.class MODELNAME(models.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = # name of actor
	gender = # gender of actor
	age = # age of the actor
	date_of_birth = # date of birth of the actor
	movies = # many to many relationship
	videos = # many to many relationship
	tv_series = # many to many relationship
	awards = # number of awards many to many rel
	in_family_relation = # the actor who is the member of the current actor family (self many to many relationship)


    class Meta:
        verbose_name = "MODELNAME"
        verbose_name_plural = "MODELNAMEs"

    def __str__(self):
        pass
    )

