from ..SQL_server.sql import Database

def init_db(database:Database):
    database.Create_tables()