from __future__ import annotations

import csv
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
    assert len(pack["questions"]) == 10
    assert {question["level"] for question in pack["questions"]} == {
        "L1",
        "L2",
        "L3",
        "L4",
        "L5",
    }
    assert pack["questions"][0]["id"] == "IDEMPOTENCY-L1-001"
    assert pack["questions"][4]["id"] == "IDEMPOTENCY-L5-001"
    assert [lab["level"] for lab in pack["api_labs"]] == ["L3", "L4", "L5"]
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
        "stepik-question-bank.csv",
    }
    assert "IDEMPOTENCY-L5-002" in (tmp_path / "question-bank.md").read_text(
        encoding="utf-8"
    )
    assert "IDEMPOTENCY-LAB-L5-001" in (tmp_path / "api-lab.md").read_text(
        encoding="utf-8"
    )
    assert "expected_answer" in (tmp_path / "quiz.csv").read_text(encoding="utf-8")


def test_stepik_export_uses_text_and_option_rows(tmp_path: Path) -> None:
    pack = build_content_pack(MODULE, module_id="idempotency")
    export_content_pack(pack, tmp_path, formats={"stepik"})

    with (tmp_path / "stepik-question-bank.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        rows = list(csv.reader(stream))

    assert len(rows) == len(pack["questions"]) * 4
    assert rows[0] == ["text", pack["questions"][0]["question"], "-"]
    assert rows[1] == ["option", pack["questions"][0]["expected_answer"], "y"]
    assert rows[2][0] == "option"
    assert rows[2][2] == "n"


def test_repository_idempotency_module_is_publishable(tmp_path: Path) -> None:
    module_path = Path("content/modules/idempotency.md")
    pack = build_content_pack(
        module_path.read_text(encoding="utf-8"), module_id="idempotency"
    )

    created = export_content_pack(pack, tmp_path)

    assert len(pack["questions"]) == 15
    assert len(pack["api_labs"]) == 3
    assert len(pack["api_labs"][0]["acceptance_criteria"]) == 4
    assert len(created) == 6
