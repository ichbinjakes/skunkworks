"""List of principal roles to bootstrap polaris and individual catalogs"""

from apache_polaris.sdk.management.models import PrincipalRole

GLOBAL_PRINICPAL_ROLES: dict[str, list[str]] = {
    "service_admin": ["catalog_admin"],
    "governance_officer": ["catalog_viewer"],
}


def get_catalog_roles(catalog_name):
    return [
        PrincipalRole(name=f"{catalog_name}_catalog_admin", federated=False, properties=None),
        PrincipalRole(
            name=f"{catalog_name}_catalog_query_service",
            federated=False,
            properties=None,
        ),
        PrincipalRole(
            name=f"{catalog_name}_catalog_ingest_service",
            federated=False,
            properties=None,
        ),
    ]


# def get_catalog_principal_roles(catalog_name: str) -> dict[str, list[str]]:
#     catalog_name = catalog_name.lower()
#     return {
#         f"{catalog_name}_catalog_admin": ["catalog_admin"],
#         f"{catalog_name}_query_service": ["catalog_reader"],
#         f"{catalog_name}_ingest_service": ["catalog_writer"],
#     }


def create_principal_roles(client):
    pass
