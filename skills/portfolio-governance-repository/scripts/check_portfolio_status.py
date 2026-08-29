#!/usr/bin/env python3
"""Check compact portfolio registry and status records for drift."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
STATES = {"live", "preview", "experimental", "planned", "retired"}


def check(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    products = value.get("products")
    integrations = value.get("integrations")
    records = value.get("status_records")
    if not isinstance(products, list):
        errors.append("products must be an array")
        products = []
    if not isinstance(integrations, list):
        errors.append("integrations must be an array")
        integrations = []
    if not isinstance(records, list):
        errors.append("status_records must be an array")
        records = []

    product_map: dict[str, dict[str, Any]] = {}
    for index, product in enumerate(products):
        if not isinstance(product, dict):
            errors.append(f"products[{index}] must be an object")
            continue
        product_id = product.get("id")
        if not isinstance(product_id, str) or not product_id:
            errors.append(f"products[{index}] has no id")
            continue
        if product_id in product_map:
            errors.append(f"duplicate product id: {product_id}")
        product_map[product_id] = product
        if not isinstance(product.get("primary_role"), str) or not product.get("primary_role"):
            errors.append(f"product {product_id} has no primary role")
        if product.get("current_state") not in STATES:
            errors.append(f"product {product_id} has invalid current state")
        if not isinstance(product.get("status_commit"), str) or not SHA_PATTERN.fullmatch(product["status_commit"]):
            errors.append(f"product {product_id} has invalid status commit")

    integration_ids: set[str] = set()
    for index, integration in enumerate(integrations):
        if not isinstance(integration, dict):
            errors.append(f"integrations[{index}] must be an object")
            continue
        integration_id = integration.get("id")
        if not isinstance(integration_id, str) or not integration_id:
            errors.append(f"integrations[{index}] has no id")
        elif integration_id in integration_ids:
            errors.append(f"duplicate integration id: {integration_id}")
        else:
            integration_ids.add(integration_id)
        for endpoint in ("from", "to"):
            if integration.get(endpoint) not in product_map:
                errors.append(f"integration {integration_id} has unknown {endpoint} product")
        if integration.get("state") not in STATES:
            errors.append(f"integration {integration_id} has invalid state")
        if integration.get("state") in {"live", "preview"} and not integration.get("contract"):
            errors.append(f"integration {integration_id} needs a contract")

    status_map: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"status_records[{index}] must be an object")
            continue
        product_id = record.get("product")
        if product_id in status_map:
            errors.append(f"duplicate status record: {product_id}")
        elif isinstance(product_id, str):
            status_map[product_id] = record
    for product_id, product in product_map.items():
        record = status_map.get(product_id)
        if not record:
            errors.append(f"missing status record: {product_id}")
            continue
        if record.get("commit") != product.get("status_commit"):
            errors.append(f"status commit drift: {product_id}")
        if record.get("current_state") != product.get("current_state"):
            errors.append(f"status lifecycle drift: {product_id}")
    for product_id in status_map:
        if product_id not in product_map:
            errors.append(f"status record references unknown product: {product_id}")

    return {"verdict": "ALIGNED" if not errors else "DRIFT", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("portfolio", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.portfolio.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "DRIFT", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "DRIFT", "errors": ["portfolio must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "ALIGNED" else 1


if __name__ == "__main__":
    sys.exit(main())
