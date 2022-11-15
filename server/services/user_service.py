from server.data import database
from server.data.database import insert_query, read_query, read_query_single_element, update_query
from server.data.models import Professional, Company, Role,User
from server.common.responses import BadRequest, Forbidden, NotFound, Success
from mariadb import IntegrityError, DataError
from datetime import date
import re

from server.data.models import Contact


def _hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(user_name: str, get_data_func = database.read_query) -> User | None:
    data = get_data_func(
        'SELECT id, user_name, password, role FROM users WHERE user_name = ?',
        (user_name,))

    return next((User.from_query_result(*row) for row in data), None)

def try_login(user_name: str, password: str) -> User | None:
    user = find_by_username(user_name)

    hashed_password = _hash_password(password)

    return user if user and user.password == hashed_password else None



def create_user(user_name: str, 
                password: str, 
                role: str,
                email:str, 
                town_id:int,
                address:str=None,
                phone:str=None, 
                insert_data_func=database.insert_query) -> User | None:
    
    password = _hash_password(password)

    try:
        generated_id = insert_data_func(
            'INSERT INTO users(user_name, password, role, email, phone, address, town_id) VALUES (?,?,?,?,?,?,?)',
            (user_name, password, role, email, phone, address, town_id))


        return User(id=generated_id, 
                    user_name=user_name, 
                    password='', 
                    role=role,
                    email=email,
                    phone=phone,
                    address=address,
                    town_id=town_id)

    except IntegrityError:
        return None


def get_town_id_by_name(town_name:str, read_data_func=database.read_query_single_element) -> int:
    town_id = (read_data_func('SELECT id from towns where name = ?', (town_name,)))

    return town_id[0] if town_id else None


def create_professional(user_id: int, 
                        first_name:str, 
                        last_name:str,
                        summary:str=None,  
                        insert_data_func=database.insert_query) -> None:
    
    professional_id = insert_data_func(
            '''INSERT INTO professionals
                            (user_id, 
                            first_name, 
                            last_name, 
                            summary) VALUES (?,?,?,?)''',
            (user_id, first_name, last_name, summary))

def create_company(user_id: int, 
                        company_name:str, 
                        description:str,
                        insert_data_func=database.insert_query) -> None:
    
    company_id = insert_data_func(
            '''INSERT INTO companies
                            (user_id, 
                            company_name, 
                            description) VALUES (?,?,?)''',
            (user_id, company_name, description))

def get_user_by_id(id:int, get_data_func = database.read_query) -> User | None:
    data = get_data_func(
        'SELECT id, user_name, password, role FROM users WHERE id = ?',
        (id,))

    return next((User(id=id, user_name=user_name, password='', role=role) for id, user_name, password, role in data), None)

def get_professional_fullname_by_id(professional_id:int) -> str:
    full_name_tuple = read_query_single_element('''SELECT first_name, last_name
                                            FROM professionals
                                            where user_id=?''', (professional_id,))
    full_name = full_name_tuple[0] + ' ' + full_name_tuple[1]

    return full_name

def get_company_name_by_id(company_id:int) -> str:
    company_name_tuple = read_query_single_element('''SELECT company_name
                                            FROM companies
                                            where user_id=?''', (company_id,))

    company_name = company_name_tuple[0]

    return company_name

def edit_user_info(id: int, email:str, phone:str, address:str, town_id:int, update_data_func=database.update_query) -> int:
    try:
        edited_info = update_data_func('''
                                    UPDATE users 
                                    SET email = ?, phone = ?, address = ?, town_id = ?
                                    WHERE id = ?''', (email, phone, address, town_id, id))
        return True
    
    except DataError:
        return False

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


def password_confirmation(password:str, confirm_password:str):
    return password == confirm_password

def email_exists(email: str):
    data = read_query('SELECT 1 from users where email = ?', (email,))

    return any(data)


def mandatory_fields_user_contact(user_name:str, password, confirm_password:str, email:str, town_name:str):
    if not user_name:
        return BadRequest('User Name field is mandatory!')
    
    if not valid_username(user_name):
        return BadRequest('Please enter a user name that is bigger than 2 and less than 30 symbols.')
        
    if not password:
        return BadRequest('Passowrd field is mandatory!')

    if not confirm_password:
        return BadRequest('Please confirm password.')
    
    if not password_confirmation(password, confirm_password):
        return BadRequest('Passwords do not match.')

    if not email:
        return BadRequest('Email field is mandatory!')

    if not valid_email(email):
        return BadRequest('Please enter a valid email address.')
    
    if not town_name:
        return BadRequest('Town Name field is mandatory!')
    
    return None

def mandatory_fields_professional(first_name:str, last_name: str):
    if not first_name:
        return BadRequest('First Name field is mandatory!')

    if not last_name:
        return BadRequest('Last Name field is mandatory!')

    return None

    
def mandatory_fields_company(company_name:str, description: str, address:str):
    if not company_name:
        return BadRequest('Company Name field is mandatory!')

    if not description:
        return BadRequest('Description field is mandatory!')
    
    if not address:
        return BadRequest('Please enter your address.')
    return None


