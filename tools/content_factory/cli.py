"""Build publishable course content packs from structured Markdown modules."""

from __future__ import annotations

import argparse
import csv
import json
import re
from io import StringIO
from pathlib import Path
from typing import Any


SECTION_ALIASES = {
    "objectives": {"цели обучения", "learning objectives", "objectives"},
    "scenario": {"сценарий", "scenario"},
    "invariants": {"инварианты", "invariants"},
    "answers": {"эталонные тезисы", "reference answers", "answer theses"},
    "sources": {"источники", "sources"},
}

LEVELS = (
    ("L1", "recall", "Объясните своими словами: {objective}"),
    ("L2", "apply", "Как вы проверите через API: {objective}"),
    (
        "L3",
        "diagnose",
        "Какой дефект или пользовательский риск возникнет, если нарушено правило: {objective}",
    ),
    (
        "L4",
        "design",
        "Спроектируйте безопасное API-решение для цели: {objective}",
    ),
    (
        "L5",
        "production",
        "Production-инцидент нарушил цель «{objective}». Как локализовать причину, "
        "остановить ущерб и доказать исправление?",
    ),
)

STEPIK_DISTRACTORS = {
    "L1": (
        "Достаточно запомнить HTTP-код, не связывая его с бизнес-правилом.",
        "Это поведение полностью определяется клиентом и не требует серверной проверки.",
    ),
    "L2": (
        "Проверить только успешный HTTP-статус и не сравнивать состояние системы.",
        "Повторить запрос с новыми данными и считать любой ответ достаточным доказательством.",
    ),
    "L3": (
        "Считать тайм-аут доказательством того, что операция не выполнилась.",
        "Игнорировать идентификаторы операций, логи и итоговое состояние данных.",
    ),
    "L4": (
        "Добавить автоматический retry без стабильного ключа и без бизнес-инвариантов.",
        "Ограничить решение изменением текста ошибки в интерфейсе.",
    ),
    "L5": (
        "Перезапустить сервис и закрыть инцидент без проверки денежных последствий.",
        "Удалить спорные операции и не сохранять evidence для разбора и регрессии.",
    ),
}


def _normalise_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _canonical_section(heading: str) -> str:
    normalised = _normalise_heading(heading)
    for canonical, aliases in SECTION_ALIASES.items():
        if normalised in aliases:
            return canonical
    return normalised


def _extract_bullets(lines: list[str]) -> list[str]:
    return [line.strip()[2:].strip() for line in lines if line.strip().startswith("- ")]


def _slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]+", "-", value.strip().lower())
    return value.strip("-") or "module"


def parse_module(module_text: str, module_id: str = "module") -> dict[str, Any]:
    """Parse the small Markdown contract used by the content factory."""
    title = ""
    sections: dict[str, list[str]] = {}
    current_section = "preamble"
    sections[current_section] = []
    endpoint = ""

    for raw_line in module_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current_section = _canonical_section(line[3:])
            sections.setdefault(current_section, [])
            continue
        if line.lower().startswith(("endpoint:", "эндпоинт:")):
            endpoint = line.split(":", 1)[1].strip()
            continue
        sections.setdefault(current_section, []).append(line)

    if not title:
        raise ValueError("Module must contain a level-one Markdown title")

    objectives = _extract_bullets(sections.get("objectives", []))
    if not objectives:
        raise ValueError("Module must contain at least one learning objective")

    invariants = _extract_bullets(sections.get("invariants", []))
    answer_theses = _extract_bullets(sections.get("answers", []))
    sources = _extract_bullets(sections.get("sources", [])) or [module_id]
    scenario = "\n".join(
        line.strip() for line in sections.get("scenario", []) if line.strip()
    )

    return {
        "module_id": module_id,
        "title": title,
        "topic": title,
        "endpoint": endpoint or "Not specified",
        "objectives": objectives,
        "scenario": scenario or "Apply the module rules to the sandbox API.",
        "invariants": invariants,
        "answer_theses": answer_theses,
        "sources": sources,
    }


def _expected_answer(level: str, thesis: str, module: dict[str, Any]) -> str:
    invariant_text = "; ".join(module["invariants"]) or thesis

    if level == "L1":
        return thesis
    if level == "L2":
        return (
            f"Построить запросы к {module['endpoint']} и доказать результат через "
            f"ответ API и бизнес-инварианты. Эталонный тезис: {thesis}"
        )
    if level == "L3":
        return (
            "Связать наблюдаемый симптом с нарушенным инвариантом и риском для пользователя: "
            f"{invariant_text}"
        )
    if level == "L4":
        return (
            f"Определить контракт {module['endpoint']}, стабильные идентификаторы, политику retry, "
            f"переходы состояний, наблюдаемость и проверки инвариантов: {invariant_text}"
        )
    return (
        "Собрать timeline и evidence по request/operation IDs, ключам повторов, логам и состоянию "
        "данных; остановить дальнейший ущерб, выполнить reconciliation, установить корневую причину "
        f"и закрепить исправление регрессионными тестами. Контрольные инварианты: {invariant_text}"
    )


def _build_api_labs(module: dict[str, Any], module_id: str) -> list[dict[str, Any]]:
    criteria = module["invariants"] or [
        "Результат подтверждён ответом API и состоянием системы."
    ]
    common = {
        "endpoint": module["endpoint"],
        "scenario": module["scenario"],
        "acceptance_criteria": criteria,
        "source_refs": module["sources"],
    }
    return [
        {
            "id": f"{module_id.upper()}-LAB-001",
            "title": f"API-диагностика: {module['title']}",
            "level": "L3",
            "tasks": [
                "Зафиксируйте начальное состояние и ожидаемые бизнес-инварианты.",
                f"Выполните основной запрос к {module['endpoint']}.",
                "Смоделируйте повтор, ошибку или граничное условие из сценария.",
                "Сравните HTTP-ответ, идентификаторы операций и итоговое состояние данных.",
                "Оформите дефект, если хотя бы один инвариант нарушен.",
            ],
            **common,
        },
        {
            "id": f"{module_id.upper()}-LAB-L4-001",
            "title": f"Проектирование API-защиты: {module['title']}",
            "level": "L4",
            "tasks": [
                "Опишите контракт запроса, ответа и доменных ошибок.",
                "Спроектируйте стабильные идентификаторы, retry-policy и переходы состояний.",
                "Определите проверки конкурентных и повторных запросов.",
                "Добавьте логи, метрики и correlation fields для доказуемой диагностики.",
                "Сформулируйте автоматические тесты каждого бизнес-инварианта.",
            ],
            **common,
        },
        {
            "id": f"{module_id.upper()}-LAB-L5-001",
            "title": f"Production-инцидент: {module['title']}",
            "level": "L5",
            "tasks": [
                "Постройте timeline от первого запроса до обнаружения пользовательского ущерба.",
                "Соберите evidence: request IDs, operation IDs, ключи повторов, логи и состояние данных.",
                "Определите безопасные меры containment без уничтожения доказательств.",
                "Спроектируйте reconciliation и восстановление корректного состояния.",
                "Зафиксируйте root cause, regression test и наблюдаемость после исправления.",
            ],
            **common,
        },
    ]


def build_content_pack(module_text: str, module_id: str = "module") -> dict[str, Any]:
    """Create a versioned content pack with questions, labs, and answer keys."""
    module = parse_module(module_text, module_id=module_id)
    questions: list[dict[str, Any]] = []

    for objective_index, objective in enumerate(module["objectives"], start=1):
        thesis = (
            module["answer_theses"][objective_index - 1]
            if objective_index <= len(module["answer_theses"])
            else objective
        )
        for level, skill, template in LEVELS:
            question_id = f"{module_id.upper()}-{level}-{objective_index:03d}"
            questions.append(
                {
                    "id": question_id,
                    "level": level,
                    "skill": skill,
                    "topic": module["topic"],
                    "question": template.format(objective=objective),
                    "expected_answer": _expected_answer(level, thesis, module),
                    "source_refs": module["sources"],
                }
            )

    return {
        "schema_version": "0.1.0",
        "module": {
            "id": module["module_id"],
            "title": module["title"],
            "topic": module["topic"],
        },
        "questions": questions,
        "api_labs": _build_api_labs(module, module_id),
        "answers": [
            {
                "question_id": question["id"],
                "expected_answer": question["expected_answer"],
            }
            for question in questions
        ],
    }


def _question_bank_markdown(pack: dict[str, Any]) -> str:
    lines = [f"# Банк вопросов: {pack['module']['title']}", ""]
    for question in pack["questions"]:
        lines.extend(
            [
                f"## {question['id']} · {question['level']} · {question['skill']}",
                "",
                question["question"],
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _answer_key_markdown(pack: dict[str, Any]) -> str:
    by_id = {question["id"]: question for question in pack["questions"]}
    lines = [f"# Эталонные ответы: {pack['module']['title']}", ""]
    for answer in pack["answers"]:
        question = by_id[answer["question_id"]]
        lines.extend(
            [
                f"## {answer['question_id']}",
                "",
                f"**Вопрос:** {question['question']}",
                "",
                f"**Эталон:** {answer['expected_answer']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _api_lab_markdown(pack: dict[str, Any]) -> str:
    lines = [f"# API-практикумы: {pack['module']['title']}", ""]
    for lab in pack["api_labs"]:
        lines.extend(
            [
                f"## {lab['id']} · {lab['level']}",
                "",
                f"### {lab['title']}",
                "",
                f"**Endpoint:** `{lab['endpoint']}`",
                "",
                "### Сценарий",
                "",
                lab["scenario"],
                "",
                "### Задание",
                "",
            ]
        )
        lines.extend(
            f"{index}. {task}" for index, task in enumerate(lab["tasks"], start=1)
        )
        lines.extend(["", "### Критерии приёмки", ""])
        lines.extend(f"- {criterion}" for criterion in lab["acceptance_criteria"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _quiz_csv(pack: dict[str, Any]) -> str:
    stream = StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=["id", "level", "skill", "topic", "question", "expected_answer"],
    )
    writer.writeheader()
    for question in pack["questions"]:
        writer.writerow(
            {
                key: question[key]
                for key in (
                    "id",
                    "level",
                    "skill",
                    "topic",
                    "question",
                    "expected_answer",
                )
            }
        )
    return stream.getvalue()


def _stepik_csv(pack: dict[str, Any]) -> str:
    """Create Stepik's test-bank CSV: text/option rows with y/n correctness."""
    stream = StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    for question in pack["questions"]:
        writer.writerow(["text", question["question"], "-"])
        writer.writerow(["option", question["expected_answer"], "y"])
        for distractor in STEPIK_DISTRACTORS[question["level"]]:
            writer.writerow(["option", distractor, "n"])
    return stream.getvalue()


def export_content_pack(
    pack: dict[str, Any], output_dir: Path, formats: set[str] | None = None
) -> list[Path]:
    """Write selected publication formats and return the created paths."""
    selected = formats or {"json", "markdown", "csv", "stepik"}
    unknown = selected - {"json", "markdown", "csv", "stepik"}
    if unknown:
        raise ValueError(f"Unsupported formats: {', '.join(sorted(unknown))}")

    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    if "json" in selected:
        path = output_dir / "content-pack.json"
        path.write_text(
            json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        created.append(path)

    if "markdown" in selected:
        markdown_files = {
            "question-bank.md": _question_bank_markdown(pack),
            "api-lab.md": _api_lab_markdown(pack),
            "answer-key.md": _answer_key_markdown(pack),
        }
        for filename, content in markdown_files.items():
            path = output_dir / filename
            path.write_text(content, encoding="utf-8")
            created.append(path)

    if "csv" in selected:
        path = output_dir / "quiz.csv"
        path.write_text(_quiz_csv(pack), encoding="utf-8")
        created.append(path)

    if "stepik" in selected:
        path = output_dir / "stepik-question-bank.csv"
        path.write_text(_stepik_csv(pack), encoding="utf-8-sig")
        created.append(path)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, type=Path, help="Source Markdown module")
    parser.add_argument("--output", required=True, type=Path, help="Output directory")
    parser.add_argument(
        "--formats",
        default="json,markdown,csv,stepik",
        help="Comma-separated list: json,markdown,csv,stepik",
    )
    args = parser.parse_args()

    module_text = args.module.read_text(encoding="utf-8")
    module_id = _slugify(args.module.stem)
    pack = build_content_pack(module_text, module_id=module_id)
    formats = {item.strip() for item in args.formats.split(",") if item.strip()}
    created = export_content_pack(pack, args.output, formats=formats)

    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
