from fastapi import FastAPI
from server.routers.users import users_router
from server.routers.professionals import professionals_router
from server.routers.companies import companies_router
from server.routers.resumes import resumes_router
from server.routers.job_ads import job_ads_router

app = FastAPI()
app.include_router(users_router)
app.include_router(professionals_router)
app.include_router(companies_router)
app.include_router(resumes_router)
app.include_router(job_ads_router)