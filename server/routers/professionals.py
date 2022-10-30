from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden
from server.data.models import Professional, Resume, ProfessionalInfo
from server.services import professional_service, resume_service
from server.services.professional_service import edit_professional_info, get_professional_info_by_id


class ProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: list[Resume]


class PersonalProfessionalResponseModel(BaseModel):
    professional: Professional
    list_of_matches: list[int]
    active_resumes: list[Resume]


professionals_router = APIRouter(prefix='/professionals')


@professionals_router.get('/{id}')
def get_professional_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    professional = professional_service.get_professional_by_id(id)

    if professional is None:
        return NotFound('Professional not found!')

    if user.role == 'professional':
        return PersonalProfessionalResponseModel(
            professional=professional,
            list_of_matches=resume_service.get_list_of_matches(id),
            active_resumes=resume_service.get_all_active_resumes_by_professional_id(id)
        )

    else:
        return ProfessionalResponseModel(
            professional=professional,
            list_of_matches=resume_service.get_list_of_matches()
        )


@professionals_router.put('/{id}')
def edit_professional_info_by_id(id: int, first_name: str, last_name: str,
                                summary: str | None, busy: int, x_token: str = Header()):

    user = get_user_or_raise_401(x_token)

    if not user.role=='professional':
        return Forbidden('You do not have permission to change Professional info!')

    professional_info=get_professional_info_by_id(id)

    if not professional_info:
        return Forbidden(f'Professional with {id} not exist!')

    edited_professional_info=edit_professional_info(professional_info,first_name,last_name,summary,busy)

    return edited_professional_info