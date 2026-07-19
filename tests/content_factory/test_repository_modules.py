from __future__ import annotations

from pathlib import Path

from tools.content_factory.build_all import build_course_content
from tools.content_factory.cli import build_content_pack, export_content_pack


def test_balances_fees_rounding_module_is_publishable(tmp_path: Path) -> None:
    module_path = Path("content/modules/balances-fees-rounding.md")
    pack = build_content_pack(
        module_path.read_text(encoding="utf-8"),
        module_id="balances-fees-rounding",
    )

    created = export_content_pack(pack, tmp_path)

    assert pack["module"]["title"] == "Балансы, комиссии и округления в переводах"
    assert len(pack["questions"]) == 15
    assert [lab["level"] for lab in pack["api_labs"]] == ["L3", "L4", "L5"]
    assert all(lab["endpoint"] == "POST /transfer" for lab in pack["api_labs"])
    assert len(pack["api_labs"][0]["acceptance_criteria"]) == 5
    assert pack["rubric"]["total_points"] == 100
    assert pack["publication_readiness"]["status"] == "READY"
    assert "src/finpay_sandbox/domain.py#calculate_fee" in pack["questions"][0][
        "source_refs"
    ]
    assert len(created) == 10


def test_repository_course_build_contains_two_ready_modules(tmp_path: Path) -> None:
    manifest = build_course_content(
        Path("content/modules"),
        tmp_path / "course-content",
    )

    assert manifest["status"] == "READY"
    assert manifest["module_count"] == 2
    assert manifest["ready_count"] == 2
    assert manifest["not_ready_count"] == 0
    assert [item["id"] for item in manifest["modules"]] == [
        "balances-fees-rounding",
        "idempotency",
    ]
    assert sum(item["question_count"] for item in manifest["modules"]) == 30
    assert sum(item["api_lab_count"] for item in manifest["modules"]) == 6
    assert all(len(item["files"]) == 10 for item in manifest["modules"])
