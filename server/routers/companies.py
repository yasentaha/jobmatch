from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized
from server.data.models import Company, JobAd, CompanyInfo
from server.services.company_service import get_company_info_by_id, get_company_by_id, get_all_companies, get_number_of_all_active_job_ads_by_company_id
from server.services import company_service, job_ad_service


companies_router = APIRouter(prefix='/companies')

@companies_router.get('/')
def get_companies(sort: str | None = None, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user:
        companies = company_service.get_all_companies()
    else:
        return Forbidden('Please Login!')

    if sort and (sort == 'asc' or sort == 'desc'):
        return company_service.sort(companies, reverse=sort == 'desc')
    else:
        return companies