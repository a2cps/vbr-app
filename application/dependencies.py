"""Provides common dependencies for FastAPI routes"""
import json
import jwt
from functools import lru_cache
from typing import List, Optional

import vbr
from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tapipy.errors import BaseTapyException
from tapipy.tapis import Tapis
from vbr.hashable import picklecache

from .auditlog import logger
from .config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


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


@picklecache.mcache(lru_cache(maxsize=4))
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


async def tapis_token(x_tapis_token: str = Depends(oauth2_scheme)):
    """Returns current Tapis token using OAuth2 scheme dependency."""
    return x_tapis_token


def tapis_client(x_tapis_token: str = Depends(tapis_token)) -> Tapis:
    """Returns a user Tapis client for the provided token"""
    try:
        client = _client(x_tapis_token)
    except BaseTapyException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was not valid: {0}".format(exc),
        )
    return client


def tapis_user(token: str = Depends(tapis_token)):
    """Get Tapis user profile for the provided token."""
    try:
        t = _client(token)
    except BaseTapyException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was not valid: {0}".format(exc),
        )
    return t.authenticator.get_userinfo().username


def tapis_roles(user: str = Depends(tapis_user), token: str = Depends(tapis_token)):
    """Get Tapis SK roles for the provided user."""
    try:
        t = _client(token)
    except BaseTapyException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was not valid: {0}".format(exc),
        )
    return t.sk.getUserRoles(user=user, tenant=settings.tapis_tenant_id).names


def role_pgrest_admin(roles: List[str] = Depends(tapis_roles)):
    if not "PGREST_ADMIN" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# Tapis SK Roles
#
# See ../scripts/create_roles.py for details


def vbr_user(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_USER" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def vbr_admin(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_ADMIN" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def vbr_read_public(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_PUBLIC" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def vbr_read_limited_phi(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_LIMITED_PHI" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def vbr_read_any_phi(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_READ_ANY_PHI" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def vbr_write_public(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_WRITE_PUBLIC" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def vbr_write_any(roles: List[str] = Depends(tapis_roles)):
    if not "VBR_WRITE_ANY" in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def log_request(request: Request):
    """Log requests using the audit logger"""
    request_body = await request.body()
    try:
        request_body = json.loads(request_body)
    except Exception:
        pass
    headers = dict(request.headers)
    auth_header = headers.pop("authorization", "")
    auth_header = auth_header.replace("Bearer ", "")
    try:
        jwt_claimset = jwt.decode(auth_header, options={"verify_signature": False})
        tapis_username = jwt_claimset.get("tapis/username", None)
        if tapis_username is not None:
            admin_client = tapis_admin_client()
            tapis_roles = admin_client.sk.getUserRoles(
                user=tapis_username, tenant=settings.tapis_tenant_id
            ).names
    except jwt.exceptions.DecodeError:
        jwt_claimset = {}
        tapis_roles = []

    log = {
        "id": request.state.uuid,
        "request": {
            "url": request.url,
            "method": request.method,
            "headers": headers,
            "query_params": dict(request.query_params),
            "path_params": dict(request.path_params),
            "body": request_body,
            "jwt_claimset": dict(jwt_claimset),
            "user_roles": tapis_roles,
        },
    }
    logger.info(log)
