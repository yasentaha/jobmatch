from fastapi import APIRouter, Header
from pydantic import BaseModel
from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized, Success, BadRequest
from server.data.models import Professional, Resume, ProfessionalInfo
from server.services import professional_service, resume_service
from server.services.professional_service import edit_professional_info, get_professional_info_by_id, edit_professional
from server.services.user_service import edit_user_info, get_town_id_by_name


class ProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: int


class PersonalProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: int
    list_of_matches: list[int]


professionals_router = APIRouter(prefix='/professionals')


@professionals_router.get('/')
def get_professionals(search: str | None = None, search_by: str | None = None, sort: str | None = None, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        professionals = professional_service.all(search, search_by)
    else:
        return Forbidden('Please log in!')

    if sort and (sort == 'asc' or sort == 'desc'):
        return professional_service.sort(professionals, reverse=sort == 'desc')
    else:
        return professionals


@professionals_router.get('/{id}')
def get_professional_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    professional = professional_service.get_professional_by_id(id)

    if professional is None:
        return NotFound('Professional not found!')

    if user.id == id or user.is_admin():
        return PersonalProfessionalResponseModel(
            professional=professional,
            active_resumes=resume_service.get_number_of_all_active_resumes(id),
            list_of_matches=resume_service.get_list_of_matches(id)
        )

    else:
        return ProfessionalResponseModel(
            professional=professional,
            active_resumes=resume_service.get_number_of_all_active_resumes(id)
        )


@professionals_router.put('/{id}/info')
def edit_professional_info_by_id(id: int, professional_info: ProfessionalInfo, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.id == id or not user.is_admin():
        return Unauthorized('You do not have permission to change Professional info!')

    edited_professional_info = edit_professional_info(id, professional_info)

    return edited_professional_info


@professionals_router.put('/{id}')
def edit_professional_by_id(id: int, professional: Professional, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.id == id:
        return Unauthorized('You do not have permission to change Professional info!')

    town_id = get_town_id_by_name(professional.town_name)
    if not town_id:
        return NotFound(f'Town {professional.town_name} is not a valid Bulgarian District Town name')
    
    error_msg = 'Your query is incorrect, please review your new info.'

    edited_user_info = edit_user_info(id, professional.email, professional.phone, professional.address, town_id)
    if edited_user_info:
        edited_professional = edit_professional(id, professional)
    else:
        return BadRequest(error_msg)
    
    if edited_professional:
        return Success(f'Successfully updated info for professional with name {professional.first_name} {professional.last_name}!')
    else:
        return BadRequest(error_msg)