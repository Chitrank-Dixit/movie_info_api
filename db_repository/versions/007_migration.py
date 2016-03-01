from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_favourite_actoress = Table('user_favourite_actoress', pre_meta,
    Column('user_preferences_id', INTEGER),
    Column('actor_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_favourite_actoress'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_favourite_actoress'].create()
