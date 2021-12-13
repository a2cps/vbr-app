"""Provides common dependencies for FastAPI routes"""
import os
from functools import lru_cache
from typing import List, Optional

import jwt
import vbr
from fastapi import Depends, Header, HTTPException
from tapipy.errors import BaseTapyException
from tapipy.tapis import Tapis
from vbr.hashable import picklecache

from .config import get_settings

settings = get_settings()


async def limit_offset(offset: int = 0, limit: int = settings.app_default_page_size):
    """Provides limit and offset query parameters."""
    return {"offset": offset, "limit": limit}


@picklecache.mcache(lru_cache(maxsize=32))
def _client(token: str) -> Tapis:
    """Private: Returns a Tapis client given an Oauth token.

    This is wrapped in an LRU cache to avoid having to load Tapis
    library multiple times when the same token is provided as input.
    """
    return Tapis(base_url=settings.tapis_base_url, access_token=token)


# @picklecache.mcache(lru_cache(maxsize=32))
def tapis_admin_client() -> Tapis:
    """Returns the configured service account Tapis client

    This account must have the PGREST_ADMIN role."""
    client = Tapis(
        base_url=settings.tapis_base_url,
        username=settings.tapis_service_uname,
        password=settings.tapis_service_pass,
    )
    client.get_tokens()
    return client


def vbr_admin_client(client: Tapis = Depends(tapis_admin_client)):
    """Returns a VBR client that uses the configured Tapis service account"""
    vbr_client = vbr.api.get_vbr_api_client(client)
    return vbr_client


async def tapis_token(x_tapis_token: Optional[str] = Header(None)):
    """Returns current Tapis access token."""
    # Read from ENV to support local testing
    if os.environ.get("X_TAPIS_TOKEN", None) is not None:
        x_tapis_token = os.environ.get("X_TAPIS_TOKEN")
    if x_tapis_token is None:
        raise HTTPException(status_code=401, detail="X-Tapis-Token header required")
    else:
        try:
            # Tapis can validates JWT on its own but it's cheaper to do it early
            jwt.decode(x_tapis_token, options={"verify_signature": False})
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="X-Tapis-Token was not valid")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="X-Tapis-Token has expired")
    return x_tapis_token


def tapis_client(x_tapis_token: str = Depends(tapis_token)) -> Tapis:
    """Returns a user Tapis client for the provided token"""
    try:
        client = _client(x_tapis_token)
    except BaseTapyException as exc:
        raise HTTPException(
            status_code=401, detail="X-Tapis-Token was not valid: {0}".format(exc)
        )
    return client


def tapis_user(token: str = Depends(tapis_token)):
    """Get Tapis user profile for the provided token."""
    try:
        t = _client(token)
    except BaseTapyException as exc:
        raise HTTPException(
            status_code=401, detail="X-Tapis-Token was not valid: {0}".format(exc)
        )
    return t.authenticator.get_userinfo().username


def tapis_roles(user: str = Depends(tapis_user), token: str = Depends(tapis_token)):
    """Get Tapis SK roles for the provided user."""
    try:
        t = _client(token)
    except BaseTapyException as exc:
        raise HTTPException(
            status_code=401, detail="X-Tapis-Token was not valid: {0}".format(exc)
        )
    return t.sk.getUserRoles(user=user, tenant=settings.tapis_tenant_id).names


def role_pgrest_admin(roles: List[str] = Depends(tapis_roles)):
    if not "PGREST_ADMIN" in roles:
        raise HTTPException(status_code=401)


# Tapis SK Roles
#
# See ../scripts/create_roles.py for details


def vbr_user(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_USER" in roles:
        raise HTTPException(status_code=401)


def vbr_admin(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_ADMIN" in roles:
        raise HTTPException(status_code=401)


def vbr_read_public(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_PUBLIC" in roles:
        raise HTTPException(status_code=401)


def vbr_read_limited_phi(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_LIMITED_PHI" in roles:
        raise HTTPException(status_code=401)


def vbr_read_any_phi(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_ANY_PHI" in roles:
        raise HTTPException(status_code=401)


def vbr_write_public(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_WRITE_PUBLIC" in roles:
        raise HTTPException(status_code=401)


def vbr_write_any(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_WRITE_ANY" in roles:
        raise HTTPException(status_code=401)
