import sqlite3

def main():
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        create_table_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
        cursor.execute(create_table_query)
        create_table_query = "CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)"
        cursor.execute(create_table_query)
        # insert_query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(insert_query, ("GoPro", "399.97"))
        connection.commit()


if __name__ == "__main__":
    main()
