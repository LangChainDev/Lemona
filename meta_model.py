# -*- coding: utf-8 -*-
import os
import re
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import *
import datetime

SCHEMA_NAME = ''

DEV_DATABASE = {'user': '',
                'password': '',
                'host': '',
                'database': ''}

PROD_DATABASE = {'user': '',
                'password': '',
                'host': '',
                'database': ''}


def connect_db(db_info, schema_name):
    """
    :param db_info: dict, DataBase Information
    :param schema_name: str, schema name 
    :return: Connected engine and base 
    """
    # This is for PostgreSQL & psycopg2. You can change to what you use.
    url = 'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}'.format(**db_info)
    engine = create_engine(url, client_encoding='utf8')
    conn = engine.connect()
    Base = declarative_base(metadata=MetaData(schema=schema_name))
    # Import the schema's information into metadata.
    Base.metadata.reflect(engine)
    return engine, Base, conn


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

def parseSequence():

    try:
        filenames = os.listdir(os.path.join(os.getcwd(), 'alembic/versions'))
        print(filenames)

        for filename in filenames:
            if "initial_migration" in filename:
                # 정규 표현식으로 sequence의 name을 파싱한다
                r = re.compile('(?<=nextval\(\S)\w+\S\w+')
                # alembic 하위 디렉토리인 versions 디렉토리에서 initial migration 파일을 읽는다
                with open(os.path.join(os.getcwd(), 'alembic/versions', filename)) as f:
                    # with open("./alembic/versions/86e58cf1c883_first.py", 'r') as f:
                    # 읽은 파일을 string 형태로 만든다.
                    data = f.read()
                    # sequence에 해당하는 문자열을 정규표현식으로 이용해 파싱한다.
                    parsed_sequence = r.findall(data)
                    # 파싱한 sequence name을 출력한다.
                    print(parsed_sequence)

                    return parsed_sequence

    except PermissionError:
        pass


def createSequence(conn, parsed_sequences):

    for parsed_sequence in parsed_sequences:
        sequence_info = parsed_sequence.split('.')
        schema_string = sequence_info[0]
        sequence_string = sequence_info[1]
        conn.execute(CreateSequence(Sequence(sequence_string, schema=schema_string)))


if __name__ == "__main__":


    engine, Base, conn = connect_db(PROD_DATABASE, SCHEMA_NAME)
    sequence_list = parseSequence()
    createSequence(conn, sequence_list)



# If you want to get Raw SQL file, do it!
# storeSQLfile(ProdBase)
