from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', post_meta,
    Column('created_at', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x10ba553d0; current_timestamp>)),
    Column('modified_at', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x10ba55690; current_timestamp>), default=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x10ba55590; current_timestamp>)),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
    Column('description', String(length=255)),
)

roles_users = Table('roles_users', post_meta,
    Column('user_id', Integer),
    Column('role_id', Integer),
)

user = Table('user', post_meta,
    Column('created_at', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x10ba553d0; current_timestamp>)),
    Column('modified_at', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x10ba55690; current_timestamp>), default=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x10ba55590; current_timestamp>)),
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
    post_meta.tables['role'].create()
    post_meta.tables['roles_users'].create()
    post_meta.tables['user'].columns['created_at'].create()
    post_meta.tables['user'].columns['modified_at'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].drop()
    post_meta.tables['roles_users'].drop()
    post_meta.tables['user'].columns['created_at'].drop()
    post_meta.tables['user'].columns['modified_at'].drop()
