from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'abc', '123'),
    User(5, 'tao', 'xyz'),
    User(7, 'katherine', 'peace')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id:u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    print(f"username = {username}")
    print(f"password = {password}")
    # print(f"user.password = {user.password}")
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    print(f"payload = {payload}")
    user_id = payload["identity"]
    print(f"user_id = {user_id}")
    return userid_mapping.get(user_id, None)
