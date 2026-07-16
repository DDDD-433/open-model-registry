#!/usr/bin/env python3
"""Validate registry invariants without requiring third-party packages."""

from __future__ import annotations

import sys
from collections import Counter
from datetime import date
from urllib.parse import urlparse

from registry import load_registry


VALID_CATEGORIES = {"llm", "vlm", "ocr-vision", "coding", "audio", "embedding", "other"}
VALID_GRADES = {"A", "B", "C", "D", "U"}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    models = data.get("models")
    if not isinstance(models, list) or not models:
        return ["models must be a non-empty list"]

    seen: set[str] = set()
    for index, model in enumerate(models):
        prefix = f"models[{index}]"
        if not isinstance(model, dict):
            errors.append(f"{prefix} must be an object")
            continue
        model_id = model.get("model_id")
        if not isinstance(model_id, str) or not model_id:
            errors.append(f"{prefix}.model_id must be a non-empty string")
        elif model_id in seen:
            errors.append(f"duplicate model_id: {model_id}")
        else:
            seen.add(model_id)

        category = model.get("category")
        if category not in VALID_CATEGORIES:
            errors.append(f"{prefix}.category is invalid: {category!r}")
        parameters = model.get("parameters", {})
        total_b = parameters.get("total_b") if isinstance(parameters, dict) else None
        if not isinstance(total_b, (int, float)) or not 0 < total_b < 12:
            errors.append(f"{prefix}.parameters.total_b must be between 0 and 12")

        openness = model.get("openness", {})
        if not isinstance(openness, dict) or openness.get("grade") not in VALID_GRADES:
            errors.append(f"{prefix}.openness.grade is invalid")

        sources = model.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}.sources must contain at least one URL")
        else:
            for source in sources:
                parsed = urlparse(source)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{prefix} has invalid source URL: {source!r}")

        if model.get("official_checkpoint") is not True:
            errors.append(f"{prefix}.official_checkpoint must be true for the primary catalog")

        last_verified = model.get("last_verified")
        if last_verified is not None:
            try:
                date.fromisoformat(last_verified)
            except (TypeError, ValueError):
                errors.append(f"{prefix}.last_verified must be an ISO date")

        license_name = openness.get("license") if isinstance(openness, dict) else None
        if license_name in {"other", None, ""} and (not isinstance(openness, dict) or openness.get("grade") != "U"):
            errors.append(f"{prefix} uses an unclassified license but is not graded U")

    return errors


if __name__ == "__main__":
    problems = validate(load_registry())
    if problems:
        print("Registry validation failed:")
        print("\n".join(f"- {problem}" for problem in problems))
        sys.exit(1)
    registry = load_registry()
    count = len(registry["models"])
    categories = Counter(model["category"] for model in registry["models"])
    grades = Counter(model["openness"]["grade"] for model in registry["models"])
    print(f"Registry valid: {count} model records")
    print("Categories: " + ", ".join(f"{key}={value}" for key, value in sorted(categories.items())))
    print("Grades: " + ", ".join(f"{key}={value}" for key, value in sorted(grades.items())))
