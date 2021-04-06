#!/bin/sh -l

echo "Running checks."
/opt/conda/envs/tethys/bin/python /tethys_app_linter.py "$1" "$GITHUB_WORKSPACE"
