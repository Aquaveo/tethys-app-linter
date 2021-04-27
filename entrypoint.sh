#!/bin/sh -l

echo -e "\033[1;4;34mRunning checks.\033[0m"
PYTHON_OUTPUT=$(/opt/conda/envs/tethys/bin/python "/tethys_app_linter.py" "$1" "$GITHUB_WORKSPACE")

RESULT=$(echo $PYTHON_OUTPUT | awk -F'RESULT: ' '{print $2}')

echo "::set-output name=result::$RESULT"
