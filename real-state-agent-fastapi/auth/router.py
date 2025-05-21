from fastapi import APIRouter, Depends

from auth.models import AuthRequest
from auth.usecases import RegisterUserUseCase, LoginUserUseCase
from auth.dependencies import get_login_usecase, get_register_usecase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(
    data: AuthRequest,
    usecase: RegisterUserUseCase = Depends(get_register_usecase)
):
    email = usecase.execute(data)
    return {"message": "Check your email", "email": email}

@router.post("/login")
def login(
    data: AuthRequest,
    usecase: LoginUserUseCase = Depends(get_login_usecase)
):
    return usecase.execute(data)
