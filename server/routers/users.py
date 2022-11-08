from fastapi import APIRouter, Header
from server.common.auth import get_user_or_raise_401, create_token
from server.common.responses import BadRequest, Forbidden, NotFound, Success
from server.data.models import LoginData, User, Contact, Company, Professional, CompanyInfo, ProfessionalInfo, CompanyRegisterData, ProfessionalRegisterData
from server.data.models import ProfessionalResponse
from server.services import user_service, professional_service, company_service
from server.services import mailjet_service


users_router = APIRouter(prefix='/users')

@users_router.post('/professionals/register')
def register_professional(data: ProfessionalRegisterData, 
                        mandatory_user=user_service.mandatory_fields_user_contact,
                        mandatory_professional=user_service.mandatory_fields_professional):

    mandatory_response_user = mandatory_user(data.user_name, data.password, data.confirm_password, data.email, data.town_name)
    
    if mandatory_response_user:
        return mandatory_response_user
    
    mandatory_response_professional = mandatory_professional(data.first_name, data.last_name)

    if mandatory_response_professional:
        return mandatory_response_professional

    role = 'professional'

    town_id = user_service.get_town_id_by_name(data.town_name)
    if not town_id:
        return NotFound(f'Town {data.town_name} is not a valid Bulgarian District Town name')
    
    if user_service.email_exists(data.email):
        return BadRequest(f'Email address {data.email} is already used. Forgot password?')

    user = user_service.create_user(data.user_name,data.password,role,data.email,town_id,data.address,data.phone)
    if not user:
        return BadRequest(f'Username {data.user_name} is taken.')

    user_service.create_professional(user.id, data.first_name, data.last_name, data.summary)

    professional = professional_service.get_professional_by_id(user.id)

    if professional and professional.email == data.email:

        # mailjet_service.send_registration_email(professional.email, professional.first_name)

        return Success(f'Professional account created for {data.first_name} {data.last_name}. Please log in to continue.')
    #else think if the above may not be successful, if yes, delete the row in users (rollback)

@users_router.post('/companies/register')
def register_company(data: CompanyRegisterData,
                    mandatory_user=user_service.mandatory_fields_user_contact,
                    mandatory_company=user_service.mandatory_fields_company):

    mandatory_response_user = mandatory_user(data.user_name, data.password, data.confirm_password, data.email, data.town_name)
    
    if mandatory_response_user:
        return mandatory_response_user

    mandatory_response_company = mandatory_company(data.company_name, data.description, data.address)

    if mandatory_response_company:
        return mandatory_response_company

    role = 'company'

    town_id = user_service.get_town_id_by_name(data.town_name)
    if not town_id:
        return NotFound(f'Town {data.town_name} is not a valid Bulgarian District Town name')

    if user_service.email_exists(data.email):
        return BadRequest(f'Email address {data.email} is already used. Forgot password?')

    user = user_service.create_user(data.user_name,data.password,role,data.email,town_id,data.address,data.phone)
    if not user:
        return BadRequest(f'Username {data.user_name} is taken.')
    
    user_service.create_company(user.id, data.company_name, data.description)

    company = company_service.get_company_by_id(user.id)

    if company and company.email == data.email:
        return Success(f'Company account created for {data.company_name}. Please log in to continue.')


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.user_name, data.password)

    if user:
        token = create_token(user)
        return {'token': token,
                'role': user.role}
    
    else:
        return BadRequest('Invalid login data')




    
