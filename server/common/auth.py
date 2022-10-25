from datetime import date, datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from data.models import Professional, Company, User
from services.user_service import find_by_username
from data.database import read_query

SECRET_KEY = 'secret'
ALGORITHM = 'HS256'


def create_token(user: User) -> str:
    to_encode = {'user_name': user.user_name}

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decode_username_from_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_name: str = payload.get('user_name')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    
    return user_name


def from_token(token: str) -> User | None:
    return find_by_username(decode_username_from_token(token))


def is_authenticated(token) -> bool:
    user_name = decode_username_from_token(token)

    return any(read_query('SELECT 1 FROM users where user_name = ?', (user_name,)))


def get_user_or_raise_401(token: str) -> User:
    if not is_authenticated(token):
        raise HTTPException(status_code=401)
    
    return from_token(token)



