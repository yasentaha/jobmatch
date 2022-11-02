from fastapi import APIRouter, Header
from pydantic import BaseModel
from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized
from server.data.models import Professional, Resume, ProfessionalInfo
from server.services import professional_service, resume_service
from server.services.professional_service import edit_professional_info, get_professional_info_by_id


class ProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: int


class PersonalProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: int
    list_of_matches: list[int]


professionals_router = APIRouter(prefix='/professionals')


@professionals_router.get('/')
def get_professionals(sort: str | None = None, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        professionals = professional_service.all()
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


@professionals_router.put('/{id}')
def edit_professional_info_by_id(id: int, professional_info: ProfessionalInfo, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.id == id or not user.is_admin():
        return Unauthorized('You do not have permission to change Professional info!')

    edited_professional_info = edit_professional_info(id, professional_info)

    return edited_professional_info
