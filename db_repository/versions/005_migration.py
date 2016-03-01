from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_favourite_actor = Table('user_favourite_actor', post_meta,
    Column('user_preferences_id', Integer),
    Column('actor_id', Integer),
)

user_favourite_actoress = Table('user_favourite_actoress', post_meta,
    Column('user_preferences_id', Integer),
    Column('actor_id', Integer),
)

user_favourite_movies = Table('user_favourite_movies', post_meta,
    Column('user_preferences_id', Integer),
    Column('movie_id', Integer),
)

user_favourite_tv_series = Table('user_favourite_tv_series', post_meta,
    Column('user_preferences_id', Integer),
    Column('tv_series_id', Integer),
)

user_favourite_videos = Table('user_favourite_videos', post_meta,
    Column('user_preferences_id', Integer),
    Column('video_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_favourite_actor'].create()
    post_meta.tables['user_favourite_actoress'].create()
    post_meta.tables['user_favourite_movies'].create()
    post_meta.tables['user_favourite_tv_series'].create()
    post_meta.tables['user_favourite_videos'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_favourite_actor'].drop()
    post_meta.tables['user_favourite_actoress'].drop()
    post_meta.tables['user_favourite_movies'].drop()
    post_meta.tables['user_favourite_tv_series'].drop()
    post_meta.tables['user_favourite_videos'].drop()
