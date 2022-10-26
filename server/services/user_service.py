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


def try_login(user_name: str, password: str) -> User | None:
    user = find_by_username(user_name)

    hashed_password = _hash_password(password)

    return user if user and user.password == hashed_password else None



def create_user(user_name: str, password: str, insert_data_func=database.insert_query) -> User | None:
    
    password = _hash_password(password)

    try:
        generated_id = insert_data_func(
            'INSERT INTO users(user_name, password, role) VALUES (?,?,?)',
            (user_name, password, Role.REGULAR))

        return User(id=generated_id, 
                    user_name=user_name, 
                    password='', 
                    role=Role.REGULAR)

    except IntegrityError:
        return None


def create_contact(email:str, address:str, town_id:int, phone:str=None, insert_data_func=database.insert_query) -> int | None:
#AGAIN TRY EXCEPT BLOCK BECAUSE EMAIL NEEDS TO BE UNIQUE CHANGE THIS IN DB!!
    try:
        generated_id = insert_data_func(
            'INSERT INTO contacts(email, phone, address, town_id) VALUES (?,?,?,?)',
            (email, address, town_id, phone))

        return generated_id

    except IntegrityError:
        return None


def get_town_id_by_name(town_name:str) -> int:
    town_id = (read_query_single_element('SELECT id from towns where name = ?', (town_name,)))[0]

    return town_id


#WE WILL USE THE ABOVE USER AND CONTACT IDS INTO THIS:
def create_professional(user_id: int, 
                        first_name:str, 
                        last_name:str,
                        contact_id, 
                        summary:str=None, 
                        image_url:str=None, 
                        insert_data_func=database.insert_query) -> Professional | None:
    
    generated_id = insert_data_func(
            '''INSERT INTO professionals
                            (user_id, 
                            first_name, 
                            last_name, 
                            summary,
                            image_url, contact_id) VALUES (?,?,?,?,?,?)''',
            (user_id, first_name, last_name, summary, image_url, contact_id))

    if generated_id:
        return Professional(user_id,first_name,last_name,summary,image_url)

def create_company(user_id: int, 
                        company_name:str, 
                        description:str,
                        contact_id, 
                        logo_url:str=None, 
                        insert_data_func=database.insert_query) -> Company | None:
    
    generated_id = insert_data_func(
            '''INSERT INTO professionals
                            (user_id, 
                            company_name, 
                            description, 
                            logo_url, contact_id) VALUES (?,?,?,?,?)''',
            (user_id, company_name, description, logo_url, contact_id))

    if generated_id:
        return Company(user_id,company_name,description,logo_url)


def valid_username(user_name: str):
    '''Expects a user name as string, and if valid, it will return it, otherwise it will return None.'''
    if len(user_name) < 2 or len(user_name) > 30:
        return None
    else:
        return user_name

def valid_email(email: str):
    '''Expects an email address as string, and if valid, it will return it, otherwise it will return None.'''
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return email
    else:
        return None


#ATTENTION: 
'''
LEFT TO DO:
- NEED TO FIX PROFESSIONAL AND COMPANY MODELS ADD CONTACT ID ONLY AND REMOVE USERNAME PASS 
FULL INFO IN RESPONSE MODELS
- CREATE RESPONSE MODELS FOR ABOVE
- GET PROFESSIONAL BY ID
- GET COMPANY BY ID
- GET USER BY ID (LESS INFO??)
- ROUTERS - REGISTER PROF, REGISTER COMP, LOG IN, ADMIN???
- UNIT TESTS
'''