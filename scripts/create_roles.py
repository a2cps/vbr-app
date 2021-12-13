import os
import argparse
from tapipy.tapis import Tapis

DEFAULT_ROLE = ("VBR_USER", "Default user role")

# VBR_ADMIN
# - VBR_READ_ANY_PHI
#   - VBR_READ_LIMITED_PHI
#     - VBR_READ_PUBLIC
#
# VBR_ADMIN
# - VBR_WRITE_ANY
#   - VBR_WRITE_PUBLIC
#
# VBR_WRITE_ANY
# - VBR_READ_ANY_PHI

ROLES = [
    ("VBR_ADMIN", "VBR Administrator"),
    ("VBR_READ_ANY_PHI", "Can read any PHI data"),
    ("VBR_READ_LIMITED_PHI", "Can read limited PHI data"),
    ("VBR_READ_PUBLIC", "Can read only public data"),
    ("VBR_WRITE_ANY", "Can write admin privileged fields and endpoints"),
    ("VBR_WRITE_PUBLIC", "Can write only public fields and endpoints"),
    DEFAULT_ROLE,
]
# (Parent, Child)
RELATIONS = [
    ("VBR_ADMIN", "VBR_WRITE_ANY"),  # Admin can write anything,
    ("VBR_WRITE_ANY", "VBR_WRITE_PUBLIC"),
    ("VBR_ADMIN", "VBR_READ_ANY_PHI"),  # Admin can read all PHI
    ("VBR_READ_ANY_PHI", "VBR_READ_LIMITED_PHI"),  # Any PHI can read Limited PHI
    ("VBR_READ_ANY_PHI", "VBR_READ_PUBLIC"),  # Limited PHI can read public
    (
        "VBR_WRITE_ANY",
        "VBR_READ_ANY_PHI",
    ),  # Anyone who can write ANY can read ANY
    (
        "VBR_WRITE_PUBLIC",
        "VBR_READ_PUBLIC",
    ),  # Anyone who can write public can read public
]


def main(arg_vals):
    t = Tapis(
        base_url=arg_vals["base_url"],
        username=arg_vals["username"],
        password=arg_vals["password"],
    )
    t.get_tokens()
    tenant_id = t.tenant_id
    # Create roles (this is impdepotent on the server side)
    for roleName, description in ROLES:
        print("Creating {0} on {1}".format(roleName, tenant_id))
        resp = t.sk.createRole(
            roleName=roleName, description=description, roleTenant=tenant_id
        )
        print("Created {0}".format(resp.url))
    # Automatically add the DEFAULT_ROLE as a child of other roles
    defaultRoleName = DEFAULT_ROLE[0]
    for roleName, description in ROLES:
        if roleName != defaultRoleName:
            print("{0} :childOf: {1}".format(defaultRoleName, roleName))
            t.sk.addChildRole(
                roleTenant=tenant_id,
                parentRoleName=roleName,
                childRoleName=defaultRoleName,
            )
    # Create other relations as per RELATIONS
    for parentRoleName, childRoleName in RELATIONS:
        if parentRoleName != childRoleName:
            print("{0} :childOf: {1}".format(childRoleName, parentRoleName))
            t.sk.addChildRole(
                roleTenant=tenant_id,
                parentRoleName=parentRoleName,
                childRoleName=childRoleName,
            )


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
    args = parser.parse_args()
    main(vars(args))
