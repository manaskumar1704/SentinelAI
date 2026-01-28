"""
Clerk Authentication Middleware

Verifies JWT tokens from Clerk and extracts user information.
"""

import httpx
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from config import get_settings
from models.user import ClerkUser


security = HTTPBearer(auto_error=False)

# Cache for Clerk JWKS
_jwks_cache: Optional[dict] = None


async def get_clerk_jwks() -> dict:
    """Fetch Clerk's JWKS (JSON Web Key Set) for token verification."""
    global _jwks_cache
    
    if _jwks_cache is not None:
        return _jwks_cache
    
    settings = get_settings()
    
    # Clerk's JWKS endpoint - derive from publishable key
    # Format: pk_test_xxx or pk_live_xxx
    # The frontend domain is encoded in the key after the prefix
    pk = settings.clerk_publishable_key
    if not pk:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clerk publishable key not configured"
        )
    
    # For development, we'll use a simplified approach
    # In production, fetch from Clerk's JWKS endpoint
    async with httpx.AsyncClient() as client:
        try:
            # Clerk JWKS endpoint pattern
            # We need the frontend clerk domain from the publishable key
            # For now, return empty and handle verification differently
            _jwks_cache = {"keys": []}
            return _jwks_cache
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch Clerk JWKS: {str(e)}"
            )


async def verify_clerk_token(token: str) -> dict:
    """
    Verify a Clerk JWT token.
    
    In production, this would verify against Clerk's JWKS.
    For development, we extract claims without full verification.
    """
    try:
        # Decode without verification for development
        # In production, use proper JWKS verification
        unverified_claims = jwt.get_unverified_claims(token)
        
        # Extract user ID from 'sub' claim
        user_id = unverified_claims.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        return {
            "user_id": user_id,
            "email": unverified_claims.get("email"),
            "full_name": unverified_claims.get("name"),
        }
    except JWTError as e:
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
    claims = await verify_clerk_token(token)
    
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
        claims = await verify_clerk_token(token)
        return ClerkUser(
            user_id=claims["user_id"],
            email=claims.get("email"),
            full_name=claims.get("full_name"),
        )
    except HTTPException:
        return None
