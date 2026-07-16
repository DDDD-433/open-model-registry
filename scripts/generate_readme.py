#!/usr/bin/env python3
"""Generate the catalog table inserted into README.md."""

from __future__ import annotations

import re
from pathlib import Path

from registry import ROOT, load_registry


START = "<!-- BEGIN GENERATED MODEL TABLE -->"
END = "<!-- END GENERATED MODEL TABLE -->"


def render_table(models: list[dict]) -> str:
    rows = [
        START,
        "| Model | Category | Parameters | License | Grade | Modalities |",
        "| --- | --- | ---: | --- | :---: | --- |",
    ]
    for model in sorted(models, key=lambda item: (item["category"], item["parameters"]["total_b"], item["model_id"])):
        params = model["parameters"]
        modalities = ", ".join(model["modalities"]["inputs"])
        rows.append(
            f"| `{model['model_id']}` | {model['category']} | {params['total_b']:g}B | "
            f"`{model['openness']['license']}` | {model['openness']['grade']} | {modalities} |"
        )
    rows.append(END)
    return "\n".join(rows)


def update_readme(readme: Path = ROOT / "README.md") -> None:
    content = readme.read_text(encoding="utf-8")
    table = render_table(load_registry()["models"])
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(table, content)
    else:
        content += "\n\n## Catalog\n\n" + table + "\n"
    readme.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print("README catalog table generated")
