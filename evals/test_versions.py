"""VERSION, every skill's metadata.version and CHANGELOG.md must agree."""

import importlib.util
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


set_version = load("set_version")
changelog_section = load("changelog_section")


def frontmatter_version(skill_file: Path):
    text = skill_file.read_text()
    front = text[4:text.index("\n---\n", 4)]
    match = re.search(r'^metadata:\n(?:  .*\n)*?  version: "([^"]+)"$', front + "\n", re.M)
    return match.group(1) if match else None


class VersionTests(unittest.TestCase):
    def test_version_is_semantic(self):
        self.assertRegex((ROOT / "VERSION").read_text(), r"^\d+\.\d+\.\d+\n$")

    def test_every_skill_carries_the_version(self):
        version = (ROOT / "VERSION").read_text().strip()
        skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                self.assertEqual(frontmatter_version(skill), version)

    def test_changelog_has_the_version_and_an_unreleased_section(self):
        text = (ROOT / "CHANGELOG.md").read_text()
        version = (ROOT / "VERSION").read_text().strip()
        self.assertIn("## [Unreleased]", text)
        self.assertTrue(changelog_section.section(version, text).strip())
        self.assertIn(f"[{version}]: https://github.com/NeuralHerd/holycow/releases/tag/v{version}", text)


class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        shutil.copytree(ROOT / "skills", self.root / "skills")

    def test_set_version_updates_version_and_every_skill(self):
        changed = set_version.set_version("2.3.4", root=self.root)
        self.assertEqual(len(changed), 10)
        self.assertEqual((self.root / "VERSION").read_text(), "2.3.4\n")
        for skill in (self.root / "skills").glob("*/SKILL.md"):
            self.assertEqual(frontmatter_version(skill), "2.3.4")
        self.assertEqual((self.root / "skills" / "hc-build" / "SKILL.md").read_text().count("2.3.4"), 1)

    def test_set_version_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            set_version.set_version("v1.0", root=self.root)
        skill = self.root / "skills" / "hc-lab" / "SKILL.md"
        skill.write_text(skill.read_text().replace('  version: "', '  release: "'))
        with self.assertRaises(ValueError):
            set_version.set_version("1.0.0", root=self.root)

    def test_changelog_section(self):
        text = "## [Unreleased]\n\n## [1.1.0] - 2026-01-02\n\n- New.\n\n## [1.0.0] - 2026-01-01\n\n- Old.\n\n[1.1.0]: x\n"
        self.assertEqual(changelog_section.section("1.1.0", text), "- New.\n")
        self.assertEqual(changelog_section.section("1.0.0", text), "- Old.\n")
        with self.assertRaises(LookupError):
            changelog_section.section("Unreleased", text)
        with self.assertRaises(LookupError):
            changelog_section.section("9.9.9", text)


if __name__ == "__main__":
    unittest.main()
