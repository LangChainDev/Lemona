# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import *


def connect_db(db_info, schema_name):
    """
    :param db_info: DB 정보 딕셔너리
    :param schema_name: 복사할 schema 이름
    :return: 연결된 Base 
    """
    url = 'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}'.format(**db_info)
    engine = create_engine(url, client_encoding='utf8')

    Base = declarative_base(metadata=MetaData(schema=schema_name))
    Base.metadata.reflect(engine)
    return engine, Base


def init_db(engine, Base):
    """
    **DB 초기화**
    아주 맨 처음에 DB를 복사해서 만들 떄 실행시켜주세요.
    처음에 초기화할때는 Alembic을 사용하지 않고, 그냥 바로 create! sequence를 새로 만드는 것까진 안되기 때문입니다.
    > postgreSQL이라서 그런듯?

    :return: 새로운 DB 생성!
    """
    return Base.metadata.create_all(engine)


"""
SCHEMA_NAME: 복사할 schema
ORIGINAL_DATABASE: 복사할 DB 정보
DATABASE: 만들어질 DB 정보
"""
SCHEMA_NAME = ''
ORIGINAL_DATABASE = {'user': '',
                     'password': '',
                     'host': '',
                     'database': ''}
original_engine, OriginalBase = connect_db(ORIGINAL_DATABASE, SCHEMA_NAME)

DATABASE = {'user': '',
            'password': '',
            'host': '',
            'database': ''}
engine, Base = connect_db(DATABASE, SCHEMA_NAME)

Base.metadata = OriginalBase.metadata
init_db(engine, Base)


# SQL문으로 출력됨
# tables = Base.metadata.tables
# for t in tables.values():
#     copy_table = str(CreateTable(t))
#     print(copy_table)
