# Next checkpoint: edge-deployment matrix

Status date: 2026-07-13  
Checkpoint owner: project maintainer  
Approval required before implementation continues: yes

## 1. Current state

The repository currently has:

- 92 curated model records under the strict `<12B total parameters` rule;
- categories for LLM, coding, VLM, OCR/vision, and audio/omni models;
- explicit openness grades (`A` through `U`);
- source URLs, license posture, total/active parameter fields, and model notes;
- Hugging Face candidate discovery that writes review-only candidates;
- live verification for model existence, parameter count, and license metadata;
- README generation, unit tests, and GitHub Actions validation.

The next checkpoint should make the registry useful for deployment decisions, not only model discovery.

## 2. Proposed objective

Build a generated **edge-deployment matrix** that answers:

> Which sub-12B models can I realistically run on a given device, runtime, and memory budget?

The first supported device targets should be:

1. Android phone — Xiaomi 11T Pro;
2. iPhone — iPhone 14 Pro Max;
3. Apple Silicon Mac;
4. Raspberry Pi / low-memory Linux device;
5. generic CPU-only laptop or desktop.

The first release should be conservative: estimated capability is allowed, but a model must not be marked “verified on device” without an actual reproducible test.

## 3. Implementation to-do

### Phase A — Extend the registry schema

- [ ] Add a `memory_estimates_gb` object for FP32, FP16, BF16, INT8, and INT4 weight-only estimates.
- [ ] Add a `runtime_support` object for Transformers, llama.cpp, MLX, ONNX, ExecuTorch, MLC, and other relevant runtimes.
- [ ] Add `hardware_readiness` fields for minimum recommended RAM, device tier, and estimated feasibility.
- [ ] Add explicit `vision_overhead` and `audio_overhead` notes for multimodal models.
- [ ] Add `verification` metadata: verification date, evidence URL, verification method, and verifier status.
- [ ] Update the JSON Schema and validator.

### Phase B — Generate deployment artifacts

- [ ] Generate `generated/models.json` for machine-readable consumers.
- [ ] Generate `generated/models.csv` for spreadsheet analysis.
- [ ] Generate `generated/hardware-matrix.md` with filters by device tier, category, license grade, and runtime.
- [ ] Add a CLI query such as:

  ```bash
  python3 scripts/query_models.py --device iphone-14-pro-max --max-memory 8
  ```

- [ ] Keep generated files deterministic and fail CI when they are stale.

### Phase C — Define the memory model

- [ ] Use transparent weight-only formulas based on total parameters and bytes per parameter.
- [ ] Add a clearly labeled runtime overhead band instead of pretending weight size equals total RAM usage.
- [ ] Separate language-only estimates from VLM/audio estimates.
- [ ] Add KV-cache warnings for long-context models.
- [ ] Add a boundary warning for models close to the 12B cutoff.
- [ ] Test the formulas against hand-calculated examples.

Initial estimate policy:

| Precision | Weight-only multiplier |
| --- | ---: |
| FP32 | 4 bytes/parameter |
| FP16/BF16 | 2 bytes/parameter |
| INT8 | 1 byte/parameter |
| INT4 | 0.5 bytes/parameter |

These are estimates only. Runtime overhead, tokenizer memory, KV cache, vision encoders, and audio encoders must remain separate fields.

### Phase D — Add real device verification

- [ ] Define a repeatable smoke-test prompt set for text, coding, image, OCR, and audio models.
- [ ] Record runtime, model format, quantization, prompt length, generation length, latency, peak memory, and result status.
- [ ] Add a `verified-on-device` record format without downloading weights in CI.
- [ ] Start with a small representative test set rather than attempting all 92 models.
- [ ] Document how contributors can submit device measurements.

Suggested first test set:

- one sub-1B text model;
- one 1–3B text model;
- one 7–9B text model;
- one small VLM;
- one OCR model;
- one coding model.

### Phase E — Improve the public README

- [ ] Add a “Best models by device” section generated from the matrix.
- [ ] Add separate views for permissive licenses, custom licenses, noncommercial models, and unverified licenses.
- [ ] Add “why this model is included” notes for representative families.
- [ ] Add a clear distinction between `open source`, `open weight`, `custom license`, and `noncommercial`.
- [ ] Add contribution instructions for new models and device benchmarks.

### Phase F — Quality gates and automation

- [ ] Add unit tests for memory calculations, filters, license views, and device tiers.
- [ ] Add schema validation for every generated artifact.
- [ ] Keep live Hugging Face verification scheduled, but do not make network access a requirement for local offline validation.
- [ ] Add a weekly candidate report that identifies new possible models without auto-promoting them.
- [ ] Track stale records whose `last_verified` date exceeds the chosen freshness window.

## 4. Approval decisions

Please approve or change these decisions before the next implementation pass:

### A. Scope

Recommended: proceed with the edge-deployment matrix for the five device targets above.

Alternative: focus only on expanding the model catalog further before adding deployment features.

### B. Model inclusion

Recommended: keep official base/instruct/reasoning/coding/VLM/OCR checkpoints in the primary registry, and include official packed/quantized artifacts in the separate deployment-variant catalog. Allow explicit `edge-exception` records above 12B only when official 16GB deployment evidence exists. Keep adapters, merges, and community fine-tunes out of both verified views.

### C. License treatment

Recommended: retain custom-license and noncommercial models in the catalog, but keep them visibly separated by openness grade and never label them simply “permissive open source.”

### D. Device verification

Recommended: begin with Xiaomi 11T Pro and iPhone 14 Pro Max, then add Mac and Raspberry Pi contributors after the measurement format is stable.

### E. Deliverable style

Recommended: keep the data source-first and generate Markdown, CSV, and JSON views from the registry rather than maintaining duplicate hand-edited tables.

## 5. Definition of done for this checkpoint

This checkpoint is complete when:

- the schema contains deployment and verification fields;
- all 92 existing records remain valid or have explicit migration notes;
- generated JSON, CSV, and Markdown artifacts are reproducible;
- a user can query models by device, memory budget, category, and license grade;
- at least six models have a documented first-pass deployment status;
- CI validates the source registry and generated artifacts;
- no model is marked device-verified without reproducible evidence.

## 6. Out of scope for this checkpoint

- building a universal benchmark leaderboard;
- automatically downloading or running every model;
- adding every Hugging Face derivative checkpoint;
- treating quantization as a reduction in parameter count;
- making legal claims beyond recording the published license and an explicit project classification;
- building a hosted web application before the generated data contract is stable.

## Approval response

Please review this file and respond with one of:

- `Approved` — proceed with the recommended scope;
- `Approved with changes` — list the sections or decisions to change;
- `Revise` — identify what should be reworked before implementation.
