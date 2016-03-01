from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
movie = Table('movie', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('genre', INTEGER),
    Column('film_industry_id', INTEGER),
)

movie = Table('movie', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('film_industry_id', Integer),
    Column('name', String(length=80)),
    Column('genre_id', Integer),
)

video = Table('video', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('genre', INTEGER),
    Column('film_industry_id', INTEGER),
)

video = Table('video', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('film_industry_id', Integer),
    Column('name', String(length=80)),
    Column('genre_id', Integer),
)

tv_series = Table('tv_series', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('genre', INTEGER),
    Column('film_industry_id', INTEGER),
)

tv_series = Table('tv_series', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('film_industry_id', Integer),
    Column('name', String(length=80)),
    Column('genre_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['movie'].columns['genre'].drop()
    post_meta.tables['movie'].columns['genre_id'].create()
    pre_meta.tables['video'].columns['genre'].drop()
    post_meta.tables['video'].columns['genre_id'].create()
    pre_meta.tables['tv_series'].columns['genre'].drop()
    post_meta.tables['tv_series'].columns['genre_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['movie'].columns['genre'].create()
    post_meta.tables['movie'].columns['genre_id'].drop()
    pre_meta.tables['video'].columns['genre'].create()
    post_meta.tables['video'].columns['genre_id'].drop()
    pre_meta.tables['tv_series'].columns['genre'].create()
    post_meta.tables['tv_series'].columns['genre_id'].drop()
