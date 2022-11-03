from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, BadRequest, Success
from server.data.models import Company, JobAd, CompanyInfo, CompanyResponseModel, PersonalCompanyResponseModel
from server.services.company_service import get_company_info_by_id, get_company_by_id, edit_company, get_all_companies
from server.services.user_service import edit_user_info, get_town_id_by_name, valid_email
from server.services import company_service, job_ad_service


companies_router = APIRouter(prefix='/companies')

@companies_router.get('/')
def get_companies(search: str | None = None, search_by: str | None = None, sort: str | None = None, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    search_validation = ['company_name', 'town_name']

    if search_by and search_by not in search_validation:
        return BadRequest(f'Cannot search by parameter {search_by}.')

    if user:
        companies = company_service.get_all_companies(search, search_by)
    else:
        return Forbidden('Please log in!')

    if sort and (sort == 'asc' or sort == 'desc'):
        return company_service.sort(companies, reverse=sort == 'desc')
    else:
        if not companies:
            return NotFound('Your search returned no results!')

        return companies

@companies_router.get('/{id}')
def get_company_by_Id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    company = company_service.get_company_by_id(id)

    if company is None:
        return NotFound(f'Company with ID: {id} not found!')

    if user.id == id:
        return PersonalCompanyResponseModel(
            company= company,
            active_job_ads=job_ad_service.get_number_of_all_active_job_ads_by_company_id(id),
            list_of_matches=job_ad_service.get_list_of_matches(id)
            )

    else:
        return CompanyResponseModel(
            company= company,
            active_job_ads=job_ad_service.get_number_of_all_active_job_ads_by_company_id(id))

@companies_router.put('/{id}')
def edit_company_by_id(id: int, company: Company, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.id == id:
        return Forbidden('You do not have permission to change Company info!')

    if not valid_email(company.email):
        return BadRequest('Please enter a valid email address.')

    town_id = get_town_id_by_name(company.town_name)
    if not town_id:
        return NotFound(f'Town {company.town_name} is not a valid Bulgarian District Town name')
    
    error_msg = 'Your query is incorrect, please review your new info.'

    edited_user_info = edit_user_info(id, company.email, company.phone, company.address, town_id)
    
    if edited_user_info:
        edited_company = edit_company(id, company)
    else:
        return BadRequest(error_msg)
    
    if edited_company:
        return Success(f'Successfully updated info for {company.company_name} company!')
    else:
        return BadRequest(error_msg)