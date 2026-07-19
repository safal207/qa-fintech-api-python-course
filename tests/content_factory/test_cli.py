from __future__ import annotations

import json
from pathlib import Path

from jsonschema import validate

from tools.content_factory.cli import build_content_pack, export_content_pack


MODULE = """# Idempotency

Endpoint: POST /payments

## Learning objectives

- keep retries safe
- prevent duplicate payments

## Scenario

The first response times out after the payment is committed.

## Invariants

- one key maps to one payment
- the balance changes once

## Reference answers

- Reuse the original result for the same key.
- Verify operation count and final balance.

## Sources

- docs/COURSE_OUTLINE.md
"""


def test_build_content_pack_has_stable_levels_and_ids() -> None:
    pack = build_content_pack(MODULE, module_id="idempotency")

    assert pack["schema_version"] == "0.1.0"
    assert len(pack["questions"]) == 6
    assert {question["level"] for question in pack["questions"]} == {"L1", "L2", "L3"}
    assert pack["questions"][0]["id"] == "IDEMPOTENCY-L1-001"
    assert pack["api_labs"][0]["endpoint"] == "POST /payments"


def test_content_pack_matches_json_schema() -> None:
    pack = build_content_pack(MODULE, module_id="idempotency")
    schema_path = Path("schemas/content-pack.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    validate(instance=pack, schema=schema)


def test_export_content_pack_creates_publication_bundle(tmp_path: Path) -> None:
    pack = build_content_pack(MODULE, module_id="idempotency")

    created = export_content_pack(pack, tmp_path)

    assert {path.name for path in created} == {
        "content-pack.json",
        "question-bank.md",
        "api-lab.md",
        "answer-key.md",
        "quiz.csv",
    }
    assert "IDEMPOTENCY-L3-002" in (tmp_path / "question-bank.md").read_text(
        encoding="utf-8"
    )
    assert "expected_answer" in (tmp_path / "quiz.csv").read_text(encoding="utf-8")


def test_repository_idempotency_module_is_publishable(tmp_path: Path) -> None:
    module_path = Path("content/modules/idempotency.md")
    pack = build_content_pack(
        module_path.read_text(encoding="utf-8"), module_id="idempotency"
    )

    created = export_content_pack(pack, tmp_path)

    assert len(pack["questions"]) == 9
    assert len(pack["api_labs"][0]["acceptance_criteria"]) == 4
    assert len(created) == 5
