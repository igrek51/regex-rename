#!/bin/bash
set -euo pipefail

MODULE_NAME=regex_rename
PYTHON_INTERPRETER="${PYTHON_INTERPRETER:-python3}"

${PYTHON_INTERPRETER} -m coverage run --source ${MODULE_NAME} -m pytest -vv --tb=short -ra --color=yes $@
# show code coverage info
${PYTHON_INTERPRETER} -m coverage report -m
