#!/usr/bin/env python3
"""Validate models that exceed 12B total parameters but have edge-deployment evidence."""

from __future__ import annotations

import json
import sys
from datetime import date
from urllib.parse import urlparse

from registry import ROOT, load_registry


EXCEPTIONS_PATH = ROOT / "models" / "edge_exceptions.yaml"


def load_exceptions() -> dict:
    with EXCEPTIONS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("target_ram_gb") != 16:
        errors.append("target_ram_gb must be 16")
    exceptions = data.get("exceptions")
    if not isinstance(exceptions, list) or not exceptions:
        return ["exceptions must be a non-empty list"]
    seen: set[str] = set()
    primary_ids = {item["model_id"] for item in load_registry()["models"]}
    for index, item in enumerate(exceptions):
        prefix = f"exceptions[{index}]"
        model_id = item.get("model_id")
        if not isinstance(model_id, str) or not model_id:
            errors.append(f"{prefix}.model_id must be a non-empty string")
        elif model_id in seen:
            errors.append(f"duplicate model_id: {model_id}")
        else:
            seen.add(model_id)
        if model_id in primary_ids:
            errors.append(f"{prefix}.model_id is also present in the primary registry")
        total = item.get("total_parameters_b")
        active = item.get("active_parameters_b")
        if not isinstance(total, (int, float)) or total <= 12:
            errors.append(f"{prefix}.total_parameters_b must be above 12")
        if active is not None and (not isinstance(active, (int, float)) or active <= 0 or active > total):
            errors.append(f"{prefix}.active_parameters_b must be positive and no greater than total")
        if item.get("fit_status") in {"yes", "borderline", "conditional"}:
            memory = item.get("memory_estimate_gb")
            if not isinstance(memory, (int, float)) or memory > 16:
                errors.append(f"{prefix} deployable records require a memory estimate at or below 16GB")
        if item.get("official_checkpoint") is not True:
            errors.append(f"{prefix}.official_checkpoint must be true")
        parsed = urlparse(item.get("source_url", ""))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{prefix}.source_url must be an HTTP(S) URL")
        try:
            date.fromisoformat(item.get("last_verified"))
        except (TypeError, ValueError):
            errors.append(f"{prefix}.last_verified must be an ISO date")
    return errors


if __name__ == "__main__":
    problems = validate(load_exceptions())
    if problems:
        print("Edge-exception validation failed:")
        print("\n".join(f"- {problem}" for problem in problems))
        sys.exit(1)
    print(f"Edge-exception registry valid: {len(load_exceptions()['exceptions'])} records")
