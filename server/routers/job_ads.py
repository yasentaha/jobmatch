from fastapi import APIRouter, Header
from pydantic import BaseModel

from server.common.auth import get_user_or_raise_401
from server.common.responses import NotFound, Forbidden, Unauthorized
from server.data.models import Company, JobAd
from server.services import company_service, job_ad_service

job_ads_router = APIRouter(prefix='/job_ads')