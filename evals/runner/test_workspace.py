import os
import shutil
import tempfile
import unittest
from pathlib import Path

from runner import workspace


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.fixture = self.tmp / "fixture"
        self.fixture.mkdir()
        (self.fixture / "README.md").write_text("Hello\n")
        (self.fixture / "old.txt").write_text("old\n")
        self.skills = self.tmp / "skills"
        (self.skills / "demo").mkdir(parents=True)
        (self.skills / "demo" / "SKILL.md").write_text("---\nname: demo\n---\n")

    def test_fixture_is_committed_and_installed_skills_are_not_changes(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        self.assertEqual(workspace.git(folder, "log", "--format=%s").strip(), "Fixture")
        installed = workspace.install_skills(folder, ".claude/skills", self.skills, ["demo"])
        self.assertEqual(installed, ["demo"])
        self.assertTrue((folder / ".claude" / "skills" / "demo" / "SKILL.md").is_file())
        self.assertEqual(workspace.git(folder, "status", "--porcelain"), "")
        self.assertEqual(workspace.changes(self.fixture, folder, skip=[".claude/skills"]), ([], ""))

    def test_changes_include_new_edited_deleted_and_committed_files(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        (folder / "README.md").write_text("Hello there\n")
        (folder / "new.txt").write_text("new\n")
        (folder / "old.txt").unlink()
        workspace.git(folder, "add", "-A")
        workspace.git(folder, "commit", "-qm", "Agent commit")
        (folder / "__pycache__").mkdir()
        (folder / "__pycache__" / "x.pyc").write_bytes(b"\0")
        changed, diff = workspace.changes(self.fixture, folder)
        self.assertEqual(changed, ["README.md", "new.txt", "old.txt"])
        for line in ("-Hello", "+Hello there", "+++ b/new.txt", "+new", "--- a/old.txt", "-old"):
            self.assertIn(line + "\n", diff)
        self.assertEqual(workspace.commits_added(folder), 1)

    def test_symlinks_are_recorded_without_reading_their_target(self):
        secret = self.tmp / "secret.txt"
        secret.write_text("do not copy\n")
        folder = workspace.create(self.fixture, parent=self.tmp)
        os.symlink(secret, folder / "link.txt")
        os.symlink(self.tmp, folder / "link-dir")
        changed, diff = workspace.changes(self.fixture, folder)
        self.assertEqual(changed, ["link-dir", "link.txt"])
        self.assertNotIn("do not copy", diff)

    def test_commit_count_ignores_planted_git_commands(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        marker = self.tmp / "ran"
        hooks = folder / ".git" / "evil-hooks"
        hooks.mkdir()
        workspace.git(folder, "config", "core.fsmonitor", f"touch {marker}; false")
        workspace.git(folder, "config", "core.hooksPath", str(hooks))
        self.assertEqual(workspace.commits_added(folder), 0)
        workspace.changes(self.fixture, folder)
        self.assertFalse(marker.exists())

    def test_binary_files_are_summarized(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        (folder / "image.bin").write_bytes(b"\xff\xfe\x00")
        self.assertEqual(workspace.changes(self.fixture, folder)[1], "Binary files /dev/null and b/image.bin differ\n")

    def test_missing_fixture_gives_an_empty_repository(self):
        folder = workspace.create(self.tmp / "absent", parent=self.tmp)
        self.assertEqual(workspace.commits_added(folder), 0)
        self.assertEqual(workspace.changes(self.tmp / "absent", folder), ([], ""))

    def test_skills_revision_outside_a_repository(self):
        self.assertEqual(workspace.skills_revision(self.tmp), {"commit": None, "dirty": None})


if __name__ == "__main__":
    unittest.main()
