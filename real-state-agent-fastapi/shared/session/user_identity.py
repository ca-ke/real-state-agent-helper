from fastapi import Request, Depends, HTTPException
from core.dependencies import get_supabase_client

async def get_user_from_token(
    request: Request,
    supabase = Depends(get_supabase_client)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = auth_header.removeprefix("Bearer ").strip()
    result = supabase.auth.get_user(token)

    if not result or not result.user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return {
        "user_id": result.user.id,  
        "email": result.user.email
    }