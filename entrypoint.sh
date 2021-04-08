#!/bin/sh -l

echo -e "\033[1;4;34mRunning checks.\033[0m"
/opt/conda/envs/tethys/bin/python /tethys_app_linter.py "$1" "$GITHUB_WORKSPACE"
