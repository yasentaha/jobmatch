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




