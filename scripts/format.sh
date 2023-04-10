#!/bin/sh -e

#* If script triggers error, exit
# set -e

#* Show trace in terminal
set -x

#* Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --apply app
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py,base.py

#* Lint with black and sirt with isort again
black app
isort --recursive --apply app

#* Affirm typing, linnting and formatting
# mypy app
black app --check
isort --recursive --check-only app
flake8

#* Test coverage generated via HTML
# pytest --cov=app --cov-report=html app/tests "${@}"