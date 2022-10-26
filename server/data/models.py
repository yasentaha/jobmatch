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
    summary: str
    busy: bool
    image_url: str


class Professional(BaseModel):
    id: int | None
    user_name: str
    password: str
    first_name: str
    last_name: str
    summary: str
    busy: bool
    image_url: str
    email: str
    phone: str
    address: str
    town_id: int

    # active_resumes: list[int] #ids of active resumes
    # hidden_resumes: list[int]

    @classmethod
    def from_query_result(cls, id, user_name, password, role, first_name, last_name, summary, busy, image_url, email,
                          phone, address, town_id):
        return cls(
            id=id,
            user_name=user_name,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
            summary=summary,
            busy=busy,
            image_url=image_url,
            email=email,
            phone=phone,
            address=address,
            town_id=town_id)


class Role:
    REGULAR = 'regular'
    ADMIN = 'admin'


class Skill(BaseModel):
    id: int | None
    name: str
    stars: int  # not more than 5, not less than 1


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
    town_name: str


class Resume(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    status: str
    town_id: int  # if town_name not in towns, catch error
    main: int
    # skills: list[Skill] # go to response model
    # match_request_ids: list[int]

class CompanyInfo(BaseModel):
    id: int | None
    company_name: str
    description: str
    logo_url: str

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

    active_job_ads: list[int]  # ids of active job_ads
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
    town_name: str


class JobAd(BaseModel):
    id: int | None
    title: str
    description: str
    min_salary: int
    max_salary: int
    work_place: str
    status: str
    town_name: str  # if town_name not in towns, catch error
    requirements: list[Skill]
    match_request_ids: list[int]


class MatchRequestResponse(BaseModel):
    id: int
    job_ad: JobAd
    resume: Resume  # MOJEM LI DA GO NAPRAVIM EDNO DO DRUGO


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
    VELIK0TARNOVO = 'Veliko Tarnovo'
    GABROVO = 'Gabrovo'
    STARAZAGORA = 'Stara Zagora'
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