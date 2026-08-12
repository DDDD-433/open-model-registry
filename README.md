# Open Model Registry

A source-backed registry of original open and open-weight language, vision-language, coding, audio, OCR, and specialist models at or below 12B total parameters.

The project is intentionally more structured than an “awesome list.” Each record separates:

- total parameters from active parameters;
- open-source claims from open-weight availability;
- official checkpoints from community derivatives;
- estimated weight memory from real runtime memory;
- model metadata from the sources used to verify it.
- field-level evidence for parameters, licensing, release dates, modalities, and deployment claims.

## Current status

The catalog now contains a curated set of language, coding, vision-language, audio, and OCR checkpoints. It is designed as a verified registry, not an exhaustive dump of every Hub derivative. Records must be verified against an official model card before they are treated as authoritative.

## Quick start

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_variants.py
python3 scripts/validate_edge_exceptions.py
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

The primary catalog includes official checkpoints with `total_b <= 12`, including explicitly marked exact-cutoff records. Official packed and quantized deployment variants of in-scope models are tracked in `models/deployment_variants.yaml`; they do not change the model’s true parameter count. Models above 12B that can still be practical on a 16GB device are tracked separately in `models/edge_exceptions.yaml` and never count toward the primary catalog. Community derivatives, adapters, and unverified merges remain excluded.

The deployment-variant view is evaluated against a 16GB RAM target. A variant can be marked `yes`, `borderline`, `no`, or `unknown`; `yes` means the recorded evidence fits, not that every runtime workload will fit. The edge-exception view separately records models above 12B total parameters when an official packed format or active-parameter architecture has documented 16GB-class deployment evidence.

Parameter counts are approximate when the original developer publishes an approximate count. Memory estimates are weight-only estimates; KV cache, activations, vision encoders, and runtime overhead can materially increase actual usage.

New and corrected records use the optional `evidence` object to identify which model card, safetensors metadata, paper, release announcement, or runtime test supports each field. Evidence revisions are pinned when available; a `null` revision means the source still needs commit-level pinning.

## Repository layout

```text
.
├── models/registry.yaml
├── models/deployment_variants.yaml
├── models/edge_exceptions.yaml
├── models/candidates.json
├── schema/model.schema.json
├── scripts/registry.py
├── scripts/validate_registry.py
├── scripts/validate_variants.py
├── scripts/validate_edge_exceptions.py
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

`scripts/discover_hf.py` uses the public Hugging Face API to find possible <=12B checkpoints from model-card metadata. It excludes common derivative markers, then writes review-only results to `models/candidates.json`. Official quantized or packed artifacts are handled through the deployment-variant catalog rather than being silently discarded.

Discovery never promotes a model automatically. A maintainer should check:

1. the repository belongs to the original developer or an official organization;
2. total parameters, not active parameters, are at or below 12B;
3. the license is present in the model card and license file;
4. the checkpoint is official; packed/quantized artifacts go into the deployment-variant catalog, while adapters and community merges remain excluded;
5. the modalities, variant, and deployment claims are supported by the official documentation.

Only after that review should a candidate be copied into `models/registry.yaml`.

GitHub Actions run the offline validator and tests on every change, regenerate-check the README table, and perform a scheduled live Hugging Face verification of every registered model ID.

Prism ML’s Bonsai family is represented across the deployment and edge-exception catalogs. Its in-scope FP16, MLX 1-bit/2-bit, GGUF, and image-generation artifacts remain in `models/deployment_variants.yaml`; the four documented 27B variants are in `models/edge_exceptions.yaml` and remain outside the primary `<=12B` catalog.

## Edge exceptions

`models/edge_exceptions.yaml` contains models that exceed 12B total parameters but may still be useful on a 16GB device after quantization or because of sparse MoE routing. Examples include Qwen3-30B-A3B, GPT-OSS-20B, DeepSeek-Coder-V2-Lite, and Prism ML’s 27B Bonsai variants.

These records are intentionally separate: active parameters can reduce compute, and quantization can reduce memory, but neither changes total parameter eligibility. Edge exceptions never inflate the primary model count.


## Catalog

<!-- BEGIN GENERATED MODEL TABLE -->
| Model | Category | Parameters | License | Grade | Modalities |
| --- | --- | ---: | --- | :---: | --- |
| `openai/whisper-large-v3-turbo` | audio | 0.809B | `mit` | B | audio |
| `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` | audio | 0.906B | `apache-2.0` | B | text |
| `OpenMOSS-Team/MOSS-Transcribe-Diarize` | audio | 0.91B | `apache-2.0` | B | audio, video, text |
| `Qwen/Qwen3-TTS-12Hz-0.6B-Base` | audio | 0.915B | `apache-2.0` | B | text, audio |
| `Qwen/Qwen3-ForcedAligner-0.6B` | audio | 0.918B | `apache-2.0` | B | audio, text |
| `Qwen/Qwen3-ASR-0.6B` | audio | 0.938B | `apache-2.0` | B | audio |
| `LiquidAI/LFM2-Audio-1.5B` | audio | 1.47B | `liquid-ai-open` | C | audio, text |
| `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | audio | 1.929B | `apache-2.0` | B | text, audio |
| `openbmb/VoxCPM2` | audio | 2.29B | `apache-2.0` | B | text |
| `Qwen/Qwen3-ASR-1.7B` | audio | 2.349B | `apache-2.0` | B | audio |
| `mistralai/Voxtral-4B-TTS-2603` | audio | 4B | `cc-by-nc-4.0` | D | text |
| `laion/moss-tts-local-transformer-4.55b-voice-acting` | audio | 4.13B | `apache-2.0` | A | text |
| `mistralai/Voxtral-Mini-4B-Realtime-2602` | audio | 4.43B | `apache-2.0` | B | audio |
| `mistralai/Voxtral-Mini-3B-2507` | audio | 4.68B | `apache-2.0` | B | text, audio |
| `google/gemma-3n-E2B` | audio | 5.44B | `gemma-terms-of-use` | C | text, image, audio, video |
| `google/gemma-3n-E2B-it` | audio | 5.44B | `gemma-terms-of-use` | C | text, image, audio, video |
| `Qwen/Qwen2.5-Omni-3B` | audio | 5.54B | `qwen-research` | D | text, image, audio, video |
| `google/gemma-3n-E4B` | audio | 7.85B | `gemma-terms-of-use` | C | text, image, audio, video |
| `google/gemma-3n-E4B-it` | audio | 7.85B | `gemma-terms-of-use` | C | text, image, audio, video |
| `OpenMOSS-Team/MOSS-TTS-v1.5` | audio | 8.49B | `apache-2.0` | B | text, audio |
| `microsoft/VibeVoice-ASR` | audio | 8.67B | `mit` | B | audio |
| `openbmb/MiniCPM-o-2_6` | audio | 8.67B | `apache-2.0` | B | text, image, audio, video |
| `OpenMOSS-Team/MOSS-Music-8B-Instruct` | audio | 9.05B | `apache-2.0` | B | text, audio |
| `OpenMOSS-Team/MOSS-Music-8B-Thinking` | audio | 9.05B | `apache-2.0` | B | text, audio |
| `openbmb/MiniCPM-o-4_5` | audio | 9.372B | `apache-2.0` | B | text, image, audio, video |
| `ai-sage/GigaChat3.1-Audio-10B-A1.8B` | audio | 10B | `mit` | B | text, audio |
| `Qwen/Qwen2.5-Omni-7B` | audio | 10.73B | `qwen-research` | D | text, image, audio, video |
| `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` | audio | 11.095B | `openmdw-1.1` | C | text, audio |
| `google/gemma-4-12B` | audio | 11.96B | `apache-2.0` | B | text, image, audio |
| `google/gemma-4-12B-it` | audio | 11.96B | `apache-2.0` | B | text, image, audio |
| `fdtn-ai/antares-350m` | coding | 0.35B | `apache-2.0` | B | text, code |
| `Qwen/Qwen2.5-Coder-0.5B-Instruct` | coding | 0.49B | `apache-2.0` | B | text |
| `fdtn-ai/antares-1b` | coding | 1B | `apache-2.0` | B | text, code |
| `Qwen/Qwen2.5-Coder-1.5B-Instruct` | coding | 1.54B | `apache-2.0` | B | text |
| `bigcode/starcoder2-3b` | coding | 3.03B | `bigcode-openrail-m` | C | text |
| `Qwen/Qwen2.5-Coder-3B-Instruct` | coding | 3.09B | `qwen-research` | D | text |
| `bigcode/starcoder2-7b` | coding | 7.17B | `bigcode-openrail-m` | C | text |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | coding | 7.62B | `apache-2.0` | B | text |
| `LiquidAI/LFM2.5-Encoder-230M` | embedding | 0.23B | `lfm1.0` | C | text |
| `microsoft/bitnet-embedding-270m` | embedding | 0.27B | `mit` | B | text |
| `LiquidAI/LFM2.5-ColBERT-350M` | embedding | 0.35B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-Embedding-350M` | embedding | 0.35B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-Encoder-350M` | embedding | 0.35B | `lfm1.0` | C | text |
| `microsoft/bitnet-embedding-0.6b` | embedding | 0.6B | `mit` | B | text |
| `nvidia/Nemotron-3-Embed-1B-BF16` | embedding | 1.141B | `openmdw-1.1` | C | text |
| `nvidia/Nemotron-3-Embed-8B-BF16` | embedding | 7.953B | `openmdw-1.1` | C | text |
| `HuggingFaceTB/SmolLM-135M` | llm | 0.13B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-135M` | llm | 0.13B | `apache-2.0` | A | text |
| `LiquidAI/LFM2.5-230M` | llm | 0.23B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-230M-Base` | llm | 0.23B | `lfm1.0` | C | text |
| `MultiverseComputingCAI/LittleLamb` | llm | 0.29B | `apache-2.0` | B | text |
| `LiquidAI/LFM2.5-350M` | llm | 0.35B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-350M-Base` | llm | 0.35B | `lfm1.0` | C | text |
| `HuggingFaceTB/SmolLM-360M` | llm | 0.36B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-360M` | llm | 0.36B | `apache-2.0` | A | text |
| `openbmb/MiniCPM4-0.5B` | llm | 0.43B | `apache-2.0` | B | text |
| `Qwen/Qwen3-0.6B` | llm | 0.75B | `apache-2.0` | B | text |
| `google/gemma-3-1b-it` | llm | 1B | `gemma-terms-of-use` | C | text |
| `openbmb/MiniCPM5-1B` | llm | 1.081B | `apache-2.0` | B | text |
| `openbmb/MiniCPM5-1B-Base` | llm | 1.081B | `apache-2.0` | B | text |
| `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | llm | 1.1B | `apache-2.0` | A | text |
| `LiquidAI/LFM2.5-1.2B-Instruct` | llm | 1.17B | `liquid-ai-open` | C | text |
| `LiquidAI/LFM2.5-1.2B-Base` | llm | 1.2B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-1.2B-Thinking` | llm | 1.2B | `lfm1.0` | C | text |
| `ibm-granite/granite-4.0-1b` | llm | 1.63B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM-1.7B` | llm | 1.71B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-1.7B` | llm | 1.71B | `apache-2.0` | A | text |
| `HuggingFaceTB/SmolLM2-1.7B-Instruct` | llm | 1.71B | `apache-2.0` | A | text |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` | llm | 1.78B | `mit` | B | text |
| `Qwen/Qwen3-1.7B` | llm | 2.03B | `apache-2.0` | B | text |
| `ibm-granite/granite-3.3-2b-instruct` | llm | 2.53B | `apache-2.0` | B | text |
| `google/gemma-2-2b-it` | llm | 2.61B | `gemma-terms-of-use` | C | text |
| `LiquidAI/LFM2.5-2.6B` | llm | 2.69B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-2.6B-Base` | llm | 2.69B | `lfm1.0` | C | text |
| `state-spaces/mamba-2.8b` | llm | 2.77B | `apache-2.0` | B | text |
| `ai21labs/AI21-Jamba2-3B` | llm | 3B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM3-3B` | llm | 3.08B | `apache-2.0` | B | text |
| `HuggingFaceTB/SmolLM3-3B-Base` | llm | 3.08B | `apache-2.0` | B | text |
| `meta-llama/Llama-3.2-3B-Instruct` | llm | 3.21B | `llama3.2` | C | text |
| `CohereLabs/tiny-aya-global` | llm | 3.35B | `cc-by-nc-4.0` | D | text |
| `ibm-granite/granite-4.0-micro` | llm | 3.4B | `apache-2.0` | B | text |
| `microsoft/Phi-3-mini-4k-instruct` | llm | 3.82B | `mit` | B | text |
| `microsoft/Phi-3.5-mini-instruct` | llm | 3.82B | `mit` | B | text |
| `microsoft/Phi-4-mini-instruct` | llm | 3.84B | `mit` | B | text |
| `Nanbeige/Nanbeige4-3B-Base` | llm | 3.93B | `apache-2.0` | B | text |
| `Nanbeige/Nanbeige4-3B-Thinking-2510` | llm | 3.93B | `apache-2.0` | B | text |
| `Nanbeige/Nanbeige4-3B-Thinking-2511` | llm | 3.93B | `apache-2.0` | B | text |
| `Nanbeige/Nanbeige4.1-3B` | llm | 3.93B | `apache-2.0` | B | text |
| `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | llm | 3.97B | `nvidia-nemotron-open-model-license` | C | text |
| `Qwen/Qwen3-4B` | llm | 4.02B | `apache-2.0` | B | text |
| `Qwen/Qwen3-4B-Instruct-2507` | llm | 4.02B | `apache-2.0` | B | text |
| `Qwen/Qwen3-4B-Thinking-2507` | llm | 4.02B | `apache-2.0` | B | text |
| `openbmb/AgentCPM-Explore` | llm | 4.022B | `apache-2.0` | B | text |
| `Nanbeige/Nanbeige4.2-3B` | llm | 4.17B | `apache-2.0` | B | text |
| `Nanbeige/Nanbeige4.2-3B-Base` | llm | 4.17B | `apache-2.0` | B | text |
| `OpenMOSS-Team/SciJudge-4B-2605` | llm | 4.41B | `apache-2.0` | B | text |
| `InternScience/Agents-A1-4B` | llm | 4.54B | `apache-2.0` | B | text |
| `FINAL-Bench/Aether-6B-11Attn-base` | llm | 5.79B | `apache-2.0` | B | text |
| `01-ai/Yi-1.5-6B-Chat` | llm | 6.06B | `apache-2.0` | B | text |
| `FINAL-Bench/AETHER-7B-7Attn-base` | llm | 6.59B | `apache-2.0` | B | text |
| `FINAL-Bench/Aether-7B-5Attn` | llm | 6.59B | `apache-2.0` | A | text |
| `FINAL-Bench/Aether-7B-5Attn-it` | llm | 6.59B | `apache-2.0` | A | text |
| `EleutherAI/pythia-6.9b` | llm | 6.86B | `apache-2.0` | A | text |
| `allenai/OLMoE-1B-7B-0924` | llm | 6.92B | `apache-2.0` | A | text |
| `bigscience/bloom-7b1` | llm | 7.07B | `bigscience-bloom-rail-1.0` | C | text |
| `mistralai/Mistral-7B-Instruct-v0.3` | llm | 7.24B | `apache-2.0` | B | text |
| `allenai/OLMo-2-1124-7B` | llm | 7.3B | `apache-2.0` | A | text |
| `allenai/OLMo-2-1124-7B-Instruct` | llm | 7.3B | `apache-2.0` | A | text |
| `tiiuae/Falcon3-7B-Instruct` | llm | 7.46B | `falcon-llm-license` | C | text |
| `Qwen/Qwen2.5-7B-Instruct` | llm | 7.61B | `apache-2.0` | B | text |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | llm | 7.62B | `mit` | B | text |
| `inclusionAI/Ling-3.0-tiny` | llm | 7.893B | `mit` | B | text |
| `LiquidAI/LFM2.5-8B-A1B` | llm | 8B | `lfm1.0` | C | text |
| `LiquidAI/LFM2.5-8B-A1B-Base` | llm | 8B | `lfm1.0` | C | text |
| `CohereForAI/c4ai-command-r7b-12-2024` | llm | 8.03B | `cc-by-nc-4.0` | D | text |
| `CohereLabs/aya-expanse-8b` | llm | 8.03B | `cc-by-nc-4.0` | D | text |
| `deepseek-ai/DeepSeek-R1-Distill-Llama-8B` | llm | 8.03B | `mit` | B | text |
| `ibm-granite/granite-3.3-8b-instruct` | llm | 8.17B | `apache-2.0` | B | text |
| `openbmb/AgentCPM-Report` | llm | 8.185B | `apache-2.0` | B | text |
| `Qwen/Qwen3-8B` | llm | 8.19B | `apache-2.0` | B | text |
| `openbmb/MiniCPM4-8B` | llm | 8.19B | `apache-2.0` | B | text |
| `openbmb/MiniCPM4.1-8B` | llm | 8.19B | `apache-2.0` | B | text |
| `Qwen/WebWorld-8B` | llm | 8.191B | `apache-2.0` | B | text |
| `01-ai/Yi-1.5-9B-Chat` | llm | 8.83B | `apache-2.0` | B | text |
| `nvidia/NVIDIA-Nemotron-Nano-9B-v2` | llm | 8.89B | `nvidia-open-model-license` | C | text |
| `google/gemma-2-9b-it` | llm | 9.24B | `gemma-terms-of-use` | C | text |
| `zai-org/GLM-4-9B-0414` | llm | 9.4B | `mit` | B | text |
| `zai-org/GLM-Z1-9B-0414` | llm | 9.4B | `mit` | B | text |
| `domyn/Domyn-Small-v1.0` | llm | 10B | `mit` | B | text |
| `tiiuae/Falcon3-10B-Instruct` | llm | 10.31B | `falcon-llm-license` | C | text |
| `ai-sage/GigaChat3-10B-A1.8B-base` | llm | 11.48B | `mit` | B | text |
| `ai-sage/GigaChat3.1-10B-A1.8B` | llm | 11.48B | `mit` | B | text |
| `EleutherAI/pythia-12b` | llm | 12B | `apache-2.0` | A | text |
| `microsoft/Florence-2-base` | ocr-vision | 0.23B | `mit` | B | image, text |
| `stepfun-ai/GOT-OCR2_0` | ocr-vision | 0.72B | `apache-2.0` | B | image, text |
| `ATH-MaaS/OvisOCR2` | ocr-vision | 0.85B | `apache-2.0` | B | image, text |
| `nvidia/NVIDIA-Nemotron-Parse-2.0` | ocr-vision | 0.903B | `nvidia-open-model-license` | C | image, text |
| `PaddlePaddle/PaddleOCR-VL` | ocr-vision | 0.96B | `apache-2.0` | B | image, text |
| `PaddlePaddle/PaddleOCR-VL-1.5` | ocr-vision | 0.96B | `apache-2.0` | B | image, text |
| `PaddlePaddle/PaddleOCR-VL-1.6` | ocr-vision | 0.96B | `apache-2.0` | B | image, text |
| `tencent/HunyuanOCR` | ocr-vision | 1.12B | `tencent-hunyuan-community` | C | image, text |
| `rednote-hilab/dots.ocr` | ocr-vision | 3.04B | `mit` | B | image, text |
| `deepseek-ai/DeepSeek-OCR` | ocr-vision | 3.34B | `mit` | B | image, text |
| `mistralai/Shieldstral-1.0-3B` | other | 3.849B | `apache-2.0` | B | text, image |
| `Nanbeige/CoSineVerifier-Tool-4B` | other | 4.41B | `mit` | B | text |
| `inclusionAI/SingGuard-NSFA-4B` | other | 5.17B | `apache-2.0` | B | text, image |
| `tencent/Hy-Embodied-RxBrain-1.0` | other | 6.21B | `apache-2.0` | B | text, image, video |
| `HuggingFaceTB/SmolVLM-256M-Instruct` | vlm | 0.26B | `apache-2.0` | B | text, image, video |
| `LiquidAI/LFM2.5-VL-450M` | vlm | 0.449B | `liquid-ai-open` | C | text, image |
| `HuggingFaceTB/SmolVLM-500M-Instruct` | vlm | 0.5B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3.5-0.8B` | vlm | 0.87B | `apache-2.0` | B | text, image, video |
| `OpenGVLab/InternVL3-1B` | vlm | 0.94B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3_5-1B` | vlm | 1.06B | `apache-2.0` | B | text, image |
| `openbmb/MiniCPM-V-4.6` | vlm | 1.3B | `apache-2.0` | B | text, image, video |
| `openbmb/MiniCPM-V-4.6-Thinking` | vlm | 1.3B | `apache-2.0` | B | text, image, video |
| `LiquidAI/LFM2.5-VL-1.6B` | vlm | 1.6B | `lfm1.0` | C | text, image |
| `microsoft/kosmos-2-patch14-224` | vlm | 1.66B | `mit` | B | text, image |
| `vikhyatk/moondream2` | vlm | 1.93B | `apache-2.0` | B | text, image |
| `OpenGVLab/InternVL3-2B` | vlm | 2.09B | `apache-2.0` | B | text, image |
| `Qwen/Qwen3-VL-2B-Instruct` | vlm | 2.13B | `apache-2.0` | B | text, image, video |
| `OpenGVLab/InternVL2-2B` | vlm | 2.21B | `mit` | B | text, image |
| `Qwen/Qwen2-VL-2B-Instruct` | vlm | 2.21B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3.5-2B` | vlm | 2.27B | `apache-2.0` | B | text, image, video |
| `OpenGVLab/InternVL3_5-2B` | vlm | 2.35B | `apache-2.0` | B | text, image |
| `CohereLabs/North-Micro-Vision-Instruct` | vlm | 2.485B | `apache-2.0` | B | text, image |
| `google/paligemma2-3b-pt-224` | vlm | 3.03B | `gemma-terms-of-use` | C | text, image |
| `LiquidAI/LFM2.5-VL-3B` | vlm | 3.123B | `lfm1.0` | C | text, image |
| `Qwen/Qwen2.5-VL-3B-Instruct` | vlm | 3.75B | `apache-2.0` | B | text, image, video |
| `OpenGVLab/InternVL2-4B` | vlm | 4.15B | `mit` | B | text, image |
| `microsoft/phi-3.5-vision-instruct` | vlm | 4.15B | `mit` | B | text, image |
| `mistralai/Ministral-3-3B-Base-2512` | vlm | 4.25B | `apache-2.0` | B | text, image |
| `mistralai/Ministral-3-3B-Instruct-2512-BF16` | vlm | 4.25B | `apache-2.0` | B | text, image |
| `mistralai/Ministral-3-3B-Reasoning-2512` | vlm | 4.25B | `apache-2.0` | B | text, image |
| `google/gemma-3-4b-it` | vlm | 4.3B | `gemma-terms-of-use` | C | text, image |
| `Qwen/Qwen3-VL-4B-Instruct` | vlm | 4.44B | `apache-2.0` | B | text, image, video |
| `microsoft/Fara1.5-4B` | vlm | 4.539B | `mit` | B | text, image |
| `inclusionAI/VISTA-4B` | vlm | 4.54B | `apache-2.0` | B | text, image |
| `Qwen/Qwen3.5-4B` | vlm | 4.66B | `apache-2.0` | B | text, image, video |
| `OpenGVLab/InternVL3_5-4B` | vlm | 4.73B | `apache-2.0` | B | text, image |
| `microsoft/Mage-VL` | vlm | 4.74B | `apache-2.0` | B | text, image, video |
| `google/gemma-4-E2B` | vlm | 5.12B | `apache-2.0` | B | text, image, audio |
| `microsoft/Phi-4-multimodal-instruct` | vlm | 5.57B | `mit` | B | text, image, audio |
| `OpenGVLab/InternVL3-8B` | vlm | 7.94B | `apache-2.0` | B | text, image |
| `google/gemma-4-E4B` | vlm | 8B | `apache-2.0` | B | text, image, audio |
| `allenai/Molmo-7B-D-0924` | vlm | 8.02B | `apache-2.0` | A | text, image |
| `OpenGVLab/InternVL2-8B` | vlm | 8.08B | `mit` | B | text, image |
| `Qwen/Qwen2-VL-7B-Instruct` | vlm | 8.29B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen2.5-VL-7B-Instruct` | vlm | 8.29B | `apache-2.0` | B | text, image, video |
| `microsoft/Fara-7B` | vlm | 8.29B | `mit` | B | text, image |
| `HuggingFaceM4/idefics2-8b` | vlm | 8.4B | `apache-2.0` | A | text, image |
| `OpenGVLab/InternVL3_5-8B` | vlm | 8.53B | `apache-2.0` | B | text, image |
| `allenai/Molmo2-8B` | vlm | 8.66B | `apache-2.0` | A | text, image, video |
| `openbmb/MiniCPM-V-4_5` | vlm | 8.7B | `apache-2.0` | B | text, image, video |
| `Qwen/Qwen3-VL-8B-Instruct` | vlm | 8.77B | `apache-2.0` | B | text, image, video |
| `mistralai/Ministral-3-8B-Base-2512` | vlm | 8.92B | `apache-2.0` | B | text, image |
| `mistralai/Ministral-3-8B-Instruct-2512-BF16` | vlm | 8.92B | `apache-2.0` | B | text, image |
| `mistralai/Ministral-3-8B-Reasoning-2512` | vlm | 8.92B | `apache-2.0` | B | text, image |
| `inclusionAI/VISTA-9B` | vlm | 9.41B | `apache-2.0` | B | text, image |
| `microsoft/Fara1.5-9B` | vlm | 9.41B | `mit` | B | text, image |
| `Qwen/Qwen3.5-9B` | vlm | 9.65B | `apache-2.0` | B | text, image, video |
| `google/paligemma2-10b-pt-224` | vlm | 9.66B | `gemma-terms-of-use` | C | text, image |
| `zai-org/GLM-4.1V-9B-Base` | vlm | 10.29B | `mit` | B | text, image |
| `zai-org/GLM-4.1V-9B-Thinking` | vlm | 10.29B | `mit` | B | text, image |
| `OpenMOSS-Team/MOSS-VL-Instruct-0708` | vlm | 11.34B | `apache-2.0` | B | text, image, video |
| `OpenMOSS-Team/MOSS-VL-Realtime` | vlm | 11.34B | `apache-2.0` | B | text, image, video |
<!-- END GENERATED MODEL TABLE -->
