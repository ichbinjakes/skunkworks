import requests

# from apache_polaris.sdk.management.api import PolarisDefaultApi
# from apache_polaris.sdk.management import ApiClient, PolarisDefaultApi, Configuration
from apache_polaris.sdk.catalog.api.iceberg_o_auth2_api import IcebergOAuth2API
from apache_polaris.sdk.catalog.api_client import ApiClient as CatalogApiClient
from apache_polaris.sdk.catalog.api_client import Configuration as CatalogApiClientConfiguration
from apache_polaris.sdk.management import (
    ApiClient,
    PolarisDefaultApi,
    Configuration,

)


# Get dex token:
response = requests.post(
    "http://localhost:5556/dex/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "password",
        "client_id": "polaris",
        "scope": "openid profile groups",
        "username": "finance@example.com",
        "password": "password",
    },
)


client_id, client_secret = "root", "s3cr3t"
polaris_catalog_url = "http://localhost:8181"

client = CatalogApiClient(
    CatalogApiClientConfiguration(
        username=client_id, password=client_secret, host=polaris_catalog_url
    )
)
oauth_api = IcebergOAuth2API(client)
token = oauth_api.get_token(
    scope="PRINCIPAL_ROLE:ALL",
    client_id=client_id,
    client_secret=client_secret,
    grant_type="client_credentials",
    _headers={"realm": "POLARIS"},
)

client = ApiClient(
    Configuration(access_token=token.access_token, host=polaris_catalog_url)
)
polaris_management_client = PolarisDefaultApi(client)

breakpoint()
