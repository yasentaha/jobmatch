from fastapi import APIRouter
from pydantic import BaseModel
from server.data.models import Resume, Skill


class ResumeResponseModel(BaseModel):
    resume: Resume
    skills: list[Skill]
    match_request_ids: list[int]


resumes_router = APIRouter(prefix='/resumes')