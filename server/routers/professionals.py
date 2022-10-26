from fastapi import APIRouter
from pydantic import BaseModel
from server.data.models import Professional


class ProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: list[int]
    hidden_resumes: list[int]


professionals_router = APIRouter(prefix='/professionals')
