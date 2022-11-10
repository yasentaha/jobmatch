from fastapi import APIRouter, Header
from pydantic import BaseModel
from server.common.auth import get_user_or_raise_401
from server.common.responses import Forbidden, Unauthorized, Success, BadRequest, NotFound
from server.data.models import Resume, Skill, CreateResume, Role, ResumeResponseModel, ResumeWithSkillsResponseModel
from server.routers import professionals
from server.services import resume_service, user_service
from server.services.resume_service import create_resume_and_add_skill, get_resume_by_id, get_all_resume_skills_by_id, \
    edit_resume_by_professional_id_and_resume_id, add_skills, return_skills_with_ids, add_skill_to_resume, \
        main_resume_for_professional_exists, change_resume_main, validate_stars
from server.services.user_service import get_professional_fullname_by_id


resumes_router = APIRouter(prefix='/resumes')


@resumes_router.post('/')
def create_resume(create_resume: CreateResume, x_token= Header()):
    user = get_user_or_raise_401(x_token)
    #VALIDATION FOR STARS FROM 1 to 5
    if not user:
        return Unauthorized('Access denied, you do not have permission to access on this server!')

    if user.role != Role.PROFESSIONAL:
        return Forbidden('You do not have permission to create a resume!')

    if create_resume.main and main_resume_for_professional_exists(user.id):
        change_resume_main(user.id)

    if create_resume.skills:
        if not validate_stars(create_resume.skills):
            return BadRequest('Stars for skills need to be between 1 and 5')

        add_skills(create_resume.skills)

    skills_with_ids = return_skills_with_ids(create_resume.skills)

    new_resume = resume_service.create_resume(user.id, create_resume)
    if new_resume:
        [add_skill_to_resume(new_resume.id, skill) for skill in skills_with_ids]

    return Success(f'Resume with title {new_resume.title} was created!')


@resumes_router.put('/{id}')
def edit_resume(resume_id: int, resume: Resume, x_token= Header()):
    user = get_user_or_raise_401(x_token)
    #VALIDATION FOR STARS FROM 1 to 5
    if user:
        edited_resume = edit_resume_by_professional_id_and_resume_id(user.id, resume_id, resume)
        return edited_resume

    return Unauthorized('Access denied, you do not have permission to edit this resume!')

@resumes_router.get('/{id}')
def view_resume(id: int, x_token= Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        resume=get_resume_by_id(id)
        if not resume:
            return NotFound(f'Resume with ID {id} does not exist or is hidden.')

        return ResumeWithSkillsResponseModel(full_name=get_professional_fullname_by_id(resume.professional_id), 
                resume=resume, 
                skills=get_all_resume_skills_by_id(resume.id))

    return Unauthorized('Please log in!')

@resumes_router.get('/')
def get_resumes(search: str | None = None, search_by: str | None = None, threshold: int | None = None,combined: bool | None = None,x_token=Header()):
    user = get_user_or_raise_401(x_token)

    search_validation = ['salary_range', 'location', 'skills']

    if search_by and search_by not in search_validation:
        return BadRequest(f'Cannot search by parameter {search_by}.')

    if user:
        resumes = resume_service.all_active(search, search_by, threshold, combined)
    else:
        return Forbidden('Please log in!')

    resumes_full = [ResumeWithSkillsResponseModel(full_name=get_professional_fullname_by_id(resume.professional_id), 
                resume=resume, 
                skills=get_all_resume_skills_by_id(resume.id)) for resume in resumes]
    return resumes_full

@resumes_router.get('/{id}')
def get_resumes(professional_id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        resumes = resume_service.all_active_resumes_without_job_salary_and_description_by_professional_id(professional_id)
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


'''
- resumes/id da mu dadesh match request
- companies/id --//--
- 


professionals/id/match_requests
MNOOGO PO TOVA:
ProfessionalMatchRequestResponse
Company Name / Id
Job Ad - full
Resume - Title / Id / Full

REJECT???????????????? AUTOMATIC FOR PROFESSIONAL WHEN MATCH WITH OTHERS
MANUAL FOR BOTH PROFESSIONAL COMPANY WHEN YOU WANT TO REJECT

companies/id/match_requests
CompanyMatchRequestResponse
Professional Name / Id
Resume - full
Job Ad - Title / Id / Full


'''