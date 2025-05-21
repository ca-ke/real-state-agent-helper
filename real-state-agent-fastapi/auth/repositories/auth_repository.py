from supabase import Client
from auth.models.auth_request import AuthRequest
from fastapi import HTTPException

class AuthRepository:
    def __init__(self, client: Client):
        self.client = client

    def sign_up(self, data: AuthRequest):
        response = self.client.auth.sign_up(data.model_dump())
        if not response.user:
            raise HTTPException(status_code=400, detail="Signup failed")
        return response.user

    def sign_in(self, data: AuthRequest):
        response = self.client.auth.sign_in_with_password(data.model_dump())
        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return response
