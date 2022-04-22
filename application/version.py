import os

__all__ = ["get_version"]

API_VERSION = "0.3.0"


def get_version():
    # This is optionally provided by the hosting container
    BUILD_VERSION = os.environ.get("BUILD_VERSION", None)
    if BUILD_VERSION is not None and BUILD_VERSION != "":
        return "{0}-{1}".format(API_VERSION, BUILD_VERSION)
    else:
        return API_VERSION
