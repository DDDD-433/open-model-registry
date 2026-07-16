#!/usr/bin/env python3
"""Estimate weight-only memory for one registry model."""

from __future__ import annotations

import argparse

from registry import load_registry, memory_estimates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Exact model_id from the registry")
    args = parser.parse_args()
    models = load_registry()["models"]
    matches = [model for model in models if model["model_id"] == args.model]
    if not matches:
        parser.error(f"model not found: {args.model}")
    model = matches[0]
    print(f"{model['name']} ({model['parameters']['total_b']}B total parameters)")
    for precision, gigabytes in memory_estimates(model["parameters"]["total_b"]).items():
        print(f"{precision}: {gigabytes:.2f} GB weight-only estimate")


if __name__ == "__main__":
    main()
