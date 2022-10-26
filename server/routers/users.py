from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound, Success
from data.models import LoginData, User, Contact, Company, Professional, CompanyInfo, ProfessionalInfo, CompanyRegisterData, ProfessionalRegisterData
from server.data.models import CompanyResponse, ProfessionalResponse
from services import user_service


users_router = APIRouter(prefix='/users')

@users_router.post('/professionals/register')
def register_professional(data: ProfessionalRegisterData):

    mandatory_fields_user_contact(data.user_name, data.password, data.confirm_password, data.email, data.address, data.town_name)
    
    mandatory_fields_professional(data.first_name, data.last_name)

    town_id = user_service.get_town_id_by_name(data.town_name)
    if not town_id:
        return NotFound(f'Town {data.town_name} is not a valid Bulgarian District Town name')

    user = user_service.create_user(data.user_name, data.password)
    if not user:
        return BadRequest(f'Username {data.user_name} is taken.')

    contact = user_service.create_contact(data.email, data.address, town_id, data.phone)
    if not contact:
            return BadRequest(f'User with {data.email} already exists.')
    
    professional = user_service.create_professional(user.id, data.first_name, data.last_name, contact.id, data.summary, data.image_url)

    return ProfessionalResponse(professional.id, 
                                user.user_name, 
                                professional.first_name,
                                professional.last_name,
                                professional.summary,
                                professional.image_url,
                                contact.email,
                                contact.phone,
                                contact.address,
                                data.town_name)

@users_router.post('/companies/register')
def register_company(data: CompanyRegisterData):

    mandatory_fields_user_contact(data.user_name, data.password, data.confirm_password, data.email, data.address, data.town_name)
    
    mandatory_fields_company(data.company_name, data.description)

    town_id = user_service.get_town_id_by_name(data.town_name)
    if not town_id:
        return NotFound(f'Town {data.town_name} is not a valid Bulgarian District Town name')

    user = user_service.create_user(data.user_name, data.password)
    if not user:
        return BadRequest(f'Username {data.user_name} is taken.')

    contact = user_service.create_contact(data.email, data.address, town_id, data.phone)
    if not contact:
            return BadRequest(f'User with {data.email} already exists.')
    
    company = user_service.create_company(user.id, data.company_name, data.description, contact.id, data.logo_url)

    return CompanyResponse(company.id,
                            user.user_name,
                            company.company_name,
                            company.description,
                            company.logo_url,
                            contact.email,
                            contact.phone,
                            contact.address,
                            data.town_name)


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.user_name, data.password)

    if user:
        token = create_token(user)
        return {'token': token}
    
    else:
        return BadRequest('Invalid login data')


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

    pass

    
def mandatory_fields_company(company_name:str, description: str):
    if not company_name:
        return BadRequest('Company Name field is mandatory!')

    if not description:
        return BadRequest('Description field is mandatory!')

    pass

    
