---
name: codebase-test-automation
description: Run and monitor the Tiny Shop Checkout unittest suite, report each test result, and start file-change testing in VS Code. Use when invoking this project's tests or changing its files.
metadata:
  short-description: Run and monitor Tiny Shop tests
---

# Tiny Shop test automation

Use the existing Python `unittest` suite in `tests/`; do not add a framework or change application code as part of test execution.

When invoked manually, inspect `tests/` for test modules and cases, then run `python scripts/watch_tests.py --root . --once` from `learner/starter/` (or the equivalent Python executable available in the environment). This runs the full suite and creates the JSON report. Report the discovered cases and actual passed, failed, and skipped counts. Include failure/error messages and tracebacks when a case fails. Do not claim unrun tests passed.

For continuous checking, the project includes `scripts/watch_tests.py`. The repository-root VS Code folder-open task starts it when this lab repository is opened as the workspace. VS Code workspace trust may be required to allow the task. The watcher runs the complete discovered suite at startup and after detected file changes, with a short quiet period to combine rapid saves. It writes per-test results and failure details to `test-reports/latest.json` and prints a summary. It monitors project files while excluding Git internals, Python bytecode caches, and its generated report directory. Stop the watcher from its terminal to end monitoring.

Run the watcher directly when not using the configured VS Code task:

```sh
python scripts/watch_tests.py --root .
```

Do not alter existing source or test files without user approval. Changes to the skill, watcher, or VS Code task are separate from modifying application code. The project currently contains a Python checkout function and `unittest` tests; there is no frontend suite or separate backend test framework to invoke.


