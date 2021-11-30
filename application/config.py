import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CORS_ENABLED = True
    PUBLIC_CNAME = os.environ.get("APP_PUBLIC_CNAME", "vbr.a2cps.tacc.cloud")
    LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("APP_LOG_FILE", "/var/log/service.log")
    OTP_KEY = os.environ.get("APP_OTP_KEY")
    TAPIS_BASE_URL = "https://a2cps-dev.tapis.io"
    TAPIS_TENANT_ID = os.environ.get("TAPIS3_TENANT_ID", "a2cps-dev")
    TAPIS_CLIENT_KEY = os.environ.get("TAPIS3_CLIENT_KEY")
    TAPIS_CLIENT_SECRET = os.environ.get("TAPIS3_CLIENT_SECRET")
    TAPIS_CLIENT_SCOPE = os.environ.get("TAPIS3_CLIENT_SCOPE", "PRODUCTION")
    TAPIS_SERVICE_UNAME = os.environ.get("TAPIS3_SERVICE_UNAME")
    TAPIS_SERVICE_PASS = os.environ.get("TAPIS3_SERVICE_PASS")
    SECRET_KEY = os.environ.get("APP_SECRET_KEY")
    URL_SCHEME = "https"


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "INFO"


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    URL_SCHEME = "http"
    PUBLIC_CNAME = "127.0.0.1"
