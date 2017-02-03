from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
access_token = Table('access_token', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_key', String(length=40), nullable=False),
    Column('user_id', Integer),
    Column('token', String(length=255)),
    Column('secret', String(length=255)),
    Column('_realms', Text),
)

client = Table('client', post_meta,
    Column('name', String(length=40)),
    Column('description', String(length=400)),
    Column('user_id', Integer),
    Column('client_key', String(length=40), primary_key=True, nullable=False),
    Column('client_secret', String(length=55), nullable=False),
    Column('_realms', Text),
    Column('_redirect_uris', Text),
)

nonce = Table('nonce', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', Integer),
    Column('nonce', String(length=40)),
    Column('client_key', String(length=40), nullable=False),
    Column('request_token', String(length=50)),
    Column('access_token', String(length=50)),
)

request_token = Table('request_token', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('client_key', String(length=40), nullable=False),
    Column('token', String(length=255)),
    Column('secret', String(length=255), nullable=False),
    Column('verifier', String(length=255)),
    Column('redirect_uri', Text),
    Column('_realms', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['access_token'].create()
    post_meta.tables['client'].create()
    post_meta.tables['nonce'].create()
    post_meta.tables['request_token'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['access_token'].drop()
    post_meta.tables['client'].drop()
    post_meta.tables['nonce'].drop()
    post_meta.tables['request_token'].drop()
