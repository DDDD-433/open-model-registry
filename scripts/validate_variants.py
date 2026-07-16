#!/usr/bin/env python3
"""Validate official deployment variants that fit a 16GB device budget."""

from __future__ import annotations

import sys
from datetime import date
from urllib.parse import urlparse

from registry import ROOT
import json


VARIANTS_PATH = ROOT / "models" / "deployment_variants.yaml"


def load_variants() -> dict:
    with VARIANTS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("target_ram_gb") != 16:
        errors.append("target_ram_gb must be 16")
    variants = data.get("variants")
    if not isinstance(variants, list) or not variants:
        return ["variants must be a non-empty list"]
    seen: set[str] = set()
    for index, variant in enumerate(variants):
        prefix = f"variants[{index}]"
        variant_id = variant.get("variant_id")
        if not isinstance(variant_id, str) or not variant_id:
            errors.append(f"{prefix}.variant_id must be a non-empty string")
        elif variant_id in seen:
            errors.append(f"duplicate variant_id: {variant_id}")
        else:
            seen.add(variant_id)
        if not isinstance(variant.get("total_parameters_b"), (int, float)) or variant["total_parameters_b"] <= 0:
            errors.append(f"{prefix}.total_parameters_b must be positive")
        parameter_scope = variant.get("parameter_scope", "in-scope")
        if parameter_scope not in {"in-scope", "edge-exception"}:
            errors.append(f"{prefix}.parameter_scope must be in-scope or edge-exception")
        elif isinstance(variant.get("total_parameters_b"), (int, float)):
            if variant["total_parameters_b"] >= 12 and parameter_scope != "edge-exception":
                errors.append(f"{prefix} models at or above 12B must be edge-exception records")
            if variant["total_parameters_b"] < 12 and parameter_scope == "edge-exception":
                errors.append(f"{prefix} below 12B cannot be labeled edge-exception")
            if parameter_scope == "edge-exception" and variant.get("fit_status") not in {"yes", "borderline"}:
                errors.append(f"{prefix} edge-exception must have fit_status yes or borderline")
        if variant.get("fit_status") == "yes" and variant.get("memory_estimate_gb") is None:
            errors.append(f"{prefix}.fit_status yes requires a memory estimate")
        if variant.get("memory_estimate_gb") is not None and variant["memory_estimate_gb"] > 16:
            errors.append(f"{prefix}.memory_estimate_gb exceeds the 16GB target")
        if variant.get("official_checkpoint") is not True:
            errors.append(f"{prefix}.official_checkpoint must be true")
        parsed = urlparse(variant.get("source_url", ""))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{prefix}.source_url must be an HTTP(S) URL")
        try:
            date.fromisoformat(variant.get("last_verified"))
        except (TypeError, ValueError):
            errors.append(f"{prefix}.last_verified must be an ISO date")
    return errors


if __name__ == "__main__":
    problems = validate(load_variants())
    if problems:
        print("Deployment variant validation failed:")
        print("\n".join(f"- {problem}" for problem in problems))
        sys.exit(1)
    print(f"Deployment variant registry valid: {len(load_variants()['variants'])} records")
