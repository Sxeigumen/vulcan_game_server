import psycopg2

class Database:
    def __init__(self, host, user, password, db_name):
        self.connection = psycopg2.connect(host = host, user = user, password = password, database = db_name)
        self.connection.autocommit = True

    def create_db(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE DATABASE Connection;""")
        except Exception as er:
            self.Handler_Error(er)
            
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

    def Update(self, table, poly, value, poly_where, value_where):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""UPDATE {table} SET {poly} = '{value}'
                               WHERE {poly_where} = '{value_where}';""")
        except Exception as er:
            self.Handler_Error(er)

    def Count(self, table):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT COUNT(*) FROM {table};""")
        except Exception as er:
            self.Handler_Error(er)

    def Select_all(self, table, poly_what = '*'):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {poly_what} FROM {table};""")
                raw = cursor.fetchall()
                return raw
        except Exception as er:
            self.Handler_Error(er)

    def Select_one(self, table, poly_where, value, poly_what = '*'):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {poly_what} FROM {table}
                              WHERE {poly_where} = '{value}';""")
                raw = cursor.fetchall()
                return raw
        except Exception as er:
            self.Handler_Error(er)

    def Select_two(self, table, poly_where, value1, value2, poly_what = '*'):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {poly_what} FROM {table}
                            WHERE {poly_where} IN ('{value1}','{value2}');""")
                raw = cursor.fetchall()
                return raw
        except Exception as er:
            self.Handler_Error(er)

    def Handler_Error(self, error):
        self.connection.close()
        raise error

