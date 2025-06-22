# Automatic Tree Registration in SQLAlchemy MPTT

This project addresses a recurring reliability issue in the `BaseNestedSets` mixin used by the `sqlalchemy-mptt` library. Previously, every subclass required a manual call to `register_tree()` to enable tree functionality via SQLAlchemy event listeners. If omitted, tree logic (such as setting left/right values) would silently fail.

The goal was to refactor the mixin to automatically register subclasses, using SQLAlchemy's lifecycle hooks to detect and configure them correctly. This change improves reliability, reduces boilerplate, and ensures tree operations work consistently.

---

## What This Project Demonstrates

This repository includes:

- Four different candidate implementations attempting to solve the problem
- A detailed evaluation comparing them on correctness, safety, and maintainability
- A final selected implementation that resolves the issue with minimal, robust logic
- Test scripts and runtime verification of the chosen approach

This reflects the kind of work involved in AI code evaluation — reading and ranking competing code snippets, identifying correctness and edge cases, and explaining the rationale for choosing one implementation over others.

---

## File Structure

├── after/ # Final chosen implementation
│ └── mixins_after.py
├── before/ # Original version requiring manual registration
│ └── mixins_before.py
├── diffs/ # Four candidate implementations and evaluation
│ ├── diff1.py
│ ├── diff2.py
│ ├── diff3.py
│ ├── diff4.py
│ └── evaluation.md
├── tests/ # Unit test to confirm automatic registration
│ └── test_auto_registration.py
├── debug/ # Manual test to observe event behavior
│ └── debug_test.py
└── README.md

---

## Diff Evaluation

To determine the best approach, I reviewed four competing diffs, each proposing a different strategy for triggering automatic registration. These were assessed based on functional behavior, event scope, subclass filtering, and long-term maintainability.

The results and conclusions are documented in [diffs/evaluation.md](diffs/evaluation.md).

---

## Final Implementation

The selected version uses SQLAlchemy’s `mapper_configured` event to automatically register subclasses when their ORM mappers are initialized. It includes safeguards to prevent duplicate registrations and applies only to valid subclasses. The full implementation is available in [`after/mixins_after.py`](after/mixins_after.py).

---

## Testing

A minimal test in [`tests/test_auto_registration.py`](tests/test_auto_registration.py) confirms that event listeners are registered correctly and that no manual `register_tree()` call is needed.

---

## Summary

This project demonstrates how to evaluate, compare, and implement solutions to subtle behavioral problems in Python codebases. It highlights not only technical ability in Python and SQLAlchemy, but also judgment in code review and reasoning — skills critical to training and evaluating AI-generated code.
