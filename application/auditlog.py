import logging
import os
from .config import get_settings

LOG_PATH = "."

__all__ = ["logger"]

settings = get_settings()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "%(asctime)-6s: %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "null": {"class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "basic",
        },
        "audit_file": {
            "level": "INFO",
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "basic",
            "filename": os.path.join(settings.app_log_path, "audit.log"),
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "basic",
            "filename": os.path.join(settings.app_log_path, "error.log"),
        },
    },
    "loggers": {
        "audit": {
            "handlers": ["null", "audit_file", "error_file"],
            "level": "DEBUG",
            "propogate": False,
        }
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("audit")
