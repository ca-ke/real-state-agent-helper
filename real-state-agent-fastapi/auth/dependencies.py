from fastapi import Depends

from auth.repositories import AuthRepository
from auth.usecases import RegisterUserUseCase, LoginUserUseCase
from core.dependencies import get_supabase_client

def get_auth_repo(
    supabase = Depends(get_supabase_client)
) -> AuthRepository:
    return AuthRepository(supabase)

def get_login_usecase(
    repo: AuthRepository = Depends(get_auth_repo)
) -> LoginUserUseCase:
    return LoginUserUseCase(repo)

def get_register_usecase(
    repo: AuthRepository = Depends(get_auth_repo)
) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo)
