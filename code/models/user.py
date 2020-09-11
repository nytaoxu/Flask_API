import sqlite3

DATABASE_NAME = "data.db"


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            find_username_query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(find_username_query, (username, ))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None
            return user

    @classmethod
    def find_by_id(cls, _id):
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            find_id_query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(find_id_query, (_id, ))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None
            return user
