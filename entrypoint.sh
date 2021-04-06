#!/bin/sh -l

cd / && /opt/conda/envs/tethys/bin/git clone https://github.com/${1}.git

/opt/conda/envs/tethys/bin/python /tethys_app_linter.py $1
