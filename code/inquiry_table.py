import sqlite3

def print_db_result(cursor):
    try:
        for i in cursor.fetchall():
            print(i)
    except Exception as e:
        print(f"Exception in print_db_result(cursor): {e}")

def main():
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        # query = "INSERT INTO users VALUES (?, ?, ?)"
        # users = [
        #     (1, 'Tao', 'xyz'),
        #     (2, 'Katherine', 'abc')
        # ]
        # cursor.executemany(query, users)
        # connection.commit()
        query = "SELECT * FROM sqlite_master WHERE type='table';"
        cursor.execute(query)
        print_db_result(cursor)

        query = "SELECT * FROM users"
        cursor.execute(query)
        print_db_result(cursor)

        query = "SELECT * FROM items"
        cursor.execute(query)
        print_db_result(cursor)


if __name__ == "__main__":
    main()
