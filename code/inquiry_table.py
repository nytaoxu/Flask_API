import sqlite3

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
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor.execute(query)
        print(cursor.fetchall())
        query = "SELECT * FROM users"
        cursor.execute(query)
        for i in cursor.fetchall():
            print(i)


if __name__ == "__main__":
    main()
