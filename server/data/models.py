from datetime import date, datetime
from pydantic import BaseModel, constr


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


class Contact(BaseModel):
    id: int | None
    email: str
    phone: str | None
    address: str
    town_id: int


class ProfessionalInfo(BaseModel):
    id: int | None
    first_name: str
    last_name: str
    summary: str | None
    busy: bool


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

    # active_resumes: int #number of active resumes
    # hidden_resumes: list[int]

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


class Role:
    ADMIN = 'admin'
    PROFESSIONAL = 'professional'
    COMPANY = 'company'


class Skill(BaseModel):
    id: int | None
    name: str
    stars: int  # not more than 5, not less than 1
    
    @classmethod
    def from_query_result(cls, id, name, stars):
        return cls(
            id=id,
            name=name,
            stars=stars)


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
    # skill_name: str
    # stars: int


class CompanyInfo(BaseModel):
    id: int | None
    company_name: str
    description: str
    successful_matches: int

    # town_name: str
    # email: str
    # phone: str | None
    # address: str | None
    # active_job_ads: int

    @classmethod
    def from_query_result(cls, id, company_name, description, successful_matches):
        return cls(
            id=id,
            company_name=company_name,
            description=description,
            successful_matches=successful_matches)


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

    # active_job_ads: int

    # archived_job_ads: list[int]

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
    town_name: str  # if town_name not in towns, catch error
    views: int
    company_id: int
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

class CreateJobAd(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    status: str
    town_name: str  # if town_name not in towns, catch error
    views:int | None
    skill_requirements: list[Skill]

class MatchRequestResponse(BaseModel):
    id: int
    request_from: str #Name
    resume_id: Resume
    job_ad_id: JobAd

class MatchRequest(BaseModel):
    id: int
    resume_id: Resume
    job_ad_id: JobAd
    requestor_id: int


class Town(BaseModel):
    SOFIA = 'Sofia'
    PLOVDIV = 'Plovdiv'
    RUSE = 'Ruse'
    VARNA = 'Varna'
    BURGAS = 'Burgas'
    VIDIN = 'Vidin'
    MONTANA = 'Montana'
    PERNIK = 'Pernik'
    KIUSTENDIL = 'Kiustendil'
    BLAGOEVGRAD = 'Blagoevgrad'
    VRATSA = 'Vratsa'
    PAZARDZHIK = 'Pazardzhik'
    SMOLIAN = 'Smolian'
    PLEVEN = 'Pleven'
    LOVECH = 'Lovech'
    VELIK0TARNOVO = 'Veliko tarnovo'
    GABROVO = 'Gabrovo'
    STARAZAGORA = 'Stara zagora'
    HASKOVO = 'Haskovo'
    KARDZHALI = 'Kardzhali'
    TARGOVISHTE = 'Targovishte'
    SLIVEN = 'Sliven'
    YAMBOL = 'Yambol'
    SILISTRA = 'Silistra'
    RAZGRAD = 'Razgrad'
    SHUMEN = 'Shumen'
    DOBRICH = 'Dobrich'

    all_towns = [SOFIA, PLOVDIV, RUSE, VARNA, BURGAS, VIDIN, MONTANA, PERNIK, KIUSTENDIL, BLAGOEVGRAD, VRATSA,
                 PAZARDZHIK, SMOLIAN, PLEVEN, LOVECH, VELIK0TARNOVO, GABROVO, STARAZAGORA, HASKOVO, KARDZHALI,
                 TARGOVISHTE, SLIVEN, YAMBOL, SILISTRA, RAZGRAD, SHUMEN, DOBRICH]


class ProfessionalResponse(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    summary: str | None
    email: str
    phone: str | None
    address: str
    town_name: str

    @classmethod
    def from_query_result(cls, id, user_name, first_name, last_name, summary, email,
                          phone, address, town_name):
        return cls(
            id=id,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            summary=summary,
            email=email,
            phone=phone,
            address=address,
            town_name=town_name)


class CompanyResponseModel(BaseModel):
    company: Company
    active_job_ads: int


class PersonalCompanyResponseModel(BaseModel):
    company: Company
    active_job_ads: int
    list_of_matches: list[int]

class JobAdResponseModel(BaseModel):
    company_name: str
    job_ad: JobAd
    skill_requirements: list[Skill]

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