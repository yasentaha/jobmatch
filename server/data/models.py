from datetime import date, datetime
from pydantic import BaseModel, constr

class LoginData(BaseModel):
    user_name: str
    password: str

class Professional(BaseModel):
    id: int | None
    user_name: str
    password: str
    role: str
    first_name: str
    last_name: str
    summary: str
    busy: bool
    image_url: str
    email: str
    phone: str
    address: str
    town_id: int

    active_resumes: list[int] #ids of active resumes
    hidden_resumes: list[int]

 
    def is_admin(self):
        return self.role == Role.ADMIN

    # @classmethod
    # def from_query_result(cls, id, user_name, password, role, first_name, last_name):
    #     return cls(
    #         id=id,
    #         user_name=user_name,
    #         password=password,
    #         role=role,
    #         registered_on=registered_on,
    #         email=email)

class Role:
    REGULAR = 'regular'
    ADMIN = 'admin'

class Skill(BaseModel):
    id: int | None
    name: str
    stars: int #not more than 5, not less than 1


class WorkPlace:
    REMOTE = 'remote'
    ONSITE = 'onsite'
    HYBRID = 'hybrid'

class Status:
    ACTIVE = 'active'
    HIDDEN = 'hidden'
    PRIVATE = 'private'
    MATCHED = 'matched'
    ARCHIVED = 'archived'
    

class ProfessionalRegisterData(BaseModel):
    user_name: str
    password: str
    first_name: str
    last_name: str
    summary: str | None
    image_url: str | None
    email: str
    phone: str | None
    address: str 
    town_id: int


class Resume(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    status: str
    town_name: str #if town_name not in towns, catch error
    skills: list[Skill]
    match_request_ids: list[int]

class Company(BaseModel):
    id: int | None
    user_name: str
    password: str
    company_name: str
    description: str
    logo_url: str
    email: str
    phone: str
    address: str
    town_id: int
    successful_matches: int

    active_job_ads: list[int] #ids of active job_ads
    archived_job_ads: list[int]

    # @classmethod
    # def from_query_result(cls, id, user_name, password, role, first_name, last_name):
    #     return cls(
    #         id=id,
    #         user_name=user_name,
    #         password=password,
    #         role=role,
    #         registered_on=registered_on,
    #         email=email)



class CompanyRegisterData(BaseModel):
    user_name: str
    password: str
    company_name: str
    description: str
    logo_url: str | None
    email: str
    phone: str | None
    address: str
    town_id: int

class JobAd(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    status: str
    town_name: str #if town_name not in towns, catch error
    requirements: list[Skill]
    match_request_ids: list[int]

class MatchRequestResponse(BaseModel):
    id: int
    job_ad: JobAd
    resume: Resume #MOJEM LI DA GO NAPRAVIM EDNO DO DRUGO