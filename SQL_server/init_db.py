from sql import Database

def main():
    host = '127.0.0.1'
    user = 'postgres'
    password = 'Kyala'
    db_name = 'Connection'
    database = Database(host, user, password, db_name)
    #init_db(database)
    #Insert(database)
    print(Select(database))

def init_db(database:Database):
    database.Create_tables()

def Insert(database:Database):
    database.Insert('Smartphones', 'ip', 'connection', '127.0.0.1', False)
    database.Insert('Smartphones', 'ip', 'connection', '10.0.41.47', False)

def Select(database:Database):
    return database.Select_all('Smartphones')

if __name__ == '__main__':
    main()