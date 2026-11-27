import json
import shutil
import tempfile
import unittest
from pathlib import Path

from runner.cases import CaseError, heading_anchor, list_cases, load_case


class ShippedCasesTests(unittest.TestCase):
    def test_every_shipped_case_loads(self):
        cases = list_cases()
        self.assertGreaterEqual(len(cases), 4)
        for case_id in cases:
            with self.subTest(case=case_id):
                load_case(case_id)

    def test_heading_anchor_matches_github(self):
        self.assertEqual(heading_anchor("Work complete, lifecycle still open"), "work-complete-lifecycle-still-open")
        self.assertEqual(heading_anchor("Dependencies, deferral, and resumed context"),
                         "dependencies-deferral-and-resumed-context")


class InvalidCaseTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / "skills" / "hc-build").mkdir(parents=True)
        (self.root / "skills" / "hc-build" / "SKILL.md").write_text("---\nname: hc-build\n---\n")
        (self.root / "evals").mkdir()
        (self.root / "evals" / "demo.md").write_text("# Demo\n\n## Small fix\n\nText.\n")
        self.cases = self.root / "evals" / "cases"

    def load(self, data, prompt="Fix it."):
        folder = self.cases / "group" / "case"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "case.json").write_text(json.dumps(data))
        if prompt is not None:
            (folder / "prompt.md").write_text(prompt)
        return load_case("group/case", cases_dir=self.cases, root=self.root)

    def valid(self, **changes):
        data = {
            "scenario": "evals/demo.md#small-fix",
            "steps": [{"prompt": "prompt.md", "invoke": "hc-build"}],
            "graders": [{"type": "skills_used", "skills": ["hc-build"]}],
        }
        data.update(changes)
        return data

    def assertRejected(self, data, message, prompt="Fix it."):
        with self.assertRaises(CaseError) as caught:
            self.load(data, prompt)
        self.assertIn(message, str(caught.exception))

    def test_valid_case_loads_prompt_and_defaults(self):
        case = self.load(self.valid())
        self.assertEqual(case.steps[0].prompt, "Fix it.")
        self.assertEqual(case.steps[0].invoke, "hc-build")
        self.assertEqual(case.timeout_seconds, 900)

    def test_rejects_unknown_scenario_heading(self):
        self.assertRejected(self.valid(scenario="evals/demo.md#missing"), "matches #missing")

    def test_rejects_unknown_skill(self):
        self.assertRejected(self.valid(steps=[{"prompt": "prompt.md", "invoke": "hc-nope"}]), "unknown skill")
        self.assertRejected(self.valid(graders=[{"type": "skills_used", "skills": ["hc-nope"]}]), "known skill")

    def test_rejects_missing_or_flag_like_prompt(self):
        self.assertRejected(self.valid(), "missing or empty", prompt=None)
        self.assertRejected(self.valid(), "must not start with '-'", prompt="--help")

    def test_rejects_bad_graders(self):
        self.assertRejected(self.valid(graders=[{"type": "vibes"}]), "type must be one of")
        self.assertRejected(self.valid(graders=[{"type": "diff_matches", "patterns": ["("]}]), "bad pattern")
        self.assertRejected(self.valid(graders=[{"type": "judge"}]), "missing ['rubric']")
        self.assertRejected(self.valid(graders=[{"type": "judge", "rubric": "x", "step": 2}]), "step must be")
        self.assertRejected(self.valid(graders=[{"type": "judge", "rubric": "x", "arms": ["maybe"]}]), "arms")
        self.assertRejected(self.valid(graders=[{"type": "judge", "rubric": "x", "extra": 1}]), "unknown keys")

    def test_rejects_unknown_case_keys(self):
        self.assertRejected(self.valid(notes="x"), "unknown keys")


if __name__ == "__main__":
    unittest.main()
