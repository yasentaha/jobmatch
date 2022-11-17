from fastapi import APIRouter, Header
from pydantic import BaseModel
from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, Success, BadRequest
from server.data.models import (Professional, ResumeWithSkillsResponseModel, Role, 
                                ResumeWithoutDescriptionAndSalaryResponse, ProfessionalMatchRequestResponse, 
                                ProfessionalResponseModel)
from server.services import professional_service, resume_service, user_service, match_request_service, job_ad_service, company_service
from server.services.professional_service import edit_professional, get_professional_by_id
from server.services.user_service import edit_user_info
from server.common.validations_and_methods import get_town_id_by_name, valid_email


professionals_router = APIRouter(prefix='/professionals')


@professionals_router.get('/')
def get_professionals(search: str | None = None, search_by: str | None = None, sort: str | None = None, x_token=Header(None)):
    user = get_user_or_raise_401(x_token)

    search_validation = ['first_name', 'last_name', 'town_name', 'busy']

    if search_by and search_by not in search_validation:
        return BadRequest(f'Cannot search by parameter {search_by}.')

    if user:
        professionals = professional_service.all(search, search_by)
    else:
        return Forbidden('Please log in!')

    if sort and (sort == 'asc' or sort == 'desc'):
        return professional_service.sort(professionals, reverse=sort == 'desc')
    
    else:
        if not professionals:
            return NotFound('Your search returned no results!')

        return professionals


@professionals_router.get('/{id}')
def professional_by_id(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    professional = get_professional_by_id(id)

    if professional is None:
        return NotFound('Professional not found!')

    return ProfessionalResponseModel(
            professional=professional,
            active_resumes=resume_service.get_number_of_all_active_resumes(id))


@professionals_router.put('/{id}')
def edit_professional_by_id(id: int, professional: Professional, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if not user.id == id:
        return Forbidden('You do not have permission to change Professional info!')

    if not valid_email(professional.email):
        return BadRequest('Please enter a valid email address.')

    town_id = get_town_id_by_name(professional.town_name)
    if not town_id:
        return NotFound(f'Town {professional.town_name} is not a valid Bulgarian District Town name')

    edited_user_info = edit_user_info(id, professional.email, professional.phone, professional.address, town_id)
    
    if edited_user_info:
        edited_professional = edit_professional(id, professional)
        if edited_professional:
            return Success(f'Successfully updated info for professional with name {professional.first_name} {professional.last_name}!')
    else:
        return BadRequest('Your query is incorrect, please review your new info.')


@professionals_router.get('/{id}/resumes')
def professional_by_id(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if user:
        if user.id == id:
            resumes = resume_service.get_all_resumes_by_professional_id(id)
            resumes_full = [ResumeWithSkillsResponseModel(full_name=user_service.get_professional_fullname_by_id(resume.professional_id), 
                resume=resume, 
                skills=resume_service.get_all_resume_skills_by_id(resume.id)) for resume in resumes]
            return resumes_full

        if user.role == Role.COMPANY:
            resumes = resume_service.get_all_active_resumes_by_professional_id(id)
            resumes_full = [ResumeWithSkillsResponseModel(full_name=user_service.get_professional_fullname_by_id(resume.professional_id), 
                resume=resume, 
                skills=resume_service.get_all_resume_skills_by_id(resume.id)) for resume in resumes]
            return resumes_full
        
        if user.role == Role.PROFESSIONAL:
            resumes = resume_service.all_active_resumes_without_job_salary_and_description_by_professional_id(id)
            resumes_full = [ResumeWithoutDescriptionAndSalaryResponse(full_name=user_service.get_professional_fullname_by_id(resume.professional_id), 
                resume=resume) for resume in resumes]
            return resumes_full
            
    else:
        return Unauthorized('Please log in!')


@professionals_router.get('/{id}/match_requests')
def get_match_requests(id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot view the Match Requests of others.')

    match_requests = match_request_service.get_match_requests_by_professional_id(user.id)

    if not match_requests:
        return NotFound('There are currently no match requests waiting for you.')

    return (ProfessionalMatchRequestResponse.from_query_result(match_request.id, 
                                            user_service.get_company_name_by_id(match_request.requestor_id),
                                            job_ad_service.get_job_ad_by_id(match_request.job_ad_id),
                                            resume_service.get_resume_by_id(match_request.resume_id)) for match_request in match_requests)


@professionals_router.put('/{id}/match_requests/{match_request_id}')
def accept_match_request(id: int, match_request_id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot match this job ad.')

    match_request = match_request_service.get_match_request_by_id(match_request_id)

    if not match_request:
        return NotFound('Match request not found.')

    company = company_service.get_company_by_id(match_request.requestor_id)

    match_request_service.its_a_match(match_request_id)
    
    professional_service.make_professional_busy(id)

    company_service.update_successful_matches(company.id)

    resume_service.make_resume_matched(match_request.resume_id)

    job_ad_service.make_job_ad_archived(match_request.job_ad_id)

    #send email to company - its a match!
    return Success(f"You successfully matched {company.company_name}'s Job Ad!")


@professionals_router.delete('/{id}/match_requests/{match_request_id}')
def reject_match_request(id: int, match_request_id: int, x_token: str = Header(None)):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.id != id:
        return Forbidden('You cannot view the Match Requests of others.')

    if not match_request_service.professional_owns_match_request(user.id, match_request_id):
        return Forbidden('You cannot reject this match request!')

    match_request = match_request_service.get_match_request_by_id(match_request_id)

    if match_request_service.delete_match_request(match_request_id):
        #send email to Company that they got rejected
        return Success(f'Match request from {user_service.get_company_name_by_id(match_request.requestor_id)} rejected!')

    