from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import Forbidden
from server.data.models import Resume, Skill
from server.routers import professionals
from server.services import resume_service


class ResumeResponseModel(BaseModel):
    resume: Resume
    skills: list[Skill]
    match_request_ids: list[int]


resumes_router = APIRouter(prefix='/resumes')


@resumes_router.get('/{id}/resumes')
def get_resumes(id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        resumes = resume_service.all_active_resumes_without_job_salary_and_description(id)
    else:
        return Forbidden('Please log in!')

    return resumes

@resumes_router.get('/{id}/resumes/hidden')
def get_resumes(id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user.id == id or user.is_admin():
        resumes = resume_service.all_hidden_resumes(id)
    else:
        return Forbidden('You do not have permission to this page!')

    return resumes
