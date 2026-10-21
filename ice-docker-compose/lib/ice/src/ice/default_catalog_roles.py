"""List of catalog roles to bootstrap a catalog with."""

from apache_polaris.sdk.management.models import CatalogPrivilege
from apache_polaris.sdk.management.models import CatalogRole


def get_catalog_roles(catalog_name: str):
    return [
        CatalogRole(
            name=f"{catalog_name}_admin",
            properties={"description": "Role with admin catalog privileges."},
        ),
        CatalogRole(
            name=f"{catalog_name}_viewer",
            properties={"description": "Role with metadata view catalog privileges only."},
        ),
        CatalogRole(
            name=f"{catalog_name}_manager",
            properties={
                "description": "Role with namespace and table creation and management privileges."
            },
        ),
        CatalogRole(
            name=f"{catalog_name}_reader",
            properties={"description": "Role with data read privileges only."},
        ),
        CatalogRole(
            name=f"{catalog_name}_writer",
            properties={"description": "Role with data write privileges only."},
        ),
    ]


def get_catalog_role_grants(role_name: str):
    return []


CATALOG_PRIVILEGES: dict[str, list[CatalogPrivilege]] = {
    "catalog_admin": [
        # create/delete namespaces, manage permissions
        CatalogPrivilege.CATALOG_MANAGE_CONTENT,
        CatalogPrivilege.CATALOG_MANAGE_ACCESS,
        CatalogPrivilege.CATALOG_MANAGE_METADATA,
        CatalogPrivilege.CATALOG_READ_PROPERTIES,
        CatalogPrivilege.CATALOG_WRITE_PROPERTIES,
        CatalogPrivilege.NAMESPACE_FULL_METADATA,
        CatalogPrivilege.TABLE_FULL_METADATA,
        CatalogPrivilege.VIEW_FULL_METADATA,
    ],
    "catalog_viewer": [
        # view tables and metadata for governance purposes
        CatalogPrivilege.CATALOG_MANAGE_METADATA,
        CatalogPrivilege.CATALOG_READ_PROPERTIES,
        CatalogPrivilege.NAMESPACE_LIST,
        CatalogPrivilege.NAMESPACE_READ_PROPERTIES,
        CatalogPrivilege.NAMESPACE_FULL_METADATA,
        CatalogPrivilege.TABLE_LIST,
        CatalogPrivilege.TABLE_READ_PROPERTIES,
        CatalogPrivilege.TABLE_FULL_METADATA,
        CatalogPrivilege.VIEW_LIST,
        CatalogPrivilege.VIEW_READ_PROPERTIES,
        CatalogPrivilege.VIEW_FULL_METADATA,
    ],
    "catalog_manager": [
        # create and delete tables and views
        CatalogPrivilege.CATALOG_MANAGE_CONTENT,
        CatalogPrivilege.CATALOG_MANAGE_METADATA,
        CatalogPrivilege.NAMESPACE_FULL_METADATA,
        CatalogPrivilege.TABLE_FULL_METADATA,
        CatalogPrivilege.VIEW_FULL_METADATA,
    ],
    "catalog_reader": [
        # read data and metadata from table
        CatalogPrivilege.CATALOG_MANAGE_METADATA,
        CatalogPrivilege.NAMESPACE_LIST,
        CatalogPrivilege.NAMESPACE_READ_PROPERTIES,
        CatalogPrivilege.NAMESPACE_FULL_METADATA,
        CatalogPrivilege.TABLE_LIST,
        CatalogPrivilege.TABLE_READ_PROPERTIES,
        CatalogPrivilege.TABLE_FULL_METADATA,
        CatalogPrivilege.TABLE_READ_DATA,
        CatalogPrivilege.VIEW_LIST,
        CatalogPrivilege.VIEW_READ_PROPERTIES,
        CatalogPrivilege.VIEW_FULL_METADATA,
    ],
    "catalog_writer": [
        # write data to table
        CatalogPrivilege.CATALOG_MANAGE_METADATA,
        CatalogPrivilege.NAMESPACE_LIST,
        CatalogPrivilege.NAMESPACE_FULL_METADATA,
        CatalogPrivilege.TABLE_LIST,
        CatalogPrivilege.TABLE_READ_PROPERTIES,
        CatalogPrivilege.TABLE_FULL_METADATA,
        CatalogPrivilege.TABLE_READ_DATA,
        CatalogPrivilege.TABLE_WRITE_DATA,
        CatalogPrivilege.VIEW_LIST,
        CatalogPrivilege.VIEW_READ_PROPERTIES,
        CatalogPrivilege.VIEW_FULL_METADATA,
    ],
}


def create_catalog_roles(client):
    pass
