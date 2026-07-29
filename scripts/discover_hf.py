#!/usr/bin/env python3
"""Discover possible official <=12B models from the public Hugging Face API.

Discovery is intentionally advisory: output goes to a candidate file and never
mutates the verified registry. A maintainer must review the model card, license,
provenance, and total parameter count before promotion.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from registry import ROOT, load_registry


API_URL = "https://huggingface.co/api/models"
EXCLUDED_MARKERS = {
    "adapter", "adapters", "awq", "bnb", "exl2", "gguf", "gptq", "int4", "int8",
    "lora", "merge", "merged", "quant", "quantized", "qlora", "safetensors-fp8",
    "tiny-random", "for-manga", "community-variant",
}
MODEL_PIPELINES = {
    "automatic-speech-recognition", "audio-classification", "image-classification",
    "image-text-to-text", "image-to-image", "image-to-text", "text-generation",
    "text2text-generation", "text-to-image", "text-to-audio", "text-to-speech",
}


def fetch_models(query: str, limit: int) -> list[dict[str, Any]]:
    params = urlencode({"search": query, "limit": limit, "full": "true", "sort": "downloads", "direction": "-1"})
    request = Request(f"{API_URL}?{params}", headers={"User-Agent": "open-model-registry/0.1"})
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("Hugging Face API returned an unexpected payload")
    return payload


def fetch_model_details(model_id: str) -> dict[str, Any]:
    request = Request(f"{API_URL}/{model_id}", headers={"User-Agent": "open-model-registry/0.1"})
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError("Hugging Face API returned an unexpected model payload")
    return payload


def parameter_count_billions(model: dict[str, Any]) -> float | None:
    safetensors = model.get("safetensors") or {}
    total = safetensors.get("total")
    if isinstance(total, (int, float)):
        return round(total / 1_000_000_000, 3)
    parameters = safetensors.get("parameters")
    if not isinstance(parameters, dict) or not parameters:
        return None
    numeric = [value for value in parameters.values() if isinstance(value, (int, float))]
    if not numeric:
        return None
    return round(max(numeric) / 1_000_000_000, 3)


def is_derivative(model: dict[str, Any]) -> bool:
    searchable = " ".join([str(model.get("modelId", "")), *[str(tag) for tag in model.get("tags", [])]]).lower()
    return any(marker in searchable for marker in EXCLUDED_MARKERS)


def category_guess(model: dict[str, Any]) -> str:
    pipeline = model.get("pipeline_tag")
    tags = {str(tag).lower() for tag in model.get("tags", [])}
    if "ocr" in tags or "document-parse" in tags:
        return "ocr-vision"
    if pipeline in {"image-text-to-text", "image-to-text", "image-to-image"} or "multimodal" in tags or "vision" in tags:
        return "vlm"
    if pipeline in {"automatic-speech-recognition", "audio-classification", "text-to-audio", "text-to-speech"} or "audio" in tags:
        return "audio"
    if "code" in tags or "coding" in tags:
        return "coding"
    return "llm"


def to_candidate(model: dict[str, Any], params_b: float) -> dict[str, Any]:
    model_id = model["modelId"]
    namespace = model_id.split("/", 1)[0] if "/" in model_id else None
    return {
        "model_id": model_id,
        "model_url": f"https://huggingface.co/{model_id}",
        "category_guess": category_guess(model),
        "parameters_total_b": params_b,
        "license": (model.get("cardData") or {}).get("license") or model.get("license"),
        "pipeline_tag": model.get("pipeline_tag"),
        "downloads": model.get("downloads", 0),
        "likes": model.get("likes", 0),
        "official_namespace": namespace,
        "tags": sorted(str(tag) for tag in model.get("tags", []) if str(tag) not in {"safetensors", "transformers"})[:20],
        "discovered_at": date.today().isoformat(),
        "review_status": "needs-review",
        "reasons": [
            "parameter count is inferred from public safetensors metadata",
            "license and original-developer provenance require human review",
            "candidate has not been promoted to the verified registry",
        ],
    }


def discover(queries: list[str], limit: int, existing_ids: set[str] | None = None) -> list[dict[str, Any]]:
    existing_ids = existing_ids or set()
    found: dict[str, dict[str, Any]] = {}
    for query in queries:
        for model in fetch_models(query, limit):
            model_id = model.get("modelId")
            if not model_id or model_id in existing_ids or is_derivative(model):
                continue
            if model.get("pipeline_tag") not in MODEL_PIPELINES:
                continue
            try:
                details = fetch_model_details(model_id)
            except Exception:
                continue
            params_b = parameter_count_billions(details)
            pipeline = details.get("pipeline_tag") or model.get("pipeline_tag")
            if params_b is None or params_b > 12 or pipeline not in MODEL_PIPELINES:
                continue
            candidate = to_candidate({**model, **details, "pipeline_tag": pipeline}, params_b)
            found[candidate["model_id"]] = candidate
    return sorted(found.values(), key=lambda item: (-item["downloads"], item["model_id"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", action="append", required=True, help="Hugging Face search query; repeatable")
    parser.add_argument("--limit", type=int, default=25, help="Results per query")
    parser.add_argument("--output", type=Path, default=ROOT / "models" / "candidates.json")
    args = parser.parse_args()
    registered_ids = {model["model_id"] for model in load_registry()["models"]}
    candidates = discover(args.query, args.limit, registered_ids)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"discovered_at": date.today().isoformat(), "candidates": candidates}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(candidates)} review candidates to {args.output}")


if __name__ == "__main__":
    main()
