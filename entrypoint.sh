#!/bin/sh -l

echo -e "\033[1;4;34mRunning checks.\033[0m"
PYTHON_OUTPUT=$(/opt/conda/envs/tethys/bin/python "/tethys_app_linter.py" "$1" "$GITHUB_WORKSPACE")

echo "$PYTHON_OUTPUT"

RESULT=$(echo "$PYTHON_OUTPUT" | awk -F'RESULT: ' '{print $2}')

if [ "$RESUlT"="Failed" ] ; then
  exit 1
fi
