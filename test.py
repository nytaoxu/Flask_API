import sqlite3


def main():
    try:
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            create_table = "CREATE TABLE users(id int, username text, password text);"
            cursor.execute(create_table)
            insert_data = "INSERT INTO users VALUES(?, ?, ?)"
            users = [
                (1, 'Tao', 'xyz'),
                (2, 'Katherine', 'abc')
            ]
            # cursor.execute(insert_data, (1, 'Tao', 'xyz'))
            # cursor.execute(insert_data, (2, 'Katherine', 'abc'))
            cursor.executemany(insert_data, users)
            connection.commit()

            inquiry = "SELECT * FROM users;"
            for i in cursor.execute(inquiry):
                # print(type(i))
                print(i)

            # x = cursor.fetchall()
            # print(x)
            # print(type(x))
            

    except Exception as e:
        print(f"Exception in main(): {e}")


if __name__ == "__main__":
    main()
