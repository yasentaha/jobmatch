from fastapi import FastAPI
from server.routers.users import users_router
from server.routers.professionals import professionals_router
from server.routers.companies import companies_router

app = FastAPI()
app.include_router(users_router)
app.include_router(professionals_router)
app.include_router(companies_router)