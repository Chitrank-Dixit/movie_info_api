from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
application = Table('application', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=40)),
    Column('client_id', String(length=40), primary_key=True, nullable=False),
    Column('client_secret', String(length=128), nullable=False),
    Column('user_id', Integer),
)

client = Table('client', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=40)),
    Column('description', String(length=400)),
    Column('user_id', Integer),
    Column('client_id', String(length=40), primary_key=True, nullable=False),
    Column('client_secret', String(length=55), nullable=False),
    Column('is_confidential', Boolean),
    Column('_redirect_uris', Text),
    Column('_default_scopes', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['application'].columns['id'].create()
    post_meta.tables['client'].columns['id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['application'].columns['id'].drop()
    post_meta.tables['client'].columns['id'].drop()
