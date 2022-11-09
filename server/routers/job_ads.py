from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, Success
from server.data.models import Company, JobAd, CreateJobAd, Role, JobAdResponseModel
from server.services import company_service, job_ad_service
from server.services.job_ad_service import add_skills, return_skills_with_ids, add_skill_to_job_ad, get_job_ad_by_id, get_all_skills_for_job_ad_id, all_active_job_ads
from server.services.user_service import get_company_name_by_id


job_ads_router = APIRouter(prefix='/job_ads')

@job_ads_router.post('/')
def create_resume(create_job_ad: CreateJobAd, x_token= Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized('Access denied, you do not have permission to access on this server!')

    if user.role != Role.COMPANY:
        return Forbidden('You do not have permission to create a job_ad!')


    if create_job_ad.skill_requirements:
        add_skills(create_job_ad.skill_requirements)

    skills_with_ids = return_skills_with_ids(create_job_ad.skill_requirements)

    new_job_ad = job_ad_service.create_job_ad(user.id, create_job_ad)
    if new_job_ad:
        [add_skill_to_job_ad(new_job_ad.id, skill) for skill in skills_with_ids]

    return Success(f'Job ad with title {new_job_ad.title} was created!')

@job_ads_router.get('/{id}')
def get_job_ad(id: int, x_token= Header()):
    user = get_user_or_raise_401(x_token)
    job_ad = get_job_ad_by_id(id)
    
    if not user:
        return Unauthorized('Please log in!')
    
    if not job_ad:
        return NotFound(f'Job ad with given ID: {id} does not exist!')
        
    return JobAdResponseModel(
            company_name=get_company_name_by_id(job_ad.company_id),
            job_ad=job_ad,
            skill_requirements=get_all_skills_for_job_ad_id(id))


@job_ads_router.get('/')
def get_job_ads(search: str | None = None, search_by: str | None = None, threshold: int | None = None,x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        job_ads = job_ad_service.all_active_job_ads(search, search_by, threshold)
    else:
        return Forbidden('Please log in!')
    
    full_job_ads = [JobAdResponseModel(company_name=get_company_name_by_id(job_ad.company_id), 
                job_ad = job_ad, 
                skill_requirements=get_all_skills_for_job_ad_id(job_ad.id)) for job_ad in job_ads]
    
    return full_job_ads