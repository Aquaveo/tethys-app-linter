#!/bin/sh -l

echo "Downloading app repository."
cd / && /opt/conda/envs/tethys/bin/git clone https://github.com/${1}.git

echo "Setting repository branch."
cd /$(basename $1) && /opt/conda/envs/tethys/bin/git checkout $2

echo "Running checks."
/opt/conda/envs/tethys/bin/python /tethys_app_linter.py $1
