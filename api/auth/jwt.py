from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os


secret_key = os.getenv('SUPABASE_SECRET_KEY')
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print("Received token:", token)
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"], audience="authenticated")
        print("Token payload:", payload)
        return payload
    except JWTError as e:
        print("JWT Error:", e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
