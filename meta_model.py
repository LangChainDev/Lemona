# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import *


def connect_db(db_info, schema_name):
    """
    :param db_info: dict, DataBase Information
    :param schema_name: str, schema name 
    :return: Connected engine and base 
    """
    # This is for PostgreSQL & psycopg2. You can change to what you use.
    url = 'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}'.format(**db_info)
    engine = create_engine(url, client_encoding='utf8')

    Base = declarative_base(metadata=MetaData(schema=schema_name))
    # Import the schema's information into metadata.
    Base.metadata.reflect(engine)
    return engine, Base


def init_db(engine, Base):
    """
    Only at the very beginning.
    I Think so... This need for only PostgreSQL.
    With 'OriginalBase' in 'Base', Alembic doesn't automatically make Sequence;(

    :return: Actually reflected in Database
    """
    return Base.metadata.create_all(engine)


def storeSQLfile(base):
    """
    :param base: what you want to store
    :return: SQL file
    """
    file_date = datetime.now().strftime('%Y%m%d_%H%M%S')
    tables = base.metadata.tables
    for table in tables.values():
        rawSQL = str(CreateTable(table))

        with open('./sql_files/schema_{}.sql'.format(file_date), 'a') as text_file:
            text_file.write(rawSQL)



# target schema name
SCHEMA_NAME = ''

# DEV_DATABASE: Development Database Information
DEV_DATABASE = {'user': '',
                'password': '',
                'host': '',
                'database': ''}
devEngine, DevBase = connect_db(DEV_DATABASE, SCHEMA_NAME)

# PROD_DATABASE: Product Database Information
PROD_DATABASE = {'user': '',
                 'password': '',
                 'host': '',
                 'database': ''}
prodEngine, ProdBase = connect_db(PROD_DATABASE, SCHEMA_NAME)

ProdBase.metadata = DevBase.metadata

# First Execute!
# init_db(prodEngine, ProdBase)

# If you want to get Raw SQL file, do it!
# storeSQLfile(ProdBase)
