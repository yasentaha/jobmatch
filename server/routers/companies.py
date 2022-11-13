from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, BadRequest, Success
from server.data.models import Company, JobAd, CompanyInfo, CompanyResponseModel, PersonalCompanyResponseModel, CompanyMatchRequestResponse
from server.services.company_service import get_company_info_by_id, get_company_by_id, edit_company, get_all_companies
from server.services.user_service import edit_user_info, get_town_id_by_name, valid_email
from server.services import company_service, job_ad_service, match_request_service, user_service, resume_service, professional_service


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


@companies_router.get('/{id}/match_requests')
def get_match_requests(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot view the Match Requests of others.')

    match_requests = match_request_service.get_match_requests_by_company_id(user.id)

    if not match_requests:
        return NotFound('There are currently no match requests waiting for you.')

    return (CompanyMatchRequestResponse(match_request.id, 
                                            user_service.get_professional_fullname_by_id(match_request.requestor_id),
                                            resume_service.get_resume_by_id(match_request.resume_id,
                                            job_ad_service.get_job_ad_by_id(match_request.job_ad_id
                                            ))) for match_request in match_requests)


@companies_router.put('/{id}/match_requests/{match_request_id}')
def match_resume(id: int, match_request_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot match this resume.')

    match_request = match_request_service.get_match_request_by_id(match_request_id)

    if not match_request:
        return NotFound('Match request not found.')

    professional = professional_service.get_professional_by_id(match_request.requestor_id)

    match_request_service.its_a_match(match_request_id)
    
    #update professional to busy
    professional_service.make_professional_busy(professional.id)

    #update company's successful matches +1
    company_service.update_successful_matches(id)

    #Resume status -> Matched
    resume_service.make_resume_matched(match_request.resume_id)

    #JobAd status -> Archived
    job_ad_service.make_job_ad_archived(match_request.job_ad_id)

    #send email to professional - its a match!
    return Success(f"You successfully matched {professional.first_name} {professional.last_name}'s Resume!")