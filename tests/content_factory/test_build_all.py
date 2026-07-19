from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.content_factory.build_all import build_course_content


MODULE_TEMPLATE = """# {title}

Endpoint: POST /payments

## Learning objectives

- verify the module business rule

## Scenario

The client retries a request after a timeout.

## Invariants

- one accepted request changes the business state once

## Reference answers

- Prove the final business state, not only the HTTP status.

## Sources

- docs/COURSE_OUTLINE.md
"""


def _write_module(path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(MODULE_TEMPLATE.format(title=title), encoding="utf-8")


def test_build_course_content_generates_manifest_and_all_bundles(tmp_path: Path) -> None:
    modules_dir = tmp_path / "modules"
    output_dir = tmp_path / "generated"
    _write_module(modules_dir / "alpha.md", "Alpha")
    _write_module(modules_dir / "nested" / "beta.md", "Beta")

    manifest = build_course_content(modules_dir, output_dir)

    assert manifest["status"] == "READY"
    assert manifest["module_count"] == 2
    assert manifest["ready_count"] == 2
    assert manifest["not_ready_count"] == 0
    assert [item["id"] for item in manifest["modules"]] == ["alpha", "nested-beta"]

    for item in manifest["modules"]:
        assert item["question_count"] == 5
        assert item["api_lab_count"] == 3
        assert len(item["source_sha256"]) == 64
        assert len(item["content_pack_sha256"]) == 64
        assert len(item["files"]) == 10
        assert all((output_dir / relative_path).exists() for relative_path in item["files"])

    written_manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert written_manifest == manifest


def test_build_course_content_is_deterministic(tmp_path: Path) -> None:
    modules_dir = tmp_path / "modules"
    _write_module(modules_dir / "idempotency.md", "Idempotency")

    first = build_course_content(modules_dir, tmp_path / "first")
    second = build_course_content(modules_dir, tmp_path / "second")

    assert first == second


def test_build_course_content_rejects_empty_module_directory(tmp_path: Path) -> None:
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()

    with pytest.raises(ValueError, match="No Markdown modules found"):
        build_course_content(modules_dir, tmp_path / "generated")
