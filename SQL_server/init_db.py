from sql import Database

def main():
    host = '192.168.220.5'
    user = 'postgres'
    password = 'Kyala'
    db_name = 'connection'
    database = Database(host, user, password, db_name)
    #Insert(database)
    print(Select(database))

def init_db(database:Database):
    database.create_db()
    database.Create_tables()

def Insert(database:Database):
    database.Insert('Smartphones', 'ip', 'connection', '127.0.0.1', False)
    database.Insert('Smartphones', 'ip', 'connection', '10.0.41.47', False)

def Select(database:Database):
    return database.Select_all('Smartphones')

if __name__ == '__main__':
    main()