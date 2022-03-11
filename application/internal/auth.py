"""Auth routes"""
from datetime import datetime
from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2PasswordRequestFormStrict,
)
from pydantic import BaseModel, EmailStr
from tapipy.tapis import Tapis

from ..config import get_settings
from ..dependencies import *

settings = get_settings()


class Authentication(BaseModel):
    username: str
    password: str
    # scope: str = "PRODUCTION"
    class Config:
        schema_extra = {
            "example": {
                "username": "tacobot",
                "password": "w}3s>R*TwwKh)36G",
            }
        }


class TapisToken(BaseModel):
    access_token: str
    # refresh_token: str
    expires_at: datetime
    token_type: str = "bearer"
    # refresh_token: str
    class Config:
        schema_extra = {
            "example": {
                "access_token": "iOiJKV1QiLCJeyJ0eXAhbGciOiJSUzI1NiJ9.eyJqdGkiOiIwNTdkYmYzMy0yYWZlLTQ1MGEtYTM3Mi01ODkxYjE1YjYxMGIiLCJpc3MiOiJodHRwczovL2EyY3BzZGV2LnRhcGlzLmlvVucyIsInN1YiI6InZhdWdobkBhMmNwc2RldiIsInRhcGlzL3RlbmFudF9pZCI6ImEyY3BzZGV2IiwidGFwaXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsInRhcGlzL2RlbGVnYXRpb24iOmZhbHNlLCJ0YXBpcy9kZWxlZ2F0aW9uX3N1YiI6bnVsbCwidGFwaXMvdXNlcm5hbWUiOiJ2YXVnaG4iLCJ0YXBpcy9hY2NvdW50X3R5cGUiOiJ1c2VyIiwiZXhwIjoxNjM5L3YzL3Rva2NjIxNTM4LCJ0YXBpcy9jbGllbnRfaWQiOiI0YzdkNzkxNGU5NTAiLCJ0YXBpcy9ncmFudF90eXBlIjoicmVmcmVzaF90b2tlbiIsInRhcGlzL3JlZnJlc2hfY291bnQiOjJ9.WCL4TXRL-HCWDY_OCI6jUrgtxzKST6FZgbmo_tB4zgKJ4apmJ5kob8WnKlWXFTH81x1BrTln6bAZlHafX9e45pvtSy9DZS5hW7F_fkgS17aVtvP5BuBZxaqcxYQOC0PeROZXGvPonr2X3Ez9BsVS03ZKGrNpVNaoh2VcZLced_uSPolNOuET26iYwjsquOYo80JtvMdMDBj2OKTSn19_-HPR285GJjZ3uPrk1kgA09pjTA8D23D6iNNhV8wyYmqtAQ-8I6H0QZJb5bTn5X47XVCRYVj8bQH1F-nnBrXHvm4ACI_b5YvOrMbto7Yz7MtXIQhoE4HEcyfZJl_iFRUYVw",
                # "refresh_token": "OiJKV1QiLCeyJ0eXAiJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIyNDkyNzJiNS02NzFhLTQ5OWQtYWMzMS0xNTVmYmY4NTQ3MjMiLCJpc3MiOiJodHRwczovL2EyY3BzZGV2LnRhcGlzLmlvL3YzL3Rva2VucyIsInN1YiI6InZhdWdobkBhMmNwc2RldiIsInRhcGlzL2luaXRpYWxfdHRsIjozMTUzNjAwMCwidGFwaXMvdGVuYW50X2lkIjoiYTJjcHNkZXYiLCJ0YXBpcy90b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjQwNjgzOSwidGFwaXMvYWNjZXNzX3Rva2VuIjp7Imp0aSI6ImM4NWJjYjA5LTU2YTQtNDhmYi1iOTQyLTIyMDA3NzFmZDgxZSIsImlzcyI6Imh0dHBudGFwaXMuaW8vdjMvdG9rZW5zIiwic3ViIjoidmF1Z2huQGEyY3BzZGV2IiwidGFwaXMvdGVuYW50X2lkIjoiYTJjcHNkZXYiLCJ0YXBpcy90b2zOi8vYTJjcHNkZXYtlbl90eXBlIjoiYWNjZXNzIiwidGFwaXMvZGVsZWdhdGlvbiI6ZmFsc2UsInRhcGlzL2RlbGVnYXRpb25fc3ViIjpudWxsLCJ0YXBpcy91c2VybmFtZSI6InZhdWdobiIsInRhcGlzL2FjY291bnRfdHlwZSI6InVzZXIiLCJ0YXBpcy9jbGllbnRfaWQiOiI0YzdkNzkxNGU5NTAiLCJ0YXBpcy9ncmFudF90eXBlIjoicGFzc3dvcmQiLCJ0YXBpcy9yZWZyZXNoX2NvdW50IjowLCJ0dGwiOjE0NDAwfX0.gJHcZlo5kYFxCELIskc80_B-mM339YRzqRPrmz8-NuI4DzFTTSekFwH69308FN3_J5GTJ6Vy1_ICPLFlsjRxw-Wc2JdesUAr3YRUojtoASChXfykALAmk368ddn5ETJJ6zO9e0VWDygXu8HaR7CDDUwRALw473v2nZqwesWkUs8AQT9JOeeAa4aX7M5PCpAb9NmBNpifaSFzKQd05TZ-981VYPExtY6Y5Wrm-xxxS6XzPId7HgST6C55VxMfjJaINkvN6QQ-OJZX8eX2-T_CHbrc7FByp94p-JuX71l6_WV9Ecob6ontX4hOmQ72XmMGt6dC8NeSBI9LioMWRhtGOw",
                "expires_at": "2023-02-14 20:33:59+00:00",
                "token_type": "bearer",
            }
        }


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=TapisToken)
def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """Retrieve a Tapis token."""

    try:

        # Allow override client ID and Key
        if form_data.client_id:
            client_id = form_data.client_id
        else:
            client_id = settings.tapis_client_id
        if form_data.client_secret:
            client_key = form_data.client_secret
        else:
            client_key = settings.tapis_client_key

        client = Tapis(
            base_url=settings.tapis_base_url,
            username=form_data.username,
            password=form_data.password
            # client_id=client_id,
            # client_key=client_key,
        )
        client.get_tokens()
        return {
            "access_token": client.access_token.access_token,
            # "refresh_token": client.refresh_token.refresh_token,
            "expires_at": client.access_token.expires_at,
            "token_type": "bearer",
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed: {0}".format(exc),
        )
