# Course Content Factory v0.1

`tools/content_factory` turns one structured Markdown module into a small publication bundle:

- `content-pack.json` — canonical machine-readable package;
- `question-bank.md` — questions grouped by stable IDs and levels;
- `api-lab.md` — scenario, tasks, and acceptance criteria;
- `answer-key.md` — reference answers;
- `quiz.csv` — tabular export for further publication/import.

## Source module contract

A module must contain:

```markdown
# Module title

Endpoint: POST /payments

## Learning objectives

- objective one
- objective two

## Scenario

A realistic API or production situation.

## Invariants

- business rule that must remain true

## Reference answers

- thesis corresponding to objective one
- thesis corresponding to objective two

## Sources

- docs/COURSE_OUTLINE.md
```

Russian headings are supported as well: `Цели обучения`, `Сценарий`, `Инварианты`, `Эталонные тезисы`, and `Источники`.

## Generate a bundle

```bash
python -m tools.content_factory.cli \
  --module content/modules/idempotency.md \
  --output generated/idempotency \
  --formats json,markdown,csv
```

## Validate

```bash
python -m pytest tests/content_factory
```

The generated JSON package is validated in tests against `schemas/content-pack.schema.json`.

## Scope of v0.1

The first version is intentionally deterministic. It does not call an LLM and does not invent factual material outside the source module. Later versions may add evidence-grounded AI generation behind the same schema and tests.
