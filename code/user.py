import sqlite3
from flask_restful import Resource, reqparse

DATABASE_NAME = "data.db"


class User:
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
                # user = cls(row[0], row[1], row[2])
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
                # user = cls(row[0], row[1], row[2])
                user = cls(*row)
            else:
                user = None
            return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="'username' filed cannot be blank"
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="'password' field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (null, ?, ?)"
            cursor.execute(query, (data["username"], data["password"]))
            connection.commit()
        return {"message": f"user {data['username']} created successfully."}, 201
