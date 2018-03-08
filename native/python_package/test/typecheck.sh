#!/bin/sh
# call this from the parent directory
mypy --ignore-missing-imports --follow-imports silent --disallow-untyped-calls \
    --disallow-untyped-defs --check-untyped-defs --warn-unused-ignores \
    --strict-optional python_driver/*.py
