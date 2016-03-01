from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_film_industry = Table('user_film_industry', pre_meta,
    Column('user_id', INTEGER),
    Column('film_industry_id', INTEGER),
)

user_film_industry = Table('user_film_industry', post_meta,
    Column('user_preferences_id', Integer),
    Column('film_industry_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_film_industry'].columns['user_id'].drop()
    post_meta.tables['user_film_industry'].columns['user_preferences_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_film_industry'].columns['user_id'].create()
    post_meta.tables['user_film_industry'].columns['user_preferences_id'].drop()
