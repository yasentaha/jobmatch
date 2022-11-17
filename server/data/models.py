from pydantic import BaseModel


class LoginData(BaseModel):
    user_name: str
    password: str


class User(BaseModel):
    id: int | None
    user_name: str
    password: str
    role: str

    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, user_name, password, role):
        return cls(
            id=id,
            user_name=user_name,
            password=password,
            role=role)


class Role:
    ADMIN = 'admin'
    PROFESSIONAL = 'professional'
    COMPANY = 'company'


class WorkPlace:
    REMOTE = 'Remote'
    ONSITE = 'Onsite'
    HYBRID = 'Hybrid'


class Status:
    ACTIVE = 'Active'
    HIDDEN = 'Hidden'
    PRIVATE = 'Private'
    MATCHED = 'Matched'
    ARCHIVED = 'Archived'


class Skill(BaseModel):
    id: int | None
    name: str
    stars: int 
    
    @classmethod
    def from_query_result(cls, id, name, stars):
        return cls(
            id=id,
            name=name,
            stars=stars)

class Professional(BaseModel):
    id: int | None
    user_name: str
    email: str
    phone: str | None
    address: str | None
    town_name: str
    first_name: str
    last_name: str
    summary: str | None
    busy: bool

    @classmethod
    def from_query_result(cls, id, user_name, email, phone, address, town_name, first_name, last_name, summary, busy):
        return cls(
            id=id,
            user_name=user_name,
            email=email,
            phone=phone,
            address=address,
            town_name=town_name,
            first_name=first_name,
            last_name=last_name,
            summary=summary,
            busy=busy)


class ProfessionalRegisterData(BaseModel):
    user_name: str | None
    password: str | None
    confirm_password: str | None
    first_name: str | None
    last_name: str | None
    summary: str | None
    email: str | None
    phone: str | None
    address: str | None
    town_name: str | None


class Resume(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    main: bool
    status: str
    town_name: str  # if town_name not in towns, catch error
    professional_id: int | None
    skills: list[Skill] | None
    @classmethod
    def from_query_result(cls, id, title, description, min_salary, max_salary, work_place, main, status, town_name, professional_id, skills=None):
        return cls(
            id=id,
            title=title,
            description=description,
            min_salary=min_salary,
            max_salary=max_salary,
            work_place=work_place,
            main=main,
            status=status,
            town_name=town_name,
            professional_id = professional_id, skills=skills)


class CreateResume(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    main: int
    status: str
    town_name: str
    skills: list[Skill]


class Company(BaseModel):
    id: int | None
    user_name: str
    company_name: str
    description: str
    email: str
    phone: str | None
    address: str
    town_name: str
    successful_matches: int

    @classmethod
    def from_query_result(cls, id, user_name, company_name, description, email, phone, address,
                          town_name, successful_matches):
        return cls(
            id=id,
            user_name=user_name,
            company_name=company_name,
            description=description,
            email=email,
            phone=phone,
            address=address,
            town_name=town_name,
            successful_matches=successful_matches)


class CompanyRegisterData(BaseModel):
    user_name: str | None
    password: str | None
    confirm_password: str | None
    company_name: str | None
    description: str | None
    email: str | None
    phone: str | None
    address: str | None
    town_name: str | None


class JobAd(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    status: str
    town_name: str
    views: int | None
    company_id: int | None
    skill_requirements: list[Skill] | None


    @classmethod
    def from_query_result(cls, id, title, description, min_salary, max_salary, work_place, status, town_name, company_id, views, skill_requirements=None):
        return cls(
            id=id,
            title=title,
            description=description,
            min_salary=min_salary,
            max_salary=max_salary,
            work_place=work_place,
            status=status,
            town_name=town_name,
            company_id=company_id,
            views=views,
            skill_requirements=skill_requirements)


class MatchRequest(BaseModel):
    id: int
    resume_id: int
    job_ad_id: int
    requestor_id: int
    
    @classmethod
    def from_query_result(cls, id, resume_id, job_ad_id, requestor_id):
        return cls(
            id=id,
            resume_id=resume_id,
            job_ad_id=job_ad_id,
            requestor_id=requestor_id)


#RESPONSE MODELS
class ProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: int

class CompanyResponseModel(BaseModel):
    company: Company
    active_job_ads: int


class PersonalProfessionalResponseModel(BaseModel):
    professional: Professional
    active_resumes: int
    list_of_matches: list[int]

class PersonalCompanyResponseModel(BaseModel):
    company: Company
    active_job_ads: int
    job_ads: list[JobAd]


class ResumeWithoutDescriptionAndSalary(BaseModel):
    id: int | None
    title: str
    work_place: str
    status: str
    town_name: str
    professional_id: int
    @classmethod
    def from_query_result(cls, id, title, work_place, status, town_name, professional_id):
        return cls(
            id=id,
            title=title,
            work_place=work_place,
            status=status,
            town_name=town_name,
            professional_id = professional_id)

class ResumeWithSkillsResponseModel(BaseModel):
    full_name: str 
    resume: Resume
    skills: list[Skill]

class ResumeWithoutDescriptionAndSalaryResponse(BaseModel):
    full_name: str 
    resume: ResumeWithoutDescriptionAndSalary

class ResumeResponseModel(BaseModel):
    full_name: str 
    resume: Resume

class JobAdResponseModel(BaseModel):
    company_name: str 
    job_ad: JobAd

class ProfessionalMatchRequestResponse(BaseModel):
    id: int
    company_name: str
    job_ad: JobAd
    resume: Resume

    @classmethod
    def from_query_result(cls, id, company_name, job_ad, resume):
        return cls(
            id=id,
            company_name=company_name,
            job_ad=job_ad,
            resume=resume)

class CompanyMatchRequestResponse(BaseModel):
    id: int
    professional_name: str
    resume: Resume
    job_ad: JobAd
    
