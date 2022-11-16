from fastapi import APIRouter, Header
from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, BadRequest, Success
from server.data.models import Company,CompanyResponseModel, PersonalCompanyResponseModel, CompanyMatchRequestResponse
from server.services.user_service import edit_user_info
from server.common.validations_and_methods import get_town_id_by_name, valid_email
from server.services.job_ad_service import get_all_active_job_ads_by_company_id, get_all_archived_job_ads_by_company_id
from server.services import company_service, job_ad_service, match_request_service, user_service, resume_service, professional_service
from server.common.mailjet_service import send_its_a_match


companies_router = APIRouter(prefix='/companies')

@companies_router.get('/')
def get_companies(search: str | None = None, search_by: str | None = None, sort: str | None = None, x_token=Header(None)):
    user = get_user_or_raise_401(x_token)

    search_validation = ['company_name', 'town_name']

    if search_by and search_by not in search_validation:
        return BadRequest(f'Cannot search by parameter {search_by}.')

    if user:
        companies = company_service.get_all_companies(search, search_by)
    else:
        return Unauthorized('Please log in!')
    
    if not companies:
        return NotFound('Your search returned no results!')

    if sort and (sort == 'asc' or sort == 'desc'):
        return company_service.sort(companies, reverse=sort == 'desc')

    return companies


@companies_router.get('/{id}')
def get_company_by_Id(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    company = company_service.get_company_by_id(id)

    if company is None:
        return NotFound(f'Company with ID: {id} not found!')

    if not user:
        return Forbidden('Please log in!')
    
    return CompanyResponseModel(
        company= company,
        active_job_ads=job_ad_service.get_number_of_all_active_job_ads_by_company_id(id))


@companies_router.get('/{id}/job_ads')
def get_companies_active_job_ads_by_Id(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    company = company_service.get_company_by_id(id)
    
    if not user:
        return Unauthorized('Please log in!')
    
    if not company:
        return Unauthorized(f'Company with ID: {id} not found!')
    
    job_ads = get_all_active_job_ads_by_company_id(id)

    if not job_ads:
        return NotFound(f'There are no active Job ads for company with ID: {id}')


    return PersonalCompanyResponseModel(
        company= company,
        active_job_ads=job_ad_service.get_number_of_all_active_job_ads_by_company_id(id),
        job_ads = job_ads)
    

@companies_router.get('/{id}/archived_job_ads')
def get_companies_archived_job_ads_by_Id(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    company = company_service.get_company_by_id(id)
    
    if not user:
        return Unauthorized('Please log in!')
    
    if not company:
        return Unauthorized(f'Company with ID: {id} not found!')
    
    if user.id == id:
        archived_job_ads = get_all_archived_job_ads_by_company_id(id)
    else:
        return Forbidden('You do not have permission to view these archived Job Ads.')

    if not archived_job_ads:
        return NotFound(f'There are no archived Job ads for company with ID: {id}')


    return PersonalCompanyResponseModel(
        company= company,
        active_job_ads=job_ad_service.get_number_of_all_active_job_ads_by_company_id(id),
        job_ads = archived_job_ads)
    

@companies_router.put('/{id}')
def edit_company_by_id(id: int, company: Company, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user.id == id:
        return Forbidden('You do not have permission to change Company info!')

    if not valid_email(company.email):
        return BadRequest('Please enter a valid email address.')

    town_id = get_town_id_by_name(company.town_name)
    if not town_id:
        return NotFound(f'Town {company.town_name} is not a valid Bulgarian District Town name')

    edited_user_info = edit_user_info(id, company.email, company.phone, company.address, town_id)
    
    if edited_user_info:
        edited_company = company_service.edit_company(id, company)
        if edited_company:
            return Success(f'Successfully updated info for {company.company_name} company!')
    else:
        return BadRequest('Your query is incorrect, please review your new info.')


@companies_router.get('/{id}/match_requests')
def get_match_requests(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot view the Match Requests of others.')

    match_requests = match_request_service.get_match_requests_by_company_id(user.id)

    if not match_requests:
        return NotFound('There are currently no match requests waiting for you.')

    return (CompanyMatchRequestResponse(id=match_request.id, 
                                            professional_name=user_service.get_professional_fullname_by_id(match_request.requestor_id),
                                            resume=resume_service.get_resume_by_id(match_request.resume_id),
                                            job_ad=job_ad_service.get_job_ad_by_id(match_request.job_ad_id
                                            )) for match_request in match_requests)


@companies_router.put('/{id}/match_requests/{match_request_id}')
def match_resume(id: int, match_request_id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot match this resume.')

    match_request = match_request_service.get_match_request_by_id(match_request_id)

    if not match_request:
        return NotFound('Match request not found.')

    professional = professional_service.get_professional_by_id(match_request.requestor_id)
    professional_full_name = f'{professional.first_name} {professional.last_name}'

    resume = resume_service.get_resume_by_id(match_request.resume_id)

    job_ad = job_ad_service.get_job_ad_by_id(match_request.job_ad_id)

    company = company_service.get_company_by_id(id)

    match_request_service.its_a_match(match_request_id)
    
    professional_service.make_professional_busy(professional.id)

    company_service.update_successful_matches(id)

    resume_service.make_resume_matched(match_request.resume_id)

    job_ad_service.make_job_ad_archived(match_request.job_ad_id)

    # send_its_a_match(professional.email, professional_full_name, resume.title, company.company_name, job_ad.title, False)
    return Success(f"You successfully matched {professional_full_name}'s Resume!")