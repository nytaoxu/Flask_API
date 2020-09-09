import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

DATABASE_NAME = "data.db"


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
        if UserModel.find_by_username(data["username"]):
            return {"message": f"A user with the username {data['username']} already exists."}, 400
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (null, ?, ?)"
            cursor.execute(query, (data["username"], data["password"]))
            connection.commit()
        return {"message": f"user {data['username']} created successfully."}, 201
