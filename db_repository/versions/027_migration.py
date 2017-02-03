from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
token = Table('token', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_id', String(length=40), nullable=False),
    Column('user_id', Integer),
    Column('application_id', Integer),
    Column('token_type', String(length=40)),
    Column('access_token', String(length=40)),
    Column('refresh_token', String(length=40)),
    Column('expires', DateTime),
    Column('_scopes', Text),
)

grant = Table('grant', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('client_id', String(length=40), nullable=False),
    Column('code', String(length=255), nullable=False),
    Column('redirect_uri', String(length=255)),
    Column('expires', DateTime),
    Column('_scopes', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['token'].columns['client_id'].create()
    post_meta.tables['grant'].columns['client_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['token'].columns['client_id'].drop()
    post_meta.tables['grant'].columns['client_id'].drop()
