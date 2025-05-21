from ..repositories.auth_repository import AuthRepository
from ..models import AuthRequest

class RegisterUserUseCase:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def execute(self, data: AuthRequest) -> str:
        user = self.repo.sign_up(data)
        return user.email
