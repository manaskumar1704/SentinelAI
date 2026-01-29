"""
Supabase Authentication Middleware

Verifies JWT tokens from Supabase Auth and extracts user information.
"""

import jwt
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import get_settings
from models.user import ClerkUser  # Renamed internally but keeping class name for compatibility


security = HTTPBearer(auto_error=False)


def verify_supabase_token(token: str) -> dict:
    """
    Verify a Supabase JWT token.
    
    Validates the token signature using the JWT secret and extracts user claims.
    """
    settings = get_settings()
    
    if not settings.supabase_jwt_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase JWT secret not configured"
        )
    
    try:
        # Decode and verify the JWT with the Supabase JWT secret
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        
        # Extract user ID from 'sub' claim (standard JWT claim)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        # Extract user metadata
        user_metadata = payload.get("user_metadata", {})
        
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "full_name": user_metadata.get("full_name") or user_metadata.get("name"),
            "role": payload.get("role", "authenticated"),
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> ClerkUser:
    """
    FastAPI dependency to get the current authenticated user.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: ClerkUser = Depends(get_current_user)):
            return {"user_id": user.user_id}
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    claims = verify_supabase_token(token)
    
    return ClerkUser(
        user_id=claims["user_id"],
        email=claims.get("email"),
        full_name=claims.get("full_name"),
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[ClerkUser]:
    """
    FastAPI dependency that returns user if authenticated, None otherwise.
    
    Useful for endpoints that work differently for authenticated users.
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        claims = verify_supabase_token(token)
        return ClerkUser(
            user_id=claims["user_id"],
            email=claims.get("email"),
            full_name=claims.get("full_name"),
        )
    except HTTPException:
        return None
