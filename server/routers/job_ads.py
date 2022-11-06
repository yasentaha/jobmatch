from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, Success
from server.data.models import Company, JobAd, CreateJobAd, Role, JobAdResponseModel
from server.services import company_service, job_ad_service
from server.services.job_ad_service import add_skills, return_skills_with_ids, add_skill_to_job_ad, get_job_ad_by_id, get_all_skills_for_job_ad_id

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

    return Success(f'Resume with title {new_job_ad.title} was created!')

@job_ads_router.get('/{id}')
def get_job_ad(id: int, x_token= Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        return JobAdResponseModel(
            resume=get_job_ad_by_id(id),
            skills=get_all_skills_for_job_ad_id(id)
        )

    return Unauthorized('Please log in!')