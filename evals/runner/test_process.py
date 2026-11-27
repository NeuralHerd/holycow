import os
import shutil
import signal
import sys
import tempfile
import time
import unittest
from pathlib import Path

from runner import process

# Starts a grandchild that leaves the process group with setsid, keeps the output pipes open and records
# its PID so the test can stop it.
ESCAPE = r"""
import subprocess, sys, time
subprocess.Popen([sys.executable, "-c",
    "import os, sys, time; os.setsid(); open(sys.argv[1], 'w').write(str(os.getpid())); time.sleep(60)",
    sys.argv[1]])
time.sleep(60)
"""


class RunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_returns_output_and_exit_code(self):
        stdout, stderr, code, timed_out = process.run(
            [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)"],
            self.tmp, dict(os.environ), timeout=30)
        self.assertEqual((stdout, stderr, code, timed_out), ("out\n", "err\n", 3, False))

    def test_timeout_keeps_partial_output(self):
        stdout, _, code, timed_out = process.run(
            [sys.executable, "-c", "import time; print('started', flush=True); time.sleep(60)"],
            self.tmp, dict(os.environ), timeout=1)
        self.assertEqual((stdout, code, timed_out), ("started\n", None, True))

    def test_a_descendant_holding_the_pipes_cannot_hang_the_runner(self):
        pid_file = self.tmp / "escaped.pid"
        started = time.monotonic()
        _, _, code, timed_out = process.run([sys.executable, "-c", ESCAPE, str(pid_file)], self.tmp,
                                            dict(os.environ), timeout=1, grace=1)
        self.assertTrue(timed_out)
        self.assertLess(time.monotonic() - started, 10)
        for _ in range(50):
            if pid_file.exists() and pid_file.read_text():
                break
            time.sleep(0.1)
        os.kill(int(pid_file.read_text()), signal.SIGKILL)


if __name__ == "__main__":
    unittest.main()
