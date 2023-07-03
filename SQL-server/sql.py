import psycopg2
import sys

host = '127.0.0.1'
user = 'postgres'
password = '*****'
db_name = 'Connection'

try:
    #Connection cursor
    connection = psycopg2.connect(host = host, user = user, password = password, database = db_name)
    #connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        print(f'Server version: {cursor.fetchone()}')
    #Create table controller
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE Controllers(
        id serial PRIMARY KEY,
        ip varchar(20) NOT NULL UNIQUE,
        connection boolean);""")
        print('Succesfull controller')
    #Create table smartphone
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE Smartphones(
        id serial PRIMARY KEY,
        ip varchar(20) NOT NULL,
        connection boolean);""")
        print('Succesfull smartphone')
    #Create table pair
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE Pairs(
        id serial PRIMARY KEY,
        id_controller int REFERENCES Controllers(id),
        id_smartphone int REFERENCES Smartphones(id));""")
        print('Succesfull pair')
except Exception as e:
    print(f'{e} while working with PostreSQL')
    sys.exit(0)
finally:
    if connection:
        connection.close()
