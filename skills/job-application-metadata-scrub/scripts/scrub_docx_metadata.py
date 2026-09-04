#!/usr/bin/env python3
"""Audit and scrub hidden authoring metadata from a job-application DOCX.

The script preserves visible document text and relationships. It refuses files
with comments or tracked changes because silently removing those artifacts may
change the applicant's intended final content.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from copy import copy
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

NORMALIZED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
AI_MARKERS = (
    "openai",
    "chatgpt",
    "codex",
    "anthropic",
    "claude",
    "gemini",
    "python-docx",
    "libreoffice",
    "ai-generated",
    "ai generated",
)
REVIEW_PART_PATTERNS = (
    re.compile(r"^word/comments(?:Extended|Ids)?\.xml$", re.I),
    re.compile(r"^word/people\.xml$", re.I),
)
TRACKED_TAGS = {
    f"{{{W_NS}}}ins",
    f"{{{W_NS}}}del",
    f"{{{W_NS}}}moveFrom",
    f"{{{W_NS}}}moveTo",
}


class ScrubError(RuntimeError):
    """A safe, actionable scrub failure."""


@dataclass
class Audit:
    valid_docx: bool
    core_property_values: int
    extended_property_values: int
    custom_properties_present: bool
    preview_thumbnail_present: bool
    review_parts: list[str]
    tracked_change_elements: int
    revision_identifiers: int
    ai_markers_in_metadata: list[str]
    zip_timestamps_normalized: bool
    story_text_sha256: str
    document_relationships_sha256: str
    clean: bool


def parse_xml(data: bytes, part: str) -> ET.Element:
    try:
        for _, (prefix, uri) in ET.iterparse(io.BytesIO(data), events=("start-ns",)):
            try:
                ET.register_namespace(prefix or "", uri)
            except ValueError:
                pass
        return ET.fromstring(data)
    except ET.ParseError as exc:
        raise ScrubError(f"Malformed XML in {part}: {exc}") from exc


def serialize_xml(root: ET.Element, original: bytes) -> bytes:
    """Serialize without dropping namespace declarations used by mc:Ignorable."""
    data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    declarations = re.findall(
        rb"xmlns(?::([A-Za-z_][\w.-]*))?=[\"']([^\"']+)[\"']", original
    )
    missing = []
    for raw_prefix, uri in declarations:
        prefix = raw_prefix.decode("ascii") if raw_prefix else ""
        needle = f"xmlns:{prefix}=".encode("ascii") if prefix else b"xmlns="
        if needle not in data:
            label = f"xmlns:{prefix}" if prefix else "xmlns"
            missing.append(f' {label}="{uri.decode("utf-8")}"'.encode("utf-8"))
    if missing:
        declaration_end = data.find(b"?>")
        root_start = data.find(b"<", declaration_end + 2 if declaration_end >= 0 else 0)
        root_end = data.find(b">", root_start)
        insert_at = root_end - 1 if data[root_end - 1 : root_end] == b"/" else root_end
        data = data[:insert_at] + b"".join(missing) + data[insert_at:]
    return data


def validate_package(names: set[str]) -> None:
    required = {"[Content_Types].xml", "_rels/.rels", "word/document.xml"}
    missing = sorted(required - names)
    if missing:
        raise ScrubError(f"Not a usable DOCX package; missing: {', '.join(missing)}")
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise ScrubError(f"Unsafe package path: {name}")


def meaningful_children(data: bytes, part: str) -> int:
    root = parse_xml(data, part)
    count = 0
    for child in root:
        if (child.text or "").strip() or child.attrib or list(child):
            count += 1
    return count


def story_text_signature(parts: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    story = re.compile(r"^word/(document|header\d+|footer\d+|footnotes|endnotes)\.xml$")
    for name in sorted(part for part in parts if story.match(part)):
        root = parse_xml(parts[name], name)
        digest.update(name.encode("utf-8"))
        for element in root.iter():
            if element.tag in {f"{{{W_NS}}}t", f"{{{W_NS}}}instrText"}:
                digest.update((element.text or "").encode("utf-8"))
                digest.update(b"\0")
    return digest.hexdigest()


def relationships_signature(parts: dict[str, bytes]) -> str:
    data = parts.get("word/_rels/document.xml.rels", b"")
    return hashlib.sha256(data).hexdigest()


def revision_identifier_count(parts: dict[str, bytes]) -> int:
    count = 0
    for name, data in parts.items():
        if not name.startswith("word/") or not name.endswith(".xml"):
            continue
        root = parse_xml(data, name)
        for element in root.iter():
            if element.tag.startswith(f"{{{W_NS}}}") and element.tag.split("}", 1)[1].startswith("rsid"):
                count += 1
            for attr in element.attrib:
                if attr.startswith(f"{{{W_NS}}}rsid") or attr in {
                    f"{{{W14_NS}}}paraId",
                    f"{{{W14_NS}}}textId",
                }:
                    count += 1
    return count


def tracked_change_count(parts: dict[str, bytes]) -> int:
    count = 0
    for name, data in parts.items():
        if not name.startswith("word/") or not name.endswith(".xml"):
            continue
        root = parse_xml(data, name)
        count += sum(1 for element in root.iter() if element.tag in TRACKED_TAGS)
    return count


def metadata_markers(parts: dict[str, bytes]) -> list[str]:
    surfaces = []
    for name in parts:
        if name.startswith("docProps/") or name.startswith("customXml/"):
            surfaces.append(name)
        elif any(pattern.match(name) for pattern in REVIEW_PART_PATTERNS):
            surfaces.append(name)
    haystack = b"\n".join(parts[name] for name in sorted(surfaces)).decode(
        "utf-8", errors="ignore"
    ).lower()
    return sorted(marker for marker in AI_MARKERS if marker in haystack)


def audit_parts(parts: dict[str, bytes], timestamps: list[tuple[int, ...]]) -> Audit:
    names = set(parts)
    validate_package(names)
    review_parts = sorted(
        name for name in names if any(pattern.match(name) for pattern in REVIEW_PART_PATTERNS)
    )
    core_values = (
        meaningful_children(parts["docProps/core.xml"], "docProps/core.xml")
        if "docProps/core.xml" in parts
        else 0
    )
    app_values = (
        meaningful_children(parts["docProps/app.xml"], "docProps/app.xml")
        if "docProps/app.xml" in parts
        else 0
    )
    tracked = tracked_change_count(parts)
    revision_ids = revision_identifier_count(parts)
    markers = metadata_markers(parts)
    timestamps_normalized = all(tuple(value) == NORMALIZED_ZIP_TIME for value in timestamps)
    custom_properties = "docProps/custom.xml" in names
    thumbnail = "docProps/thumbnail.jpeg" in names or "docProps/thumbnail.png" in names
    clean = not any(
        (
            core_values,
            app_values,
            custom_properties,
            thumbnail,
            review_parts,
            tracked,
            revision_ids,
            markers,
            not timestamps_normalized,
        )
    )
    return Audit(
        valid_docx=True,
        core_property_values=core_values,
        extended_property_values=app_values,
        custom_properties_present=custom_properties,
        preview_thumbnail_present=thumbnail,
        review_parts=review_parts,
        tracked_change_elements=tracked,
        revision_identifiers=revision_ids,
        ai_markers_in_metadata=markers,
        zip_timestamps_normalized=timestamps_normalized,
        story_text_sha256=story_text_signature(parts),
        document_relationships_sha256=relationships_signature(parts),
        clean=clean,
    )


def read_docx(path: Path) -> tuple[dict[str, bytes], dict[str, zipfile.ZipInfo]]:
    if not path.is_file():
        raise ScrubError(f"Input file does not exist: {path}")
    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = {info.filename: copy(info) for info in archive.infolist() if not info.is_dir()}
            parts = {name: archive.read(name) for name in infos}
    except (zipfile.BadZipFile, OSError) as exc:
        raise ScrubError(f"Cannot read DOCX package: {exc}") from exc
    validate_package(set(parts))
    return parts, infos


def empty_xml_root(data: bytes, part: str) -> bytes:
    root = parse_xml(data, part)
    for child in list(root):
        root.remove(child)
    return serialize_xml(root, data)


def remove_package_targets(data: bytes, part: str, targets: set[str]) -> bytes:
    root = parse_xml(data, part)
    for rel in list(root):
        target = (rel.attrib.get("Target") or "").replace("\\", "/")
        if any(target.endswith(value) for value in targets):
            root.remove(rel)
    return serialize_xml(root, data)


def remove_content_type_overrides(data: bytes, removed_parts: set[str]) -> bytes:
    root = parse_xml(data, "[Content_Types].xml")
    for child in list(root):
        if child.tag == f"{{{CT_NS}}}Override":
            part_name = (child.attrib.get("PartName") or "").lstrip("/")
            if part_name in removed_parts:
                root.remove(child)
    return serialize_xml(root, data)


def strip_revision_identifiers(data: bytes, part: str) -> bytes:
    root = parse_xml(data, part)
    changed = False
    for parent in root.iter():
        for child in list(parent):
            if child.tag.startswith(f"{{{W_NS}}}") and child.tag.split("}", 1)[1].startswith("rsid"):
                parent.remove(child)
                changed = True
    for element in root.iter():
        for attr in list(element.attrib):
            if attr.startswith(f"{{{W_NS}}}rsid") or attr in {
                f"{{{W14_NS}}}paraId",
                f"{{{W14_NS}}}textId",
            }:
                del element.attrib[attr]
                changed = True
    if not changed:
        return data
    return serialize_xml(root, data)


def scrub_parts(parts: dict[str, bytes]) -> tuple[dict[str, bytes], dict[str, int]]:
    before = audit_parts(parts, [NORMALIZED_ZIP_TIME] * len(parts))
    if before.review_parts or before.tracked_change_elements:
        details = []
        if before.review_parts:
            details.append("review parts: " + ", ".join(before.review_parts))
        if before.tracked_change_elements:
            details.append(f"tracked changes: {before.tracked_change_elements}")
        raise ScrubError(
            "Refusing to scrub a document with unresolved review artifacts ("
            + "; ".join(details)
            + "). Finalise comments and revisions explicitly first."
        )

    cleaned = dict(parts)
    stats = {
        "core_properties_cleared": 0,
        "extended_properties_cleared": 0,
        "custom_property_parts_removed": 0,
        "preview_parts_removed": 0,
        "revision_identifiers_removed": before.revision_identifiers,
    }

    if "docProps/core.xml" in cleaned:
        cleaned["docProps/core.xml"] = empty_xml_root(
            cleaned["docProps/core.xml"], "docProps/core.xml"
        )
        stats["core_properties_cleared"] = before.core_property_values
    if "docProps/app.xml" in cleaned:
        cleaned["docProps/app.xml"] = empty_xml_root(
            cleaned["docProps/app.xml"], "docProps/app.xml"
        )
        stats["extended_properties_cleared"] = before.extended_property_values

    removed = {
        name
        for name in cleaned
        if name == "docProps/custom.xml"
        or name in {"docProps/thumbnail.jpeg", "docProps/thumbnail.png"}
    }
    for name in removed:
        del cleaned[name]
    stats["custom_property_parts_removed"] = int("docProps/custom.xml" in removed)
    stats["preview_parts_removed"] = sum(name.startswith("docProps/thumbnail") for name in removed)

    if "_rels/.rels" in cleaned:
        cleaned["_rels/.rels"] = remove_package_targets(
            cleaned["_rels/.rels"],
            "_rels/.rels",
            {"docProps/custom.xml", "docProps/thumbnail.jpeg", "docProps/thumbnail.png"},
        )
    cleaned["[Content_Types].xml"] = remove_content_type_overrides(
        cleaned["[Content_Types].xml"], removed
    )

    for name in list(cleaned):
        if name.startswith("word/") and name.endswith(".xml"):
            cleaned[name] = strip_revision_identifiers(cleaned[name], name)
    return cleaned, stats


def write_docx(
    path: Path, parts: dict[str, bytes], infos: dict[str, zipfile.ZipInfo]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(parts):
                old = infos.get(name)
                info = zipfile.ZipInfo(filename=name, date_time=NORMALIZED_ZIP_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                if old is not None:
                    info.external_attr = old.external_attr
                    info.create_system = old.create_system
                archive.writestr(info, parts[name])
    except OSError as exc:
        raise ScrubError(f"Cannot write cleaned DOCX: {exc}") from exc


def run(input_path: Path, output_path: Path | None, audit_only: bool) -> dict[str, object]:
    parts, infos = read_docx(input_path)
    input_audit = audit_parts(parts, [info.date_time for info in infos.values()])
    if audit_only:
        return {"path": str(input_path), "audit": asdict(input_audit)}
    if output_path is None:
        raise ScrubError("--out is required unless --audit is used")
    if input_path.resolve() == output_path.resolve():
        raise ScrubError("Input and output must be different files")

    cleaned, stats = scrub_parts(parts)
    write_docx(output_path, cleaned, infos)
    output_parts, output_infos = read_docx(output_path)
    output_audit = audit_parts(
        output_parts, [info.date_time for info in output_infos.values()]
    )
    content_preserved = (
        input_audit.story_text_sha256 == output_audit.story_text_sha256
        and input_audit.document_relationships_sha256
        == output_audit.document_relationships_sha256
    )
    if not output_audit.clean or not content_preserved:
        raise ScrubError(
            "Post-scrub verification failed; do not submit the generated file"
        )
    return {
        "input": str(input_path),
        "output": str(output_path),
        "removed": stats,
        "content_preserved": content_preserved,
        "audit": asdict(output_audit),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--audit", action="store_true")
    mode.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.input, args.out, args.audit)
    except ScrubError as exc:
        print(json.dumps({"clean": False, "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
