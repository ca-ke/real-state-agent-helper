from ..repositories.auth_repository import AuthRepository
from ..models import AuthRequest, AuthResponse

class LoginUserUseCase:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def execute(self, data: AuthRequest) -> AuthResponse:
        result = self.repo.sign_in(data)
        return AuthResponse(
            access_token=result.session.access_token,
            user_id=result.user.id,
            email=result.user.email
        )
