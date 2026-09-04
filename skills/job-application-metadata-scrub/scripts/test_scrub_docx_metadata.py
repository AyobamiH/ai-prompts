#!/usr/bin/env python3
"""Standard-library regression tests for scrub_docx_metadata.py."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("scrub_docx_metadata.py")
SPEC = importlib.util.spec_from_file_location("scrub_docx_metadata", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


CONTENT_TYPES = b'''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Override PartName="/word/document.xml" ContentType="application/xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/xml"/>
  <Override PartName="/docProps/custom.xml" ContentType="application/xml"/>
  <Override PartName="/docProps/thumbnail.jpeg" ContentType="image/jpeg"/>
</Types>'''
ROOT_RELS = b'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="r1" Target="word/document.xml" Type="officeDocument"/>
  <Relationship Id="r2" Target="docProps/custom.xml" Type="custom-properties"/>
  <Relationship Id="r3" Target="docProps/thumbnail.jpeg" Type="thumbnail"/>
</Relationships>'''
CORE = b'''<?xml version="1.0" encoding="UTF-8"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>ChatGPT</dc:creator></cp:coreProperties>'''
APP = b'''<?xml version="1.0" encoding="UTF-8"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>python-docx</Application></Properties>'''
DOCUMENT = b'''<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"><w:body><w:p w:rsidR="00112233" w14:paraId="AABBCCDD"><w:r><w:t>Visible CV content</w:t></w:r></w:p></w:body></w:document>'''
DOCUMENT_RELS = b'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'''


def make_fixture(path: Path, tracked: bool = False) -> None:
    document = DOCUMENT
    if tracked:
        document = document.replace(
            b"<w:r><w:t>Visible CV content</w:t></w:r>",
            b"<w:ins w:author=\"Reviewer\"><w:r><w:t>Visible CV content</w:t></w:r></w:ins>",
        )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", CONTENT_TYPES)
        archive.writestr("_rels/.rels", ROOT_RELS)
        archive.writestr("docProps/core.xml", CORE)
        archive.writestr("docProps/app.xml", APP)
        archive.writestr("docProps/custom.xml", b"<Properties>OpenAI</Properties>")
        archive.writestr("docProps/thumbnail.jpeg", b"preview")
        archive.writestr("word/document.xml", document)
        archive.writestr("word/_rels/document.xml.rels", DOCUMENT_RELS)


class ScrubTests(unittest.TestCase):
    def test_scrubs_metadata_and_preserves_visible_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.docx"
            output = Path(directory) / "clean.docx"
            make_fixture(source)
            result = MODULE.run(source, output, False)
            self.assertTrue(result["content_preserved"])
            self.assertTrue(result["audit"]["clean"])
            with zipfile.ZipFile(output) as archive:
                self.assertNotIn("docProps/custom.xml", archive.namelist())
                self.assertNotIn("docProps/thumbnail.jpeg", archive.namelist())
                self.assertIn(b"Visible CV content", archive.read("word/document.xml"))

    def test_refuses_unresolved_tracked_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "tracked.docx"
            output = Path(directory) / "clean.docx"
            make_fixture(source, tracked=True)
            with self.assertRaises(MODULE.ScrubError):
                MODULE.run(source, output, False)


if __name__ == "__main__":
    unittest.main()
