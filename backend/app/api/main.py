from fastapi import APIRouter
from app.api.login.routes import router as login_router
from app.api.users.routes import (
    router as users_router,
    signUpLoginRouter as signup_login_router,
)
from app.api.notes.routes import router as notes_router

api_router = APIRouter()
api_router.include_router(login_router)
api_router.include_router(users_router)
api_router.include_router(signup_login_router)
api_router.include_router(notes_router)
