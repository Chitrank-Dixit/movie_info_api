from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
movie = Table('movie', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('film_industry_id', Integer),
    Column('name', String(length=80)),
    Column('genre', Integer),
)

video = Table('video', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('film_industry_id', Integer),
    Column('name', String(length=80)),
    Column('genre', Integer),
)

tv_series = Table('tv_series', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('film_industry_id', Integer),
    Column('name', String(length=80)),
    Column('genre', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['movie'].columns['film_industry_id'].create()
    post_meta.tables['video'].columns['film_industry_id'].create()
    post_meta.tables['tv_series'].columns['film_industry_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['movie'].columns['film_industry_id'].drop()
    post_meta.tables['video'].columns['film_industry_id'].drop()
    post_meta.tables['tv_series'].columns['film_industry_id'].drop()
