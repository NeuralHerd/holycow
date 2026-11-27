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

    def test_fixture_is_committed_and_installed_skills_stay_out_of_git(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        self.assertEqual(workspace.git(folder, "log", "--format=%s").strip(), "Fixture")
        installed = workspace.install_skills(folder, ".claude/skills", self.skills, ["demo"])
        self.assertEqual(installed, ["demo"])
        self.assertTrue((folder / ".claude" / "skills" / "demo" / "SKILL.md").is_file())
        self.assertEqual(workspace.git(folder, "status", "--porcelain"), "")
        self.assertEqual(workspace.changed_files(folder), [])
        self.assertEqual(workspace.diff(folder), "")

    def test_changes_include_new_edited_and_deleted_files(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        (folder / "README.md").write_text("Hello there\n")
        (folder / "new.txt").write_text("new\n")
        (folder / "old.txt").unlink()
        self.assertEqual(workspace.changed_files(folder), ["README.md", "new.txt", "old.txt"])
        changes = workspace.diff(folder)
        self.assertIn("+Hello there", changes)
        self.assertIn("+new", changes)
        self.assertIn("-old", changes)

    def test_counts_commits_the_agent_adds(self):
        folder = workspace.create(self.fixture, parent=self.tmp)
        self.assertEqual(workspace.commits_added(folder), 0)
        (folder / "README.md").write_text("Changed\n")
        workspace.git(folder, "commit", "-qam", "Agent commit")
        self.assertEqual(workspace.commits_added(folder), 1)

    def test_missing_fixture_gives_an_empty_repository(self):
        folder = workspace.create(self.tmp / "absent", parent=self.tmp)
        self.assertEqual(workspace.commits_added(folder), 0)
        self.assertEqual(workspace.changed_files(folder), [])

    def test_skills_revision_outside_a_repository(self):
        self.assertEqual(workspace.skills_revision(self.tmp), {"commit": None, "dirty": None})


if __name__ == "__main__":
    unittest.main()
