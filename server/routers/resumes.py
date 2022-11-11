from fastapi import APIRouter, Header
from pydantic import BaseModel
from server.common.auth import get_user_or_raise_401
from server.common.responses import Forbidden, Unauthorized, Success, BadRequest, NotFound
from server.data.models import Resume, Skill, CreateResume, Role, ResumeResponseModel, ResumeWithSkillsResponseModel
from server.services import resume_service, user_service, job_ad_service, match_request_service, professional_service, company_service
from server.services.resume_service import create_resume_and_add_skill, get_resume_by_id, get_all_resume_skills_by_id, \
    edit_resume_by_professional_id_and_resume_id, add_skills, return_skills_with_ids, add_skill_to_resume, \
        main_resume_for_professional_exists, change_resume_main, validate_stars
from server.services.user_service import get_professional_fullname_by_id


resumes_router = APIRouter(prefix='/resumes')


@resumes_router.post('/')
def create_resume(resume: Resume, x_token= Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')

    if user.role != Role.PROFESSIONAL:
        return Forbidden('You do not have permission to create a resume!')


    if not resume.skills:
        return BadRequest('You need to add at least one skill to your resume.')

    else:
        if not validate_stars(resume.skills):
            return BadRequest('Stars for skills need to be between 1 and 5')

        add_skills(resume.skills)

    if resume.main and main_resume_for_professional_exists(user.id):
        change_resume_main(user.id)

    new_resume = resume_service.create_resume(user.id, resume)


    return Success(f'Resume with title {new_resume.title} was created!')


@resumes_router.put('/{resume_id}')
def edit_resume(resume_id: int, resume: Resume, x_token= Header()):
    user = get_user_or_raise_401(x_token)
    
    if not user:
        return Unauthorized('Please log in!')

    if user.id != resume.professional_id:
        return Forbidden('You do not have permission to edit this resume!')

    if not resume.skills:
        return BadRequest('You need to leave at least one skill to your resume.')

    else:
        if not validate_stars(resume.skills):
            return BadRequest('Stars for skills need to be between 1 and 5')

        add_skills(resume.skills)


    edited_resume = edit_resume_by_professional_id_and_resume_id(user.id, resume_id, resume)
    if edited_resume:
        return ResumeResponseModel(full_name=get_professional_fullname_by_id(edit_resume.professional_id), 
                resume=edit_resume)


@resumes_router.get('/{id}')
def view_resume(id: int, x_token= Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        resume=get_resume_by_id(id)
        if not resume:
            return NotFound(f'Resume with ID {id} does not exist or is hidden.')

        return ResumeResponseModel(full_name=get_professional_fullname_by_id(resume.professional_id), 
                resume=resume)

    return Unauthorized('Please log in!')

@resumes_router.get('/')
def get_resumes(search: str | None = None, search_by: str | None = None, threshold: int | None = None,combined: bool | None = None,x_token=Header()):
    user = get_user_or_raise_401(x_token)

    search_validation = ['salary_range', 'location', 'skills', 'job_ad']

    if search_by and search_by not in search_validation:
        return BadRequest(f'Cannot search by parameter {search_by}.')

    if user:
        resumes = resume_service.all_active(search, search_by, threshold, combined)
    else:
        return Forbidden('Please log in!')

    if not resumes:
        return NotFound('No resumes match your search.')

    resumes_response = [ResumeResponseModel(full_name=get_professional_fullname_by_id(resume.professional_id), 
                resume=resume) for resume in resumes]
    
    return resumes_response


@resumes_router.get('/{id}/resumes/hidden')
def get_resumes(professional_id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user.id == id or user.is_admin():
        resumes = resume_service.all_hidden_resumes_by_id(professional_id)
    else:
        return Unauthorized('Access denied, you do not have permission to access on this server!')

    return resumes


@resumes_router.post('/{id}')
def send_match_request(id: int, job_ad_id:int, x_token= Header()):

    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')
    
    if user.role != Role.COMPANY:
        return Forbidden('Only companies can initiate match requests to professionals.')

    resume = get_resume_by_id(id)   

    if not resume:
        return NotFound(f'Resume with id {id} does not exist!')
    
    job_ad = job_ad_service.get_job_ad_by_id(job_ad_id)

    if not job_ad:
        return NotFound(f'Job Ad with id {job_ad_id} does not exist!')

    if job_ad.company_id != user.id:
        return Forbidden('You do not own this Job Ad!')

    professional = professional_service.get_professional_by_id(resume.professional_id)

    company = company_service.get_company_by_id(user.id)

    existing_match_request = match_request_service.match_request_by_combined_key(id, job_ad_id)

    if existing_match_request:
        if existing_match_request.requestor_id == user.id:
            return BadRequest(f'You already sent a match request with Job Ad with ID {job_ad_id} to Resume with ID {id}!')
        elif existing_match_request.requestor_id == resume.professional_id:
            #delete match request / update match request with match = 1 ???s
            #update professional to busy
            #Resume status -> Matched
            #JobAd status -> Archived
            #send email to Company and to Professional
            return Success(f'Instant Match!')
    else:
        match_request_service.initiate_match_request(user.id, id, job_ad_id)
        #send email to Professional
        return Success(f'Your Match Request was successfully sent to {professional.first_name} {professional.last_name}!')

    