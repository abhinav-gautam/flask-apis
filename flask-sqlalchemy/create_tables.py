import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# insert_item = "INSERT INTO items VALUES (NULL,?,?)"
# cursor.execute(insert_item, ('test', 12))

# insert_item = "INSERT INTO users VALUES (NULL,?,?)"
# cursor.execute(insert_item, ('test', 'test'))

get_all_users = "SELECT * FROM users"
print('Users')
for row in cursor.execute(get_all_users):
    print(row)

get_all_items = "SELECT * FROM items"
print('Items')
for row in cursor.execute(get_all_items):
    print(row)

connection.commit()
connection.close()
