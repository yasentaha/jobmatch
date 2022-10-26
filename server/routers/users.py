from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound, Success
from data.models import LoginData, User, Contact, Company, Professional, CompanyInfo, ProfessionalInfo, CompanyRegisterData, ProfessionalRegisterData
from server.data.models import ProfessionalResponse
from services import user_service


users_router = APIRouter(prefix='/users')



def mandatory_fields_user_contact(user_name:str, password, confirm_password:str, email:str, address:str, town_name:str):
    if not user_name:
        return BadRequest('User Name field is mandatory!')
    
    if not user_service.valid_username(user_name):
        return BadRequest('Please enter a user name that is bigger than 2 and less than 30 symbols.')
        
    if not password:
        return BadRequest('Passowrd field is mandatory!')

    if not confirm_password:
        return BadRequest('Please confirm password.')
    
    if not user_service.password_confirmation(password, confirm_password):
        return BadRequest('Passwords do not match.')

    if not email:
        return BadRequest('Email field is mandatory!')

    if not user_service.valid_email(email):
        return BadRequest('Please enter a valid email address.')
#ATTENTION DO WE NEED ADDRESS TO BE MANDATORY??
    if not address:
        return BadRequest('Please enter your address.')
    
    if not town_name:
        return BadRequest('Town Name field is mandatory!')
    
    pass

def mandatory_fields_professional(first_name:str, last_name: str):
    if not first_name:
        return BadRequest('First Name field is mandatory!')

    if not last_name:
        return BadRequest('Last Name field is mandatory!')
    
def mandatory_fields_company(company_name:str, description: str):
    if not company_name:
        return BadRequest('Company Name field is mandatory!')

    if not description:
        return BadRequest('Description field is mandatory!')

    
