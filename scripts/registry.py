#!/usr/bin/env python3
"""Zero-dependency helpers for the JSON-compatible YAML registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "models" / "registry.yaml"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("registry root must be an object")
    return data


def memory_estimates(total_b: float) -> dict[str, float]:
    """Return weight-only decimal GB estimates for common precisions."""
    return {
        "fp16": round(total_b * 2, 2),
        "int8": round(total_b, 2),
        "int4": round(total_b * 0.5, 2),
    }
