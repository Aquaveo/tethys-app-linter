#!/bin/sh -l

cd / && /opt/conda/envs/tethys/bin/git clone https://github.com/${1}.git
cd $(basename $1) && /opt/conda/envs/tethys/bin/git checkout $2

/opt/conda/envs/tethys/bin/python /tethys_app_linter.py $1
