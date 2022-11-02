from fastapi import APIRouter, Header
from pydantic import BaseModel
from server.common.auth import get_user_or_raise_401
from server.common.responses import Forbidden, Unauthorized, Success
from server.data.models import Resume, Skill, CreateResume
from server.routers import professionals
from server.services import resume_service
from server.services.resume_service import create_resume_and_add_skill, get_resume_by_id, get_all_resume_skills_by_id, \
    edit_resume_by_professional_id_and_resume_id


class ResumeResponseModel(BaseModel):
    resume: Resume
    skills: list[Skill]
    match_request_ids: list[int]


class ResumeWithSkillsResponseModel(BaseModel):
    resume: Resume
    skills: list[Skill]


resumes_router = APIRouter(prefix='/professionals')


@resumes_router.post('/{id}/resumes')
def create_resume(professional_id: int, create_resume: CreateResume, x_token: Header()):
    user = get_user_or_raise_401(x_token)

    if user.id != professional_id:
        return Unauthorized('Access denied, you do not have permission to access on this server!')

    new_resume: CreateResume

    new_resume = create_resume_and_add_skill(professional_id, create_resume)

    return Success(f'Resume with title {new_resume.title} was created!')


@resumes_router.get('/{id}/resumes/{resume_id}')
def edit_resume(professional_id: int, resume_id: int, resume: Resume, x_token: Header()):
    user = get_user_or_raise_401(x_token)

    if user.id == professional_id:
        edited_resume = edit_resume_by_professional_id_and_resume_id(professional_id, resume_id, resume)
        return edited_resume

    return Unauthorized('Access denied, you do not have permission to edit this resume!')

@resumes_router.get('/{id}/resumes/{resume_id}')
def view_resume(professional_id: int, resume_id: int, x_token: Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        return ResumeWithSkillsResponseModel(
            resune=get_resume_by_id(professional_id, resume_id),
            skills=get_all_resume_skills_by_id(resume_id)
        )

    return Unauthorized('Please log in!')


@resumes_router.get('/')
def get_resumes(professional_id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        resumes = resume_service.all_active_resumes_without_job_salary_and_description_by_id(professional_id)
    else:
        return Forbidden('Please log in!')

    return resumes


@resumes_router.get('/{id}/resumes/hidden')
def get_resumes(professional_id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user.id == id or user.is_admin():
        resumes = resume_service.all_hidden_resumes_by_id(professional_id)
    else:
        return Unauthorized('Access denied, you do not have permission to access on this server!')

    return resumes
