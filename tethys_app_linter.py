#!/usr/local/bin/python

import sys
import os
import subprocess
import yaml

# parse repo name
repo_owner, repo_name = sys.argv[1].split('/')

install_file = ''

# check setup.py exists
if os.path.isfile(f'/{repo_name}/setup.py'):
    print("setup.py file exists.")
else:
    print("setup.py not found.")

# check install.yml exists
if os.path.isfile(f'/{repo_name}/install.yml'):
    install_file = f'/{repo_name}/install.yml'
    print("install.yml file exists.")
elif f'{repo_name}/install.yaml':
    install_file = os.path.isfile(f'/{repo_name}/install.yaml')
    print("install.yaml file exists.")
else:
    print("install.yml not found.")

# check that all dependencies are included in "install.yml"
if install_file:
    requirements = []
    p = subprocess.Popen(['pipreqs', repo_name, "--print"], stdout=subprocess.PIPE)
    for req in p.communicate()[0].splitlines():
        package, version = req.decode("utf-8").split('==')
        if package != 'tethys_platform' and package != 'tethys_platform.egg':
            requirements.append(package)

    listed_requirements = []
    with open(install_file, 'r') as f:
        install_file_contents = yaml.safe_load(f).get('requirements', {})
    if install_file_contents and install_file_contents['conda']['packages']:
        listed_requirements.extend(install_file_contents['conda']['packages'])
    if install_file_contents and install_file_contents['pip']:
        listed_requirements.extend(install_file_contents['pip'])

    requirements = set(sorted(requirements))
    listed_requirements = set(sorted(listed_requirements))

    if listed_requirements.issubset(requirements):
        print('All requirements are listed.')
    else:
        requirement_diff = list(requirements.difference(listed_requirements))
        print(f'Missing requirements: {requirement_diff}')
        print(requirements, listed_requirements)
