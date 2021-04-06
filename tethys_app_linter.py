#!/usr/local/bin/python

import sys
import os
from glob import glob
import subprocess
import yaml

# variables
errors = False
python_version = sys.version[:3]
repo_owner, repo_name = sys.argv[1].split('/')
install_file = ''
app_python_package = ''

# check setup.py exists
print('Checking that setup.py exists.')
if os.path.isfile(f'/{repo_name}/setup.py'):
    print("setup.py file exists.")
else:
    errors = True
    print('setup.py not found.')

# check install.yml exists
print('Checking that install.yml exists.')
if os.path.isfile(f'/{repo_name}/install.yml'):
    install_file = f'/{repo_name}/install.yml'
    print("install.yml file exists.")
elif os.path.isfile(f'/{repo_name}/install.yaml'):
    install_file = f'/{repo_name}/install.yaml'
    print("install.yaml file exists.")
else:
    errors = True
    print("install.yml not found.")

# check that all dependencies are included in "install.yml"
print('Checking that all dependencies have been listed.')
if install_file:
    already_installed_requirements = []
    p0 = subprocess.Popen('. /opt/conda/bin/activate tethys && conda list', stdout=subprocess.PIPE, shell=True)
    requirements = []
    p1 = subprocess.Popen(f'/opt/conda/envs/tethys/bin/pipreqs {repo_name} --print', stdout=subprocess.PIPE, shell=True)
    for req in p1.communicate()[0].splitlines():
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
        errors = True
        requirement_diff = list(requirements.difference(listed_requirements))
        print(f'Missing requirements: {requirement_diff}')

# check that the app python package is the only directory in the app package directory
print('Checking that the app python package is the only directory in the app package directory.')
if len(os.listdir(f'/{repo_name}/tethysapp')) > 1:
    print('The app package contains directories other than the app python package')
else:
    app_python_package = os.listdir(f'/{repo_name}/tethysapp')[0]

# check that there's not an __init__.py file at the release and app package directories
print('Verifying that the release package directory is not a python package.')
if os.path.isfile(f'/{repo_name}/__init__.py'):
    errors = True
    print('Found an "__init__.py" file in the release package directory. Please remove it.')
elif os.path.isfile(f'/{repo_name}/tethysapp/__init__.py'):
    errors = True
    print('Found an "__init__.py" file in the app package directory. Please remove it.')

# check that __init__.py in app python package is empty
if app_python_package:
    print('Verifying that the __init__.py file in the app python package is empty.')
    if os.path.isfile(f'/{repo_name}/tethysapp/{app_python_package}/__init__.py'):
        with open(f'/{repo_name}/tethysapp/{app_python_package}/__init__.py', 'r') as f:
            if f.read():
                print('The app python package "__init__.py" file should  be empty.')

# install the app
if app_python_package:
    print('Testing app installation.')
    if not errors:
        p2 = subprocess.Popen(
            [f'cd /{repo_name} && /opt/conda/envs/tethys/bin/tethys install'],
            stdout=subprocess.PIPE,
            shell=True
        )
        print(p2.communicate()[0])

# check that needed non-python files were properly added to the resource_files variable of setup.py
if app_python_package:
    non_python_files_repo = []
    non_python_files_installation = []
    repo_python_package = f'/{repo_name}/tethysapp/{app_python_package}'
    installed_python_package = glob(f'/opt/conda/envs/tethys/lib/python{python_version}/site-packages/{repo_name}*')[0]

    for root, subdirs, files in os.walk(repo_python_package):
        for file in files:
            if not file.endswith('.py'):
                non_python_files_repo.append(file)

    for root, subdirs, files in os.walk(installed_python_package):
        for file in files:
            if not file.endswith('.py'):
                non_python_files_installation.append(file)

    for file in non_python_files_repo:
        if file not in non_python_files_installation:
            print(f'The file "{file}" was not added to the "resource_files" variable in the setup.py.')
