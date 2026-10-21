from apache_polaris.sdk.management.api import PolarisDefaultApi
from apache_polaris.sdk.management import (
    Catalog,
    PolarisDefaultApi,
    CreateCatalogRequest,
    GrantCatalogRoleRequest,
    CatalogRole,
    AddGrantRequest,
    CatalogGrant,
    CatalogPrivilege,
    CreateCatalogRoleRequest,
    Principal,
    CreatePrincipalRequest,
    PrincipalRole,
    CreatePrincipalRoleRequest,
    GrantPrincipalRoleRequest,
    CatalogProperties,
)


from ice.deployment_model import PolarisCatalog, PolarisDeploymentYaml


def create_catalog(catalog: PolarisCatalog, client: PolarisDefaultApi):
    """Create the catalog, catalog roles, principal roles and principals."""

    # Create the catalog
    client.create_catalog(
        create_catalog_request=CreateCatalogRequest(
            Catalog(
                type="internal",
                name=catalog.name,
                properties=CatalogProperties(
                    default_base_location=catalog.default_base_location,
                    additional_properties=catalog.additional_properties,
                ),
            )
        )
    )

    # Create the catalog roles
    if catalog.catalog_roles:
        for role in catalog.catalog_roles:
            client.create_catalog_role(
                catalog_name=catalog.name,
                create_catalog_role_request=CreateCatalogRoleRequest(
                    catalogRole=CatalogRole(name=role.name)
                ),
            )
            # Grant permissions to the catalog role
            if role.permissions:
                for permission in role.permissions:
                    client.add_grant_to_catalog_role(
                        catalog_name=catalog.name,
                        catalog_role_name=role.name,
                        add_grant_request=AddGrantRequest(
                            grant=CatalogGrant(privilege=CatalogPrivilege(permission))
                        ),
                    )

    # Create the principal roles
    if catalog.principal_roles:
        for principal_role in catalog.principal_roles:
            client.create_principal_role(
                create_principal_role_request=CreatePrincipalRoleRequest(
                    principalRole=PrincipalRole(name=principal_role.name, federated=False)
                )
            )
            # Grant catalog roles to the principal role
            if principal_role.catalog_roles:
                for catalog_role in principal_role.catalog_roles:
                    client.assign_catalog_role_to_principal_role(
                        principal_role_name=principal_role.name,
                        catalog_name=catalog.name,
                        grant_catalog_role_request=GrantCatalogRoleRequest(
                            catalogRole=CatalogRole(name=catalog_role)
                        ),
                    )

    # Grant principal roles to the principals
    if catalog.principals:
        for principal in catalog.principals:
            client.create_principal(
                create_principal_request=CreatePrincipalRequest(
                    principal=Principal(principal.name)
                )
            )
            # Grant the principal roles to the principal
            if principal.principal_roles:
                for principal_role in principal.principal_roles:
                    client.assign_principal_role(
                        principal_name=principal.name,
                        grant_principal_role_request=GrantPrincipalRoleRequest(
                            principalRole=PrincipalRole(name=principal_role.name)
                        ),
                    )


def create_catalogs(deployment_yaml: PolarisDeploymentYaml, client: PolarisDefaultApi):
    """Create all catalogs, roles and principals specified in the deployment yaml file."""

    for catalog in deployment_yaml.catalogs:
        create_catalog(catalog, client)




# catalog_name = ""

# # TODO: get details from yaml file
# polaris_management_client.create_catalog(
#     create_catalog_request=CreateCatalogRequest(
#         Catalog(
#             type="internal",
#             name=catalog_name,
#             properties=CatalogProperties(default_base_location="", additional_properties={}),
#         )
#     )
# )

# catalog_roles = get_catalog_roles(catalog_name)
# for i in catalog_roles:
#     polaris_management_client.create_catalog_role(
#         catalog_name=catalog_name,
#         create_catalog_role_request=CreateCatalogRoleRequest(
#             catalogRole=CatalogRole(name=i, properties={})
#         ),
#     )
#     role_grants = get_catalog_role_grants(i.name)
#     for j in role_grants:
#         polaris_management_client.add_grant_to_catalog_role(
#             catalog_name=catalog_name,
#             catalog_role_name=i.name,
#             add_grant_request=AddGrantRequest(grant=CatalogGrant(privilege=j)),
#         )

# # TODO: create global principal roles
# for i in []:
#     polaris_management_client.create_principal_role()
#     for j in []:
#         polaris_management_client.assign_catalog_role_to_principal_role()


# for i in []:
#     polaris_management_client.create_principal()
#     for j in []:
#         polaris_management_client.assign_principal_role()
