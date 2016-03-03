from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=80)),
    Column('first_name', VARCHAR(length=80)),
    Column('last_name', VARCHAR(length=80)),
    Column('password', VARCHAR(length=80)),
    Column('location', VARCHAR(length=80)),
    Column('email', VARCHAR(length=120)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=80)),
    Column('first_name', String(length=80)),
    Column('last_name', String(length=80)),
    Column('password', String(length=80)),
    Column('address', String(length=80)),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['location'].drop()
    post_meta.tables['user'].columns['address'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['location'].create()
    post_meta.tables['user'].columns['address'].drop()
