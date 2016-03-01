from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_film_industry = Table('user_film_industry', pre_meta,
    Column('user_id', INTEGER),
    Column('film_industry_id', INTEGER),
)

film_industry_users = Table('film_industry_users', post_meta,
    Column('user_id', Integer),
    Column('film_industry_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_film_industry'].drop()
    post_meta.tables['film_industry_users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_film_industry'].create()
    post_meta.tables['film_industry_users'].drop()
