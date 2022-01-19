"""Administrative routes"""
from datetime import datetime
from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from tapipy.tapis import Tapis

from ..config import get_settings
from ..dependencies import *

settings = get_settings()

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


class GrantableRole(Enum):
    VBR_ADMIN = "VBR_ADMIN"
    VBR_READ_ANY_PHI = "VBR_READ_ANY_PHI"
    VBR_READ_LIMITED_PHI = "VBR_READ_LIMITED_PHI"
    VBR_READ_PUBLIC = "VBR_READ_PUBLIC"
    VBR_WRITE_ANY = "VBR_WRITE_ANY"
    VBR_WRITE_PUBLIC = "VBR_WRITE_PUBLIC"


class Role(Enum):
    VBR_USER = "VBR_USER"
    VBR_ADMIN = "VBR_ADMIN"
    VBR_READ_ANY_PHI = "VBR_READ_ANY_PHI"
    VBR_READ_LIMITED_PHI = "VBR_READ_LIMITED_PHI"
    VBR_READ_PUBLIC = "VBR_READ_PUBLIC"
    VBR_WRITE_ANY = "VBR_WRITE_ANY"
    VBR_WRITE_PUBLIC = "VBR_WRITE_PUBLIC"


"VBR_READ_ANY", "VBR_READ_ANY_PHI", "VBR_READ_LIMITED_PHI", "VBR_READ_PUBLIC", "VBR_USER", "VBR_WRITE_PUBLIC"


class TapisRole(BaseModel):
    name: str
    description: str
    owner: str
    # updated: datetime
    # updatedby: str
    class Config:
        schema_extra = {
            "example": {
                "name": "TACO_USER",
                "description": "Default user role",
                "owner": "tacobot",
            }
        }


class User(BaseModel):
    username: str
    name: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "username": "tacobot",
                "name": "Chuy Tacbobot",
                "email": "elpresidente@tacobot.com",
            }
        }


class AddUser(BaseModel):
    username: str
    role: Optional[Role] = "VBR_READ_PUBLIC"

    class Config:
        schema_extra = {"example": {"username": "tacobot", "role": "VBR_READ_PUBLIC"}}


def build_user(username: str, client: Tapis) -> User:
    profile = client.authenticator.get_profile(username=username)
    user = {
        "username": profile.username,
        "name": "{0} {1}".format(profile.given_name, profile.last_name),
        "email": profile.email,
    }
    return user


@router.get(
    "/roles",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=List[TapisRole],
)
def list_roles(client: Tapis = Depends(tapis_client)):
    """List VBR roles."""
    role_names = client.sk.getRoleNames(tenant=settings.tapis_tenant_id).names
    roles = []
    for rn in role_names:
        if rn in [e.value for e in Role]:
            role = client.sk.getRoleByName(tenant=settings.tapis_tenant_id, roleName=rn)
            roles.append(
                {
                    "name": role.name,
                    "description": role.description,
                    "owner": role.owner,
                }
            )
    return roles


@router.get(
    "/users",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=List[User],
)
def list_users(client: Tapis = Depends(tapis_client)):
    """List authorized users."""
    usernames = client.sk.getUsersWithRole(
        tenant=settings.tapis_tenant_id, roleName="VBR_USER"
    ).names
    users = [build_user(u, client) for u in usernames]
    return users


@router.post(
    "/users",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=User,
)
def add_user(body: AddUser = Body(...), client: Tapis = Depends(tapis_client)):
    """Add an authorized user."""
    try:
        client.sk.grantRole(
            tenant=settings.tapis_tenant_id,
            user=body.username,
            roleName=body.role.value,
        )
        return build_user(username=body.username, client=client)
    except Exception:
        raise


@router.get(
    "/user/{username}",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=User,
)
def get_user(username: str, client: Tapis = Depends(tapis_client)):
    """Get profile of an authorized user."""
    if (
        "VBR_USER"
        in client.sk.getUserRoles(user=username, tenant=settings.tapis_tenant_id).names
    ):
        user_profile = build_user(username, client)
        return User(**user_profile)
    else:
        raise HTTPException(status_code=404, detail="Not an authorized VBR user")


@router.get(
    "/user/{username}/roles",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=List[Role],
)
def list_user_roles(username: str, client: Tapis = Depends(tapis_client)):
    """List roles for an authorized user."""
    roles = [
        r
        for r in client.sk.getUserRoles(
            tenant=settings.tapis_tenant_id, user=username
        ).names
        if r in [e.value for e in Role]
    ]
    roles = sorted(roles)
    return roles


@router.put(
    "/user/{username}/roles",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=List[Role],
)
def grant_user_role(
    username: str,
    role: GrantableRole = "VBR_READ_PUBLIC",
    client: Tapis = Depends(tapis_client),
):
    """Grant a role to a user."""
    client.sk.grantRole(
        tenant=settings.tapis_tenant_id, user=username, roleName=role.value
    )
    # Return list of roles for user
    roles = [
        r
        for r in client.sk.getUserRoles(
            tenant=settings.tapis_tenant_id, user=username
        ).names
        if r in [e.value for e in Role]
    ]
    roles = sorted(roles)
    return roles


@router.delete(
    "/user/{username}/roles/{role}",
    dependencies=[Depends(tapis_client), Depends(vbr_admin)],
    response_model=List[Role],
)
def revoke_user_role(username: str, role: Role, client: Tapis = Depends(tapis_client)):
    """Revoke a role from a user.

    Note: Inherited roles (such as VBR_USER) cannot be revoked using this method.
    """
    client.sk.revokeUserRole(
        tenant=settings.tapis_tenant_id, user=username, roleName=role.value
    )
    roles = [
        r
        for r in client.sk.getUserRoles(
            tenant=settings.tapis_tenant_id, user=username
        ).names
        if r in [e.value for e in Role]
    ]
    roles = sorted(roles)
    return roles
