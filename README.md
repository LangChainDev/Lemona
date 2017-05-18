# Lemona

DB catalog exporter in SQLAlchemy form.

Lemona is a tool that uses sqlalchemy metadata to export database catalog in sqlalchemy format.



After exporting the db schema using lemona, you can use alembic to manage the migration.



## Dependency

- python3.6 


- sqlalchemy
- alembic(optional)




## How to use

### Postgresql

PostgreSQL requires that you set up a schema when there are multiple schemas in the database.

```python
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
```

When you run **meta_model.py**, the schema information in DEV_DATABASE is exported to PROD_DATABASE.

```shell
$ python3 meta_model.py
```



















