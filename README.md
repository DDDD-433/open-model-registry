# Open Model Registry

A source-backed registry of original open and open-weight language, vision-language, coding, and OCR models below 12B total parameters.

The project is intentionally more structured than an “awesome list.” Each record separates:

- total parameters from active parameters;
- open-source claims from open-weight availability;
- official checkpoints from community derivatives;
- estimated weight memory from real runtime memory;
- model metadata from the sources used to verify it.

## Current status

The catalog now contains a curated set of language, coding, vision-language, audio, and OCR checkpoints. It is designed as a verified registry, not an exhaustive dump of every Hub derivative. Records must be verified against an official model card before they are treated as authoritative.

## Quick start

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_variants.py
python3 scripts/generate_readme.py
python3 scripts/estimate_memory.py --model Qwen/Qwen2.5-7B-Instruct
python3 scripts/verify_hf.py

# Discover new candidates without changing the verified registry
python3 scripts/discover_hf.py \
  --query "small language model" \
  --query "vision language model" \
  --query "OCR model"
```

The project has no runtime dependency: `models/registry.yaml` is written in JSON-compatible YAML, so the scripts can load it with Python’s standard library. JSON-compatible YAML is valid YAML 1.2 and keeps the initial contributor workflow installation-free.

## Inclusion rules

The primary catalog includes official checkpoints with `total_b < 12`. Official packed and quantized deployment variants are also tracked in `models/deployment_variants.yaml` when their original model is in scope or when they are important edge-deployment exceptions. They do not change the model’s true parameter count. Community derivatives, adapters, and unverified merges remain excluded.

The deployment-variant view is evaluated against a 16GB RAM target. A variant can be marked `yes`, `borderline`, `no`, or `unknown`; `yes` means the recorded evidence fits, not that every runtime workload will fit. Records at or above 12B use `parameter_scope: edge-exception` and are included only when an official packed format has documented 16GB-class deployment evidence.

Parameter counts are approximate when the original developer publishes an approximate count. Memory estimates are weight-only estimates; KV cache, activations, vision encoders, and runtime overhead can materially increase actual usage.

## Repository layout

```text
.
├── models/registry.yaml
├── models/deployment_variants.yaml
├── models/candidates.json
├── schema/model.schema.json
├── scripts/registry.py
├── scripts/validate_registry.py
├── scripts/validate_variants.py
├── scripts/generate_readme.py
├── scripts/discover_hf.py
├── scripts/estimate_memory.py
└── tests/test_registry.py
```

## Openness grades

| Grade | Meaning |
| --- | --- |
| A | Weights, code, training recipe, and meaningful data disclosure |
| B | Permissively licensed weights and inference code |
| C | Open weights under a custom commercial-use license |
| D | Research-only or noncommercial |
| U | License or provenance still unverified |

## Contributing

Add or update a record only when it has an official checkpoint URL and an official source URL. Run the validator and generated-table check before opening a pull request. Keep claims narrow and record uncertainty in `notes` rather than silently guessing.

## Discovery and review workflow

`scripts/discover_hf.py` uses the public Hugging Face API to find possible sub-12B checkpoints from model-card metadata. It excludes common derivative markers, then writes review-only results to `models/candidates.json`. Official quantized or packed artifacts are handled through the deployment-variant catalog rather than being silently discarded.

Discovery never promotes a model automatically. A maintainer should check:

1. the repository belongs to the original developer or an official organization;
2. total parameters, not active parameters, are below 12B;
3. the license is present in the model card and license file;
4. the checkpoint is official; packed/quantized artifacts go into the deployment-variant catalog, while adapters and community merges remain excluded;
5. the modalities, variant, and deployment claims are supported by the official documentation.

Only after that review should a candidate be copied into `models/registry.yaml`.

GitHub Actions run the offline validator and tests on every change, regenerate-check the README table, and perform a scheduled live Hugging Face verification of every registered model ID.

Prism ML’s Bonsai family is represented in `models/deployment_variants.yaml`, including FP16, MLX 1-bit/2-bit, GGUF, image-generation artifacts, and four documented 27B edge exceptions. These are linked to their source model or marked as deployment-only when a one-to-one base-model mapping is not applicable. The 27B records remain outside the primary `<12B` catalog.


## Catalog

<!-- BEGIN GENERATED MODEL TABLE -->
| Model | Category | Parameters | License | Grade | Modalities |
| --- | --- | ---: | --- | :---: | --- |
| `microsoft/Phi-4-multimodal-instruct` | audio | 5.57B | `mit` | B | text, image, audio |
| `openbmb/MiniCPM-o-2_6` | audio | 8.67B | `apache-2.0` | B | text, image, audio, video |
| `Qwen/Qwen2.5-Coder-0.5B-Instruct` | coding | 0.49B | `apache-2.0` | B | text |
| `Qwen/Qwen2.5-Coder-1.5B-Instruct` | coding | 1.54B | `apache-2.0` | B | text |
| `bigcode/starcoder2-3b` | coding | 3.03B | `bigcode-openrail-m` | C | text |
| `Qwen/Qwen2.5-Coder-3B-Instruct` | coding | 3.09B | `other` | U | text |
| `bigcode/starcoder2-7b` | coding | 7.17B | `bigcode-openrail-m` | C | text |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | coding | 7.62B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM-135M` | llm | 0.13B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-135M` | llm | 0.13B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM-360M` | llm | 0.36B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-360M` | llm | 0.36B | `apache-2.0` | A | text |
| `Qwen/Qwen3-0.6B` | llm | 0.75B | `apache-2.0` | B | text |
| `google/gemma-3-1b-it` | llm | 1B | `gemma-terms-of-use` | C | text |
| `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | llm | 1.1B | `apache-2.0` | A | text |
| `ibm-granite/granite-4.0-1b` | llm | 1.63B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM-1.7B` | llm | 1.71B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-1.7B` | llm | 1.71B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-1.7B-Instruct` | llm | 1.71B | `apache-2.0` | A | text |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` | llm | 1.78B | `mit` | B | text |
| `Qwen/Qwen3-1.7B` | llm | 2.03B | `apache-2.0` | B | text |
| `ibm-granite/granite-3.3-2b-instruct` | llm | 2.53B | `apache-2.0` | B | text |
| `google/gemma-2-2b-it` | llm | 2.61B | `gemma-terms-of-use` | C | text |
| `state-spaces/mamba-2.8b` | llm | 2.77B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM3-3B` | llm | 3.08B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM3-3B-Base` | llm | 3.08B | `apache-2.0` | B | text |
| `meta-llama/Llama-3.2-3B-Instruct` | llm | 3.21B | `llama3.2` | C | text |
| `ibm-granite/granite-4.0-micro` | llm | 3.4B | `apache-2.0` | B | text |
| `microsoft/Phi-3-mini-4k-instruct` | llm | 3.82B | `mit` | B | text |
| `microsoft/Phi-3.5-mini-instruct` | llm | 3.82B | `mit` | B | text |
| `microsoft/Phi-4-mini-instruct` | llm | 3.84B | `mit` | B | text |
| `Qwen/Qwen3-4B` | llm | 4.02B | `apache-2.0` | B | text |
| `01-ai/Yi-1.5-6B-Chat` | llm | 6.06B | `apache-2.0` | B | text |
| `EleutherAI/pythia-6.9b` | llm | 6.86B | `apache-2.0` | A | text |
| `allenai/OLMoE-1B-7B-0924` | llm | 6.92B | `apache-2.0` | A | text |
| `bigscience/bloom-7b1` | llm | 7.07B | `bigscience-bloom-rail-1.0` | C | text |
| `mistralai/Mistral-7B-Instruct-v0.3` | llm | 7.24B | `apache-2.0` | B | text |
| `allenai/OLMo-2-1124-7B` | llm | 7.3B | `apache-2.0` | A | text |
| `allenai/OLMo-2-1124-7B-Instruct` | llm | 7.3B | `apache-2.0` | A | text |
| `tiiuae/Falcon3-7B-Instruct` | llm | 7.46B | `falcon-llm-license` | C | text |
| `Qwen/Qwen2.5-7B-Instruct` | llm | 7.61B | `apache-2.0` | B | text |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | llm | 7.62B | `mit` | B | text |
| `CohereForAI/c4ai-command-r7b-12-2024` | llm | 8.03B | `cc-by-nc-4.0` | D | text |
| `deepseek-ai/DeepSeek-R1-Distill-Llama-8B` | llm | 8.03B | `mit` | B | text |
| `ibm-granite/granite-3.3-8b-instruct` | llm | 8.17B | `apache-2.0` | B | text |
| `Qwen/Qwen3-8B` | llm | 8.19B | `apache-2.0` | B | text |
| `01-ai/Yi-1.5-9B-Chat` | llm | 8.83B | `apache-2.0` | B | text |
| `google/gemma-2-9b-it` | llm | 9.24B | `gemma-terms-of-use` | C | text |
| `tiiuae/Falcon3-10B-Instruct` | llm | 10.31B | `falcon-llm-license` | C | text |
| `microsoft/Florence-2-base` | ocr-vision | 0.23B | `mit` | B | image, text |
| `stepfun-ai/GOT-OCR2_0` | ocr-vision | 0.72B | `apache-2.0` | B | image, text |
| `PaddlePaddle/PaddleOCR-VL` | ocr-vision | 0.96B | `apache-2.0` | B | image, text |
| `PaddlePaddle/PaddleOCR-VL-1.5` | ocr-vision | 0.96B | `apache-2.0` | B | image, text |
| `PaddlePaddle/PaddleOCR-VL-1.6` | ocr-vision | 0.96B | `apache-2.0` | B | image, text |
| `rednote-hilab/dots.ocr` | ocr-vision | 3.04B | `mit` | B | image, text |
| `deepseek-ai/DeepSeek-OCR` | ocr-vision | 3.34B | `mit` | B | image, text |
| `HuggingFaceTB/SmolVLM-256M-Instruct` | vlm | 0.26B | `apache-2.0` | B | text, image, video |
| `HuggingFaceTB/SmolVLM-500M-Instruct` | vlm | 0.5B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3.5-0.8B` | vlm | 0.87B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3-1B` | vlm | 0.94B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3_5-1B` | vlm | 1.06B | `apache-2.0` | B | text, image |
| `microsoft/kosmos-2-patch14-224` | vlm | 1.66B | `mit` | B | text, image |
| `vikhyatk/moondream2` | vlm | 1.93B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3-2B` | vlm | 2.09B | `apache-2.0` | B | text, image |
| `Qwen/Qwen3-VL-2B-Instruct` | vlm | 2.13B | `apache-2.0` | B | text, image, video |
| `OpenGVLab/InternVL2-2B` | vlm | 2.21B | `mit` | B | text, image |
| `Qwen/Qwen2-VL-2B-Instruct` | vlm | 2.21B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3.5-2B` | vlm | 2.27B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3_5-2B` | vlm | 2.35B | `apache-2.0` | B | text, image |
| `google/paligemma2-3b-pt-224` | vlm | 3.03B | `gemma-terms-of-use` | C | text, image |
| `Qwen/Qwen2.5-VL-3B-Instruct` | vlm | 3.75B | `apache-2.0` | B | text, image, video |
| `mistralai/Ministral-3-3B-Instruct-2512-BF16` | vlm | 3.85B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL2-4B` | vlm | 4.15B | `mit` | B | text, image |
| `microsoft/phi-3.5-vision-instruct` | vlm | 4.15B | `mit` | B | text, image |
| `google/gemma-3-4b-it` | vlm | 4.3B | `gemma-terms-of-use` | C | text, image |
| `Qwen/Qwen3-VL-4B-Instruct` | vlm | 4.44B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3.5-4B` | vlm | 4.66B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3_5-4B` | vlm | 4.73B | `apache-2.0` | B | text, image |
| `google/gemma-4-E2B` | vlm | 5.12B | `apache-2.0` | B | text, image, audio |
| `OpenGVLab/InternVL3-8B` | vlm | 7.94B | `apache-2.0` | B | text, image |
| `google/gemma-4-E4B` | vlm | 8B | `apache-2.0` | B | text, image, audio |
| `allenai/Molmo-7B-D-0924` | vlm | 8.02B | `apache-2.0` | A | text, image |
| `OpenGVLab/InternVL2-8B` | vlm | 8.08B | `mit` | B | text, image |
| `Qwen/Qwen2-VL-7B-Instruct` | vlm | 8.29B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen2.5-VL-7B-Instruct` | vlm | 8.29B | `apache-2.0` | B | text, image, video |
| `HuggingFaceM4/idefics2-8b` | vlm | 8.4B | `apache-2.0` | A | text, image |
| `OpenGVLab/InternVL3_5-8B` | vlm | 8.53B | `apache-2.0` | B | text, image |
| `openbmb/MiniCPM-V-4_5` | vlm | 8.7B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3-VL-8B-Instruct` | vlm | 8.77B | `apache-2.0` | B | text, image, video |
| `mistralai/Ministral-3-8B-Instruct-2512-BF16` | vlm | 8.92B | `apache-2.0` | B | text, image |
| `Qwen/Qwen3.5-9B` | vlm | 9.65B | `apache-2.0` | B | text, image |
| `google/paligemma2-10b-pt-224` | vlm | 9.66B | `gemma-terms-of-use` | C | text, image |
<!-- END GENERATED MODEL TABLE -->
