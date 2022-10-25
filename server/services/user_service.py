from data import database
from data.database import insert_query, read_query, read_query_single_element, update_query
from data.models import Professional, Company, Role,User
from mariadb import IntegrityError
from datetime import date
import re

def _hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(user_name: str, get_data_func = database.read_query) -> User | None:
    data = get_data_func(
        'SELECT id, user_name, password FROM users WHERE user_name = ?',
        (user_name,))

    return next((User(id, user_name, password) for id, user_name, password in data), None)


