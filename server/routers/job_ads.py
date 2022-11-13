from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, Success, BadRequest
from server.data.models import Company, JobAd, Role, JobAdResponseModel
from server.services import company_service, job_ad_service, professional_service, match_request_service, resume_service
from server.services.job_ad_service import (add_skills,
                                            return_skills_with_ids,
                                            add_skill_to_job_ad, 
                                            get_job_ad_by_id, 
                                            get_all_skills_for_job_ad_id, 
                                            all_active_job_ads, 
                                            update_job_ads_views,
                                            edit_job_ad_by_company_and_job_ad_ids)
from server.services.user_service import get_company_name_by_id
from server.services.resume_service import get_resume_by_id
from server.common.validations_and_methods import validate_stars, validate_salary, validate_work_place, validate_status


job_ads_router = APIRouter(prefix='/job_ads')

@job_ads_router.post('/')
def create_job_ad(create_job_ad: JobAd, x_token= Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Access denied, you do not have permission to access on this server!')

    if user.role != Role.COMPANY:
        return Forbidden('You do not have permission to create a job_ad!')
    
    if not validate_status(create_job_ad.status):
        return BadRequest('The given status is incorrect!')
    
    if not validate_work_place(create_job_ad.work_place):
        return BadRequest('Invalid work place!')

    if not validate_salary(create_job_ad.min_salary, create_job_ad.max_salary):
        return BadRequest('Incorrect salary range!')

    if not create_job_ad.skill_requirements:
        return BadRequest('You need to add at least one skill to your job ad.')

    if create_job_ad.skill_requirements:
        
        if not validate_stars(create_job_ad.skill_requirements):
            return BadRequest('Stars for skills need to be between 1 and 5!')
        
        add_skills(create_job_ad.skill_requirements)

    new_job_ad = job_ad_service.create_job_ad(user.id, create_job_ad)

    return Success(f'Job ad with title {new_job_ad.title} was created!')

@job_ads_router.get('/{id}')
def get_job_ad(id: int, x_token= Header()):
    user = get_user_or_raise_401(x_token)
    
    if user:
        job_ad = get_job_ad_by_id(id)
    
        if not job_ad:
            return NotFound(f'Job ad with given ID: {id} does not exist!')
    
        update_job_ads_views(id)
        
        return JobAdResponseModel(
                company_name=get_company_name_by_id(job_ad.company_id),
                job_ad=job_ad)
    
    return Unauthorized('Please log in!')


@job_ads_router.get('/')
def get_job_ads(search: str | None = None, search_by: str | None = None, threshold: int | None = None,combined: bool | None = None,x_token=Header()):
    user = get_user_or_raise_401(x_token)

    search_validation = ['salary_range', 'location', 'skills', 'resume']

    if search_by and search_by not in search_validation:
        return BadRequest(f'Cannot search by parameter {search_by}.')

    if search_by == 'resume':
        resume = get_resume_by_id(int(search))
        if not resume:
            return NotFound(f'Resume with ID {search} does not exist.')
        search = resume
    
    if user:
        job_ads = job_ad_service.all_active_job_ads(search, search_by, threshold, combined)
    else:
        return Forbidden('Please log in!')
    
    if not job_ads:
        return NotFound('No resumes match your search.')
    
    job_ads_response = [JobAdResponseModel(company_name=get_company_name_by_id(job_ad.company_id), 
               job_ad = job_ad) for job_ad in job_ads]
    
    return job_ads_response

@job_ads_router.put('/{id}')
def edit_job_ad_by_id(id: int, job_ad: JobAd, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    if not user:
        return Unauthorized('Please log in!')

    if user.id != job_ad.company_id:
        return Forbidden('You do not have permission to edit this job ad!')

    if not job_ad.skill_requirements:
        return BadRequest('You need to leave at least one skill to your job ad.')
    
    if not validate_status(create_job_ad.status):
        return BadRequest('The given status is incorrect!')
    
    if not validate_work_place(create_job_ad.work_place):
        return BadRequest('Invalid work place!')

    if not validate_salary(create_job_ad.min_salary, create_job_ad.max_salary):
        return BadRequest('Incorrect salary range!')

    if not job_ad.skill_requirements:
        return BadRequest('You need to add at least one skill to your job ad.')

    else:
        if not validate_stars(job_ad.skill_requirements):
            return BadRequest('Stars for skills need to be between 1 and 5')

        add_skills(job_ad.skill_requirements)


    edited_job_ad =edit_job_ad_by_company_and_job_ad_ids(user.id, id, job_ad)
    if edited_job_ad:
        return JobAdResponseModel(company_name=get_company_name_by_id(edited_job_ad.company_id), 
                job_ad=edited_job_ad)


@job_ads_router.post('/{id}')
def send_match_request(id: int, resume_id: int, x_token= Header()):

    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Please log in!')
    
    if user.role != Role.PROFESSIONAL:
        return Forbidden('Only professionals can initiate match requests to companies.')

    job_ad = job_ad_service.get_job_ad_by_id(id)

    if not job_ad:
        return NotFound(f'Job Ad with id {id} does not exist!')
    
    resume = get_resume_by_id(resume_id)   

    if not resume:
        return NotFound(f'Resume with id {resume_id} does not exist!')
    

    if resume.professional_id != user.id:
        return Forbidden('You do not own this Resume!')

    company = company_service.get_company_by_id(job_ad.company_id)

    professional = professional_service.get_professional_by_id(resume.professional_id)


    existing_match_request = match_request_service.match_request_by_combined_key(resume_id, id)

    if existing_match_request:
        if existing_match_request.requestor_id == user.id:
            return BadRequest(f'You already sent a match request with Resume with ID {resume_id} to Job Ad with ID {id}!')
    
        elif existing_match_request.requestor_id == job_ad.company_id:
            #update match request with match = 1 ???
            match_request_service.its_a_match(existing_match_request.id)
            
            #update professional to busy
            professional_service.make_professional_busy(professional.id)

            #update company's successful matches +1
            company_service.update_successful_matches(company.id)

            #Resume status -> Matched
            resume_service.make_resume_matched(resume.id)

            #JobAd status -> Archived
            job_ad_service.make_job_ad_archived(job_ad.id)

            #send email to Company and to Professional
            return Success(f'Instant Match!')
    else:
        match_request_service.initiate_match_request(user.id, resume.id, job_ad.id)
        #send email to Company
        return Success(f'Your Match Request was successfully sent to {company.company_name}!')