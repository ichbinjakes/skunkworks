from typing import Optional, List

from pydantic import BaseModel


class PolarisCatalogRole(BaseModel):
    """Catalog role schema."""

    name: str
    permissions: Optional[List[str]] = []


class PolarisPrincipalRole(BaseModel):
    """Principal role schema."""

    name: str
    catalog_roles: Optional[List[str]] = []


class PolarisPrincipals(BaseModel):
    """Principal to principal role mapping."""

    name: str
    principal_roles: Optional[List[str]] = []


class PolarisCatalog(BaseModel):
    """Catalog schema."""

    name: str
    default_base_location: str
    additional_properties: Optional[dict[str, str]] = None
    catalog_roles: Optional[List[PolarisCatalogRole]] = []
    principal_roles: Optional[List[PolarisPrincipalRole]] = []
    principals: Optional[List[PolarisPrincipals]]


class PolarisDeploymentYaml(BaseModel):
    """Schema defining Polaris deployment catalogs and roles."""

    catalogs: List[PolarisCatalog]
