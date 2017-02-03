from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
application = Table('application', post_meta,
    Column('name', String(length=40)),
    Column('client_id', String(length=40), primary_key=True, nullable=False),
    Column('client_secret', String(length=55), nullable=False),
    Column('user_id', Integer),
)

token = Table('token', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('client_id', VARCHAR(length=40), nullable=False),
    Column('user_id', INTEGER),
    Column('token_type', VARCHAR(length=40)),
    Column('access_token', VARCHAR(length=255)),
    Column('refresh_token', VARCHAR(length=255)),
    Column('expires', DATETIME),
    Column('_scopes', TEXT),
)

grant = Table('grant', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('client_id', VARCHAR(length=40), nullable=False),
    Column('code', VARCHAR(length=255), nullable=False),
    Column('redirect_uri', VARCHAR(length=255)),
    Column('expires', DATETIME),
    Column('_scopes', TEXT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['application'].create()
    pre_meta.tables['token'].columns['client_id'].drop()
    pre_meta.tables['grant'].columns['client_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['application'].drop()
    pre_meta.tables['token'].columns['client_id'].create()
    pre_meta.tables['grant'].columns['client_id'].create()
