from fastapi import APIRouter
from app.schemas.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest):
    return await register_user(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    return await login_user(data)
