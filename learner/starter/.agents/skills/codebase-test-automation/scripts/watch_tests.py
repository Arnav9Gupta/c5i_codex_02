import argparse
import hashlib
import json
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

IGNORED_DIRS = {".git", "__pycache__", "test-reports"}


class RecordingResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.cases = []
        self._records = {}

    def startTest(self, test):
        super().startTest(test)
        record = {"id": test.id(), "status": "running"}
        self.cases.append(record)
        self._records[test] = record

    def addSuccess(self, test):
        super().addSuccess(test)
        self._records[test]["status"] = "passed"

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._records[test].update(status="skipped", detail=reason)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._records[test].update(status="failed", detail=self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self._records[test].update(status="failed", detail=self._exc_info_to_string(err, test))

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self._records[test].update(status="skipped", detail="Expected failure")

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self._records[test].update(status="failed", detail="Unexpected success")


def fingerprint(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if any(part in IGNORED_DIRS for part in path.parts) or path.suffix == ".pyc":
            continue
        if path.is_file():
            try:
                digest.update(path.relative_to(root).as_posix().encode())
                digest.update(path.read_bytes())
            except OSError:
                continue
    return digest.digest()


def run_tests(root):
    previous_path = list(sys.path)
    sys.path.insert(0, str(root))
    try:
        suite = unittest.defaultTestLoader.discover(str(root / "tests"))
        result = RecordingResult()
        started = datetime.now(timezone.utc).isoformat()
        started_at = time.monotonic()
        suite.run(result)
        duration = round(time.monotonic() - started_at, 3)
    finally:
        sys.path[:] = previous_path

    counts = {status: sum(case["status"] == status for case in result.cases)
              for status in ("passed", "failed", "skipped")}
    report = {
        "started_at": started,
        "project": root.name,
        "framework": "unittest",
        "discovered": len(result.cases),
        "counts": counts,
        "duration_seconds": duration,
        "successful": result.wasSuccessful(),
        "tests": result.cases,
    }
    report_dir = root / "test-reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / "latest.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"{started} | {len(result.cases)} tests: {counts['passed']} passed, "
          f"{counts['failed']} failed, {counts['skipped']} skipped")
    print(f"Report: {report_path}")
    for case in result.cases:
        if case["status"] == "failed":
            print(f"\nFAIL: {case['id']}\n{case.get('detail', '')}")
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description="Run Tiny Shop tests on file changes.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4],
                        help="Tiny Shop Checkout project directory")
    parser.add_argument("--interval", type=float, default=0.75,
                        help="File polling interval in seconds")
    parser.add_argument("--quiet-period", type=float, default=1.25,
                        help="Quiet period after changes before testing")
    parser.add_argument("--once", action="store_true",
                        help="Run once and exit instead of watching")
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "tests").is_dir():
        parser.error(f"No tests directory found under {root}")

    print(f"Watching {root} for changes. Press Ctrl+C to stop.", flush=True)
    state = fingerprint(root)
    successful = run_tests(root)
    if args.once:
        return 0 if successful else 1
    try:
        while True:
            time.sleep(args.interval)
            current = fingerprint(root)
            if current == state:
                continue
            state = current
            last_change = time.monotonic()
            while time.monotonic() - last_change < args.quiet_period:
                time.sleep(args.interval)
                updated = fingerprint(root)
                if updated != state:
                    state = updated
                    last_change = time.monotonic()
            run_tests(root)
    except KeyboardInterrupt:
        print("\nStopped watching.", flush=True)


if __name__ == "__main__":
    main()
