"""Run with: python3 -m unittest discover -s evals -p 'test_init_banner.py'."""

import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills/holycow-init/scripts/banner.py"
SPEC = importlib.util.spec_from_file_location("init_banner", SCRIPT)
banner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(banner)
SGR = re.compile(r"\033\[[0-9;]*m")


class InitBannerTests(unittest.TestCase):
    def test_captured_output_stays_plain_even_with_color_environment(self):
        env = {"TERM": "xterm-256color", "COLORTERM": "truecolor"}
        self.assertEqual(banner.color_mode("auto", env, False), "never")
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=ROOT.parent,
            env={**os.environ, **env}, capture_output=True, check=True,
        )
        self.assertNotIn(b"\x1b", result.stdout)
        self.assertIn(b"HOLYCOW", result.stdout)

    def test_terminal_capabilities_and_no_color(self):
        for env, expected in (
            ({"TERM": "dumb", "COLORTERM": "truecolor"}, "never"),
            ({}, "never"),
            ({"TERM": "xterm", "NO_COLOR": "1"}, "never"),
            ({"TERM": "xterm"}, "16"),
            ({"TERM": "xterm-256color"}, "256"),
            ({"TERM": "xterm", "COLORTERM": "truecolor"}, "truecolor"),
            ({"TERM": "xterm-direct"}, "truecolor"),
        ):
            with self.subTest(env=env):
                self.assertEqual(banner.color_mode("auto", env, True), expected)
        self.assertEqual(banner.color_mode("truecolor", {"NO_COLOR": "1"}, False), "truecolor")

    def test_all_sizes_and_color_modes_preserve_visible_geometry(self):
        for width in (1, 2, 7, 13, 20, 24, 40, 60, 80, 100):
            plain = banner.render(width, "never")
            for mode in ("truecolor", "256", "16", "never"):
                with self.subTest(width=width, mode=mode):
                    output = banner.render(width, mode)
                    visible = SGR.sub("", output)
                    self.assertEqual(visible, plain)
                    self.assertLessEqual(max(map(len, visible.splitlines())), width)
                    self.assertNotIn("\x1b", visible)
                    self.assertTrue(visible.isascii())

    def test_color_does_not_leak_into_following_shell_output(self):
        for mode in ("truecolor", "256", "16"):
            output = banner.render(100, mode)
            self.assertIn("\x1b[", output)
            for line in output.splitlines():
                if "\x1b" in line:
                    self.assertEqual(SGR.findall(line)[-1], banner.RESET)
            self.assertNotRegex(SGR.sub("", output), r"[\x00-\x08\x0b-\x1f\x7f]")

    def test_explicit_color_and_quiet_work_when_invoked_from_another_directory(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--color", "truecolor", "--width", "100"],
            cwd=ROOT.parent, capture_output=True, check=True,
        )
        self.assertIn(b"\x1b[38;2;", result.stdout)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--color", "truecolor", "--quiet"],
            capture_output=True, check=True,
        )
        self.assertEqual(result.stdout, b"")

    def test_nonpositive_width_is_rejected(self):
        for width in ("0", "-1"):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--width", width], capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, b"")


if __name__ == "__main__":
    unittest.main()
