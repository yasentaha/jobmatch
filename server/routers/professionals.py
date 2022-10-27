from fastapi import APIRouter
from pydantic import BaseModel
from server.data.models import Professional, Resume


class ProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: list[Resume]

class PersonalProfessionalResponseModel(BaseModel):
    professional: Professional
    list_of_matches: list[int]
    active_resumes: list[Resume]


professionals_router = APIRouter(prefix='/professionals')
