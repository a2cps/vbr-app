"""Auth routes"""
from datetime import datetime
from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException
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
    class Config:
        schema_extra = {
            "example": {
                "access_token": "iOiJKV1QiLCJeyJ0eXAhbGciOiJSUzI1NiJ9.eyJqdGkiOiIwNTdkYmYzMy0yYWZlLTQ1MGEtYTM3Mi01ODkxYjE1YjYxMGIiLCJpc3MiOiJodHRwczovL2EyY3BzZGV2LnRhcGlzLmlvVucyIsInN1YiI6InZhdWdobkBhMmNwc2RldiIsInRhcGlzL3RlbmFudF9pZCI6ImEyY3BzZGV2IiwidGFwaXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsInRhcGlzL2RlbGVnYXRpb24iOmZhbHNlLCJ0YXBpcy9kZWxlZ2F0aW9uX3N1YiI6bnVsbCwidGFwaXMvdXNlcm5hbWUiOiJ2YXVnaG4iLCJ0YXBpcy9hY2NvdW50X3R5cGUiOiJ1c2VyIiwiZXhwIjoxNjM5L3YzL3Rva2NjIxNTM4LCJ0YXBpcy9jbGllbnRfaWQiOiI0YzdkNzkxNGU5NTAiLCJ0YXBpcy9ncmFudF90eXBlIjoicmVmcmVzaF90b2tlbiIsInRhcGlzL3JlZnJlc2hfY291bnQiOjJ9.WCL4TXRL-HCWDY_OCI6jUrgtxzKST6FZgbmo_tB4zgKJ4apmJ5kob8WnKlWXFTH81x1BrTln6bAZlHafX9e45pvtSy9DZS5hW7F_fkgS17aVtvP5BuBZxaqcxYQOC0PeROZXGvPonr2X3Ez9BsVS03ZKGrNpVNaoh2VcZLced_uSPolNOuET26iYwjsquOYo80JtvMdMDBj2OKTSn19_-HPR285GJjZ3uPrk1kgA09pjTA8D23D6iNNhV8wyYmqtAQ-8I6H0QZJb5bTn5X47XVCRYVj8bQH1F-nnBrXHvm4ACI_b5YvOrMbto7Yz7MtXIQhoE4HEcyfZJl_iFRUYVw",
            }
        }


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=TapisToken)
def get_token(
    body: Authentication = Body(...),
) -> dict:
    """Retrieve a Tapis token.

    Note: This endpoint will be deprecated in favor of a more standards-compliant implementation."""
    try:
        client = Tapis(
            base_url=settings.tapis_base_url,
            username=body.username,
            password=body.password,
        )
        client.get_tokens()
        return {"access_token": client.access_token.access_token}
    except Exception as exc:
        raise HTTPException(
            status_code=401, detail="Authorization failed: {0}".format(exc)
        )
