# Project Guide

## Purpose and scope

This repository contains a self-contained Day 2 training lab about project instructions for Codex. Its learner project is Tiny Shop Checkout, a deliberately small Python example. The root README describes instructor materials, but the checked-in tree contains only `learner/` materials and does not include the referenced `instructor/` directory.

## Structure

- `README.md` explains the lab bundle and a suggested session comparing work with and without project instructions.
- `learner/starter/` is the clean learner project; it intentionally has no `AGENTS.md`.
- `learner/starter/src/checkout.py` defines `calculate_total(items)`.
- `learner/starter/tests/test_checkout.py` contains the visible `unittest` tests.
- `learner/starter/sample_orders.json` contains two synthetic order lines for inspection.
- `learner/starter/task_card.md` specifies two exercises: optional percentage discounts and a separate currency-formatting helper. These are task requirements, not existing functionality.
- `learner/starter/comparison_worksheet.md` is for recording observations from the guided and unguided runs.
- `learner/starter/README.md` documents the starter project and its local test command.
- `learner/skill_and_mcp_lab.md` extends the course with instructional material about Skills, plugins, MCP grounding, integrations, and review. Its examples are lab guidance, not dependencies or configured services in this repository.
- `learner/integration_task_template.md` is an instructor-completed template for a cohort integration exercise; placeholders are not project configuration.

## Application behavior and contract

`calculate_total(items)` iterates over item mappings with `price` and `quantity` keys, converts each price to `float` and quantity to `int`, multiplies them, and returns the accumulated total as a float. The `name` field appears in the sample data but is not read by the function. An empty sequence returns `0.0`. The source docstring explicitly says floats are intentional for this teaching exercise and notes that production money code would normally use `Decimal` or integer minor units.

Do not describe discounts or formatted currency as implemented behavior: they appear only in the task card. The existing function returns a numeric float and does not format currency.

## Development and verification

The starter README documents this command, run from `learner/starter/`:

```sh
python3 -m unittest discover -s tests -v
```

It states that no package installation is required. The test module uses Python's standard-library `unittest` framework and imports `calculate_total` from `src.checkout`. The checked-in tests cover a single item, multiple items, an empty cart, and the float return type.

There is no dependency manifest, lock file, build configuration, linter configuration, or CI workflow in the checked-in project tree. Do not infer additional setup steps or tooling.

## Conventions for changes

- Keep checkout calculation in `src/checkout.py` and tests in `tests/`.
- Preserve the documented `calculate_total(items)` contract unless the task explicitly changes it.
- Keep calculation numeric and currency presentation separate, consistent with Task B's stated requirement.
- Add or update focused `unittest` cases for requested behavior and boundaries.
- Do not add a dependency or change the item schema for Task A; these constraints are explicit in the task card.
- Use the documented test command and report its actual result when verification is requested.
- Treat lab instructions, templates, examples, and requested future tasks as instructional content, not evidence that related code or integrations already exist.
