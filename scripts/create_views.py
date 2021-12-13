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
            client.pgrest.delete_view(view_name=view.manage_view_id)


def load_sql(filename: str, tenant_id: str, replace: bool = False) -> str:
    with open(filename) as f:
        sql = f.read()
        sql = sql.strip()
        sql = re.sub(r"\s+", " ", sql)
        return sql


def construct_view(filename: str, raw_sql: str, comments: str = None) -> dict:
    view_name = os.path.basename(filename)
    view_name = re.sub(r".sql$", "", view_name)
    # TODO - extract first line comment -- formatted as /* comment goes here */
    # Transform SQL into
    if not raw_sql.endswith(";"):
        raw_sql = raw_sql + ";"
    if not raw_sql.startswith("AS "):
        raw_sql = "AS " + raw_sql
    return {"view_name": view_name, "raw_sql": raw_sql, "comments": comments}


def main(arg_vals):
    t = Tapis(
        base_url=arg_vals["base_url"],
        username=arg_vals["username"],
        password=arg_vals["password"],
    )
    t.get_tokens()
    tenant_id = t.tenant_id
    client = TapisDirectClient(t)
    client.setup("pgrest", api_path="manage/views")
    view_sql_files = [f for f in os.listdir(VIEWS_PATH) if not f.startswith(".")]
    base_views = []
    child_views = []
    for view_file in view_sql_files:
        if arg_vals["view_names"] != []:
            if view_file not in arg_vals["view_names"]:
                continue
        raw_sql = load_sql(os.path.join(VIEWS_PATH, view_file), tenant_id, False)
        data = construct_view(view_file, raw_sql)
        if "base" in data["view_name"]:
            base_views.append(data)
        else:
            child_views.append(data)
    print(len(base_views), "base views found")
    print(len(child_views), "child views found")

    # Create views
    # TODO - Check for existence and delete
    for view in base_views:
        try:
            # try:
            #     client.setup("pgrest", api_path="manage/views/" + view["view_name"])
            #     resp = client.delete()
            #     print("Deleted {0}".format(view["view_name"]))
            #     client.setup("pgrest", api_path="manage/views")
            # except Exception as exc:
            #     # TODO - better error checking and reporting
            #     print(exc)
            resp = client.post(data=view)
            print("Created " + view["view_name"])
        except Exception as exc:
            print(exc)

    for view in child_views:
        try:
            resp = client.post(data=view)
            print("Created " + view["view_name"])
        except Exception as exc:
            print(exc)


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
    parser.add_argument("view_names", nargs="*", help="Optional view name(s)")
    args = parser.parse_args()
    main(vars(args))
