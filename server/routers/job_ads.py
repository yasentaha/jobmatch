from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, Success
from server.data.models import Company, JobAd, CreateJobAd, Role
from server.services import company_service, job_ad_service
from server.services.job_ad_service import add_skills, return_skills_with_ids, add_skill_to_job_ad

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