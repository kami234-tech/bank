from fastapi import Header, HTTPException
from firebase_admin import auth as firebase_auth

async def authenticate_user(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

    id_token = authorization.split("Bearer ")[-1]

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
