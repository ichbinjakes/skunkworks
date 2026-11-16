#!/usr/bin/env python3
"""Create an Iceberg table in Apache Polaris and append random data to it.

Requires:
    pip install "pyiceberg[pyarrow]" pyarrow boto3

Environment:
    POLARIS_HOST       default http://localhost:8181
    POLARIS_CLIENT_ID  default root
    POLARIS_SECRET     default s3cr3t
    S3_ENDPOINT        default http://localhost:9000
    AWS_ACCESS_KEY_ID  default admin
    AWS_SECRET_ACCESS_KEY default password123
"""

import argparse
import os
import random
import uuid
from datetime import datetime, timedelta, timezone

import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.catalog.rest import RestCatalog
from pyiceberg.schema import Schema
from pyiceberg.types import (
    BooleanType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    NestedField,
    StringType,
    TimestamptzType,
)

NAMESPACE = ("raw", "bronze", "silver", "gold")
CATALOG_NAME = "shadow_catalog"
TABLE_NAME = "random_events"
S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "http://localhost:9000")
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", "admin")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "password123")


def get_catalog() -> RestCatalog:
    catalog = load_catalog(
        "default",
        type="rest",
        uri=f"{os.environ.get('POLARIS_HOST', 'http://localhost:8181')}/api/catalog",
        warehouse="shadow_catalog",
        token=f"{os.environ.get('POLARIS_CLIENT_ID', 'root')}:{os.environ.get('POLARIS_SECRET', 's3cr3t')}",
        **{
            "s3.endpoint": S3_ENDPOINT,
            "s3.access-key-id": ACCESS_KEY,
            "s3.secret-access-key": SECRET_KEY,
            "s3.path-style-access": "true",
        },
    )
    return catalog


def table_schema() -> Schema:
    return Schema(
        NestedField(1, "event_id", StringType(), required=True),
        NestedField(2, "user_id", LongType(), required=False),
        NestedField(3, "session_count", IntegerType(), required=False),
        NestedField(4, "score", DoubleType(), required=False),
        NestedField(5, "ratio", FloatType(), required=False),
        NestedField(6, "is_active", BooleanType(), required=False),
        NestedField(7, "country", StringType(), required=False),
        NestedField(8, "device", StringType(), required=False),
        NestedField(9, "event_ts", TimestamptzType(), required=False),
    )


def create_table(catalog: RestCatalog) -> None:
    if NAMESPACE[0] not in catalog.list_namespaces() and not catalog.namespace_exists(NAMESPACE):
        catalog.create_namespace(NAMESPACE)
        print(f"created namespace {NAMESPACE}")

    if catalog.table_exists(TABLE_NAME, NAMESPACE):
        print(f"table {NAMESPACE}.{TABLE_NAME} already exists, reusing it")
        return

    catalog.create_table(
        identifier=f"{NAMESPACE}.{TABLE_NAME}",
        schema=table_schema(),
        partition_spec=None,
        location=f"s3://shadow-catalog/{NAMESPACE[0]}/{TABLE_NAME}",
        properties={"write.format.default": "parquet"},
    )
    print(f"created table {NAMESPACE}.{TABLE_NAME}")


def random_rows(count: int) -> pa.Table:
    countries = ["US", "GB", "DE", "FR", "JP", "BR", "IN", "AU", "CA", "MX"]
    devices = ["mobile", "desktop", "tablet", "tv", "watch"]
    now = datetime.now(timezone.utc)

    batch = []
    for _ in range(count):
        batch.append(
            (
                str(uuid.uuid4()),
                random.randint(1, 100_000),
                random.randint(0, 250),
                random.uniform(0.0, 1000.0),
                random.uniform(0.0, 1.0),
                random.choice([True, False]),
                random.choice(countries),
                random.choice(devices),
                now - timedelta(seconds=random.randint(0, 86_400 * 30)),
            )
        )

    return pa.Table.from_pylist(
        [dict(zip(table_schema().column_names, row)) for row in batch],
        schema=table_schema().as_arrow(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create and append random data to an Iceberg table")
    parser.add_argument("--rows", type=int, default=1_000, help="rows to append (default 1000)")
    parser.add_argument("--seed", type=int, default=None, help="seed the RNG for reproducible data")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    catalog = get_catalog()
    create_table(catalog)

    data = random_rows(args.rows)
    table = catalog.load_table(f"{NAMESPACE}.{TABLE_NAME}")
    table.append(data)
    print(f"appended {args.rows} rows to {NAMESPACE}.{TABLE_NAME}")
    print(f"table now has {len(table.scan().to_arrow())} rows")


if __name__ == "__main__":
    main()