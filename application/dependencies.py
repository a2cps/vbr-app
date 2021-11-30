import os
from typing import List, Optional

import jwt
import vbr
from fastapi import Depends, Header, HTTPException
from tapipy.tapis import Tapis

from .config import DevelopmentConfig as Config


async def limit_offset(offset: int = 0, limit: int = 20):
    """Provides limit and offset query parameters."""
    return {"offset": offset, "limit": limit}


def tapis_admin_client() -> Tapis:
    """Returns a service account Tapis client"""
    client = Tapis(
        base_url=Config.TAPIS_BASE_URL,
        username=Config.TAPIS_SERVICE_UNAME,
        password=Config.TAPIS_SERVICE_PASS,
    )
    client.get_tokens()
    return client


def vbr_admin_client(client: Tapis = Depends(tapis_admin_client)):
    """Returns an administrator VBR client"""
    vbr_client = vbr.api.get_vbr_api_client(client)
    return vbr_client


async def tapis_token(x_tapis_token: Optional[str] = Header(None)):
    """Returns current Tapis access token."""
    if os.environ.get("X_TAPIS_TOKEN", None) is not None:
        x_tapis_token = os.environ.get("X_TAPIS_TOKEN")
    if x_tapis_token is None:
        raise HTTPException(status_code=401, detail="X-Tapis-Token header required")
    else:
        try:
            # Tapis can validates JWT on its own but it's cheaper to do it early
            jwt.decode(x_tapis_token, options={"verify_signature": False})
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Token was not valid")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
    return x_tapis_token


def tapis_client(x_tapis_token: str = Depends(tapis_token)) -> Tapis:
    """Returns a user Tapis client for the provided token"""
    client = Tapis(base_url=Config.TAPIS_BASE_URL, access_token=x_tapis_token)
    return client


def tapis_user(token: str = Depends(tapis_token)):
    """Get Tapis user profile for the provided token."""
    t = Tapis(base_url=Config.TAPIS_BASE_URL, access_token=token)
    return t.authenticator.get_userinfo().username


def tapis_roles(user: str = Depends(tapis_user), token: str = Depends(tapis_token)):
    """Get Tapis SK roles for the provided user."""
    t = Tapis(base_url=Config.TAPIS_BASE_URL, access_token=token)
    return t.sk.getUserRoles(user=user, tenant=Config.TAPIS_TENANT_ID).names


def role_pgrest_admin(roles: List[str] = Depends(tapis_roles)):
    if not "PGREST_ADMIN" in roles:
        raise HTTPException(status_code=401)


# Tapis SK Roles
#
# VBR_ADMIN
#   L_VBR_READ_ANY
#     L_VBR_READ_PUBLIC
#   L_VBR_WRITE_ANY
#     L_VBR_WRITE_PUBLIC
#
# VBR_WRITE_ANY
#   L_ VBR_READ_ANY
# VBR_WRITE_PUBLIC
#   L_ VBR_READ_PUBLIC


def role_vbr_admin(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_ADMIN" in roles:
        raise HTTPException(status_code=401)


def role_vbr_read(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_PUBLIC" in roles:
        raise HTTPException(status_code=401)


def role_vbr_read_any(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_ANY" in roles:
        raise HTTPException(status_code=401)


def role_vbr_write(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_WRITE_PUBLIC" in roles:
        raise HTTPException(status_code=401)


def role_vbr_write_any(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_WRITE_ANY" in roles:
        raise HTTPException(status_code=401)
