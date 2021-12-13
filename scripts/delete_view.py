import argparse
import os
import re
import sys

# import sqlfluff
from tapipy.tapis import Tapis
from vbr.client.connection import TapisDirectClient

VIEWS_PATH = "./views"


def delete_view(view_name: str, client: Tapis):
    views = client.pgrest.list_views()
    for view in views:
        if view.view_name == view_name or view.root_url == view_name:
            client.pgrest.delete_view(view_name=str(view.manage_view_id))


def main(arg_vals):
    t = Tapis(
        base_url=arg_vals["base_url"],
        username=arg_vals["username"],
        password=arg_vals["password"],
    )
    t.get_tokens()
    tenant_id = t.tenant_id
    for view_name in arg_vals["view_names"]:
        try:
            delete_view(view_name, t)
        except Exception as exc:
            print(exc)
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        type=str,
        default=os.environ.get("TAPIS_BASE_URL"),
        dest="base_url",
        help="Tapis API Base URL",
    )
    parser.add_argument(
        "-U",
        type=str,
        dest="username",
        default=os.environ.get("TAPIS_USERNAME"),
        help="Tapis Username",
    )
    parser.add_argument(
        "-P",
        type=str,
        dest="password",
        default=os.environ.get("TAPIS_PASSWORD"),
        help="Tapis Password",
    )
    parser.add_argument("view_names", nargs="+", help="View name(s)")
    args = parser.parse_args()
    main(vars(args))
