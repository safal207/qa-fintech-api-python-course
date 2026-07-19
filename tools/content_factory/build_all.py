"""Build publication bundles for every course module and write a manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from jsonschema import validate

from tools.content_factory.cli import _slugify, build_content_pack, export_content_pack

DEFAULT_FORMATS = {"json", "markdown", "csv", "stepik"}


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_pack_bytes(pack: dict[str, Any]) -> bytes:
    return json.dumps(
        pack,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _safe_recreate_output(output_dir: Path) -> None:
    resolved = output_dir.resolve()
    forbidden = {Path.cwd().resolve(), Path(resolved.anchor).resolve()}
    if resolved in forbidden:
        raise ValueError("Refusing to replace the repository root or filesystem root")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def _load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_course_content(
    modules_dir: Path,
    output_dir: Path,
    formats: set[str] | None = None,
    *,
    content_schema_path: Path = Path("schemas/content-pack.schema.json"),
    manifest_schema_path: Path = Path("schemas/course-content-manifest.schema.json"),
) -> dict[str, Any]:
    """Build all Markdown modules, validate them, and return the course manifest."""
    selected = formats or DEFAULT_FORMATS
    module_paths = sorted(path for path in modules_dir.rglob("*.md") if path.is_file())
    if not module_paths:
        raise ValueError(f"No Markdown modules found in {modules_dir}")

    content_schema = _load_schema(content_schema_path)
    manifest_schema = _load_schema(manifest_schema_path)
    _safe_recreate_output(output_dir)

    module_entries: list[dict[str, Any]] = []
    seen_module_ids: dict[str, Path] = {}
    for module_path in module_paths:
        relative_source = module_path.relative_to(modules_dir)
        module_key = relative_source.with_suffix("").as_posix().replace("/", "-")
        module_id = _slugify(module_key)
        previous_source = seen_module_ids.get(module_id)
        if previous_source is not None:
            raise ValueError(
                f"Module ID collision for '{module_id}': "
                f"{previous_source.as_posix()} and {relative_source.as_posix()}"
            )
        seen_module_ids[module_id] = relative_source

        source_bytes = module_path.read_bytes()
        module_text = source_bytes.decode("utf-8")
        pack = build_content_pack(module_text, module_id=module_id)
        validate(instance=pack, schema=content_schema)

        module_output = output_dir / module_id
        created = export_content_pack(pack, module_output, formats=selected)
        relative_files = sorted(path.relative_to(output_dir).as_posix() for path in created)
        status = pack["publication_readiness"]["status"]

        module_entries.append(
            {
                "id": module_id,
                "title": pack["module"]["title"],
                "source": relative_source.as_posix(),
                "output": module_id,
                "status": status,
                "source_sha256": _sha256_bytes(source_bytes),
                "content_pack_sha256": _sha256_bytes(_canonical_pack_bytes(pack)),
                "question_count": len(pack["questions"]),
                "api_lab_count": len(pack["api_labs"]),
                "files": relative_files,
            }
        )

    ready_count = sum(item["status"] == "READY" for item in module_entries)
    manifest = {
        "schema_version": "0.1.0",
        "status": "READY" if ready_count == len(module_entries) else "NOT_READY",
        "module_count": len(module_entries),
        "ready_count": ready_count,
        "not_ready_count": len(module_entries) - ready_count,
        "modules": module_entries,
    }
    validate(instance=manifest, schema=manifest_schema)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--modules-dir",
        type=Path,
        default=Path("content/modules"),
        help="Directory containing source Markdown modules",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("generated/course-content"),
        help="Directory for all publication bundles and manifest.json",
    )
    parser.add_argument(
        "--formats",
        default="json,markdown,csv,stepik",
        help="Comma-separated list: json,markdown,csv,stepik",
    )
    args = parser.parse_args()

    formats = {item.strip() for item in args.formats.split(",") if item.strip()}
    manifest = build_course_content(args.modules_dir, args.output, formats=formats)
    print(args.output / "manifest.json")
    print(
        f"modules={manifest['module_count']} ready={manifest['ready_count']} "
        f"status={manifest['status']}"
    )
    return 0 if manifest["status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
