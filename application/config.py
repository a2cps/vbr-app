"""Implements configuration via environment variables"""
from functools import lru_cache

from pydantic_settings import BaseSettings

__all__ = ["Settings", "get_settings"]


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    tapis_base_url: str = "https://tacc.tapis.io"
    tapis_tenant_id: str = "tacc"
    tapis_client_scope: str = "PRODUCTION"
    tapis_service_uname: str = "username"
    tapis_service_pass: str = "p@assw0rd!"
    tapis_client_id: str = "client_id"
    tapis_client_key: str = "client_key"
    tapis_client_secret: str = "client_secret"
    app_secret_key: str = "A>=MW;ZDF;/;Nf5>fNWnBPv@"
    app_otp_key: str = "Wx9H2K9fJzmnMKKquGca76ALdY8MaaMp"
    app_public_cname: str = "localhost"
    app_log_level: str = "DEBUG"
    app_debug: bool = False
    app_default_page_size: int = 50
    app_log_path: str = "."
    app_build_version: str = ""

    class Config:
        env_file = "env.rc"
