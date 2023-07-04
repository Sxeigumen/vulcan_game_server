import psycopg2
import sys

host = '127.0.0.1'
user = 'postgres'
password = '*****'
db_name = 'Connection'

class Database:
    def __init__(self, host, user, password, db_name):
        self.connection = psycopg2.connect(host = host, user = user, password = password, database = db_name)
        self.connection.autocommit = True

    def Create_tables(self):
        try:
            #Create table controller
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE Controllers(
                id serial PRIMARY KEY,
                ip varchar(20) NOT NULL UNIQUE,
                connection boolean);""")
            #Create table smartphone
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE Smartphones(
                id serial PRIMARY KEY,
                ip varchar(20) NOT NULL,
                connection boolean);""")
            #Create table pair
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE Pairs(
                id serial PRIMARY KEY,
                id_controller int REFERENCES Controllers(id),
                id_smartphone int REFERENCES Smartphones(id));""")
        except Exception as er:
            self.Handler_Error(er)

    def Insert(self, table, poly_1, poly_2, value_1, value_2):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO {table} ({poly_1},{poly_2}) VALUES
                ('{value_1}','{value_2}');""")
        except Exception as er:
            self.Handler_Error(er)

    def Count(self, table):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT COUNT(*) FROM {table};""")
        except Exception as er:
            self.Handler_Error(er)

    def Select(self, table, poly_what = '*'):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {poly_what} FROM {table};""")
                raw = cursor.fetchone()
                return raw
        except Exception as er:
            self.Handler_Error(er)

    def Select(self, table, poly_where, value, poly_what = '*'):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {poly_what} FROM {table}
                              WHERE {poly_where} = '{value}';""")
                raw = cursor.fetchone()
                return raw
        except Exception as er:
            self.Handler_Error(er)

    def Select(self, table, poly_where, value1, value2, poly_what = '*'):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {poly_what} FROM {table}
                            WHERE {poly_where} IN ('{value1}','{value2}');""")
        except Exception as er:
            self.Handler_Error(er)

    def Handler_Error(self, error):
        self.connection.close()
        raise error

