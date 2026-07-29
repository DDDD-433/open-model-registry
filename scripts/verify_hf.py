#!/usr/bin/env python3
"""Check the verified registry against live Hugging Face model metadata."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen

from registry import load_registry


def fetch(model_id: str, timeout: float = 10.0) -> dict:
    request = Request(
        f"https://huggingface.co/api/models/{model_id}",
        headers={"User-Agent": "open-model-registry/0.1"},
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def live_parameters(model: dict) -> float | None:
    safetensors = model.get("safetensors") or {}
    total = safetensors.get("total")
    if isinstance(total, (int, float)):
        return total / 1_000_000_000
    values = (safetensors.get("parameters") or {}).values()
    numeric = [value for value in values if isinstance(value, (int, float))]
    return max(numeric) / 1_000_000_000 if numeric else None


def normalize_license(value: str | None) -> str | None:
    if value == "gemma":
        return "gemma-terms-of-use"
    if value == "falcon-llm-license":
        return "other"
    return value


def verify_registry(
    tolerance: float = 0.15,
    model_ids: set[str] | None = None,
    max_workers: int = 4,
) -> tuple[list[str], list[str], int]:
    records = [
        record for record in load_registry()["models"]
        if model_ids is None or record["model_id"] in model_ids
    ]
    errors: list[str] = []
    warnings: list[str] = []

    def check(record: dict) -> tuple[dict, dict | None, str | None]:
        try:
            return record, fetch(record["model_id"]), None
        except Exception as exc:  # network/API failures should be visible per record
            return record, None, str(exc)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check, record) for record in records]
        for future in as_completed(futures):
            record, live, failure = future.result()
            model_id = record["model_id"]
            if failure:
                errors.append(f"{model_id}: unavailable ({failure})")
                continue
            params = live_parameters(live)
            if params is not None and params > 12:
                errors.append(f"{model_id}: live total is {params:.3f}B, outside <=12B")
            expected = record["parameters"]["total_b"]
            if params is not None and abs(params - expected) > tolerance:
                errors.append(f"{model_id}: recorded {expected:g}B, live metadata {params:.3f}B")
            expected_license = normalize_license(record["openness"].get("license"))
            live_license = normalize_license((live.get("cardData") or {}).get("license") or live.get("license"))
            if expected_license and live_license and expected_license != live_license:
                warnings.append(f"{model_id}: recorded license {expected_license!r}, live API license {live_license!r}")

    return errors, warnings, len(records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tolerance", type=float, default=0.15, help="Allowed parameter-count difference in billions")
    parser.add_argument("--model", action="append", help="Verify only this model_id; repeatable")
    parser.add_argument("--max-workers", type=int, default=4, help="Concurrent API requests")
    args = parser.parse_args()
    errors, warnings, count = verify_registry(args.tolerance, set(args.model) if args.model else None, args.max_workers)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Live verification failed:")
        print("\n".join(f"- {error}" for error in errors))
        sys.exit(1)
    print(f"Live verification passed for {count} model records")
