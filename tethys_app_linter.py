#!/opt/conda/envs/tethys/bin/python

import sys
import os
from glob import glob
import subprocess
import yaml
from typing import Literal

# colors
end_style = '\033[0m'
red_style = '\033[0;31m'
green_style = '\033[0;32m'
orange_style = '\033[0;33m'
blue_style = '\033[0;34m'

# variables
success = True
python_version = sys.version[:3]
pipreqs_exec = '/opt/conda/envs/tethys/bin/pipreqs'
repo_owner, repo_name = sys.argv[1].split('/')
workspace = sys.argv[2]

# use test_app if running on self
if repo_name == 'tethys-app-linter':
    repo_name = 'tethysapp-test_app'
    workspace = os.path.join('/', repo_name)


# print colors
def c_print(msg: str, style: Literal[red_style, green_style, orange_style, blue_style]) -> str:
    print(f'{style}{msg}{end_style}')


# check setup.py exists
def setup_py_exists(path: str = workspace) -> bool:
    c_print('Verifying that setup.py exists', blue_style)
    if os.path.isfile(os.path.join(path, 'setup.py')):
        c_print('setup.py file exists.', green_style)
        return True
    else:
        c_print('setup.py not found.', red_style)
        return False


# check install.yml exists
def install_yml_exists(path: str = workspace) -> str:
    c_print('Verifying that install.yml exists.', blue_style)
    if os.path.isfile(os.path.join(path, 'install.yml')):
        c_print('install.yml file exists.', green_style)
        file_path = os.path.join(path, 'install.yml')
        is_valid_yml = install_yml_is_valid(file_path)
        if is_valid_yml:
            return file_path
    elif os.path.isfile(os.path.join(path, 'install.yaml')):
        c_print('install.yaml file exists.', green_style)
        file_path = os.path.join(path, 'install.yaml')
        is_valid_yml = install_yml_is_valid(file_path)
        if is_valid_yml:
            return file_path
    else:
        c_print('install.yml not found.', red_style)
        return ''


# check install.yml is valid yml
def install_yml_is_valid(file_path: str) -> bool:
    c_print('Validating install.yml.', blue_style)
    try:
        with open(file_path, 'r') as yml:
            yaml.safe_load(yml)
        return True
    except Exception as e:
        c_print(e, red_style)
        return False


# check that all dependencies are included in "install.yml"
def check_dependencies(file_path: str, repo_path: str = workspace) -> bool:
    if file_path:
        c_print('Verifying that all dependencies have been listed.', blue_style)
        # generate tethys_platform dependencies
        tethys_platform_dependencies = []
        tethys_platform_installation_path = glob(
            f'/opt/conda/envs/tethys/lib/python{python_version}/site-packages/tethys_platform*'
        )[0]
        with open(os.path.join(tethys_platform_installation_path, 'top_level.txt'), 'r') as submodule_list:
            tethys_libraries = submodule_list.read().splitlines()

        for lib in tethys_libraries:
            p0 = subprocess.Popen(
                f'{pipreqs_exec} /opt/conda/envs/tethys/lib/python{python_version}/site-packages/{lib} --print',
                stdout=subprocess.PIPE,
                shell=True
            )
            for req in p0.communicate()[0].splitlines():
                package, version = req.decode('utf-8').split('==')
                if package.lower() not in tethys_platform_dependencies:
                    tethys_platform_dependencies.append(package.lower())

        requirements = []
        p1 = subprocess.Popen(
            f'{pipreqs_exec} {repo_path} --print',
            stdout=subprocess.PIPE,
            shell=True
        )
        for req in p1.communicate()[0].splitlines():
            package, version = req.decode('utf-8').split('==')
            if package.lower() not in tethys_platform_dependencies:
                requirements.append(package.lower())

        listed_requirements = []
        with open(file_path, 'r') as yml:
            install_file_contents = yaml.safe_load(yml).get('requirements', {})
        if install_file_contents and install_file_contents['conda']['packages']:
            listed_requirements.extend(install_file_contents['conda']['packages'])
        if install_file_contents and install_file_contents['pip']:
            listed_requirements.extend(install_file_contents['pip'])

        requirements = set(requirements)
        listed_requirements = set(listed_requirements)

        if not requirements or listed_requirements.issubset(requirements):
            c_print('All requirements are listed.', green_style)
            return True
        else:
            requirement_diff = list(requirements.difference(listed_requirements))
            c_print(f'Missing requirements: {requirement_diff}', red_style)
            return False
    else:
        c_print('Dependencies not checked. Could not find install.yml.', red_style)
        return False


# check that the app python package is the only directory in the app package directory
def app_python_package_is_only(path: str = workspace) -> str:
    c_print('Verifying that the app python package is the only directory in the app package directory.', blue_style)
    if len(os.listdir(os.path.join(path, 'tethysapp'))) > 1:
        c_print('The app package contains directories other than the app python package', red_style)
        return ''
    return os.listdir(os.path.join(path, 'tethysapp'))[0]


# check tethys 3 syntax
def is_tethys_3(app_python_package: str) -> bool:
    ret = False
    if app_python_package:
        check1 = app_and_release_package_are_not_python_packages()
        check2 = init_py_is_empty(app_python_package)
        if check1 and check2:
            ret = True
    return ret


# check that there's not an __init__.py file at the release and app package directories
def app_and_release_package_are_not_python_packages(path: str = workspace) -> bool:
    c_print('Verifying that the release package directory is not a python package.', blue_style)
    ret = True
    if os.path.isfile(os.path.join(path, '__init__.py')):
        c_print('Found "__init__.py" in the release package directory. Please remove it.', red_style)
        ret = False
    if os.path.isfile(os.path.join(path, 'tethysapp', '__init__.py')):
        c_print('Found "__init__.py" in the app package directory. Please remove it.', red_style)
        ret = False
    return ret


# check that __init__.py in app python package is empty
def init_py_is_empty(app_python_package: str, path: str = workspace) -> bool:
    c_print('Verifying that the __init__.py file in the app python package is empty.', blue_style)
    if os.path.isfile(os.path.join(path, 'tethysapp', app_python_package, '__init__.py')):
        with open(os.path.join(path, 'tethysapp', app_python_package, '__init__.py'), 'r') as f:
            for line in f.readlines():
                if not line.startswith("#"):
                    c_print('The app python package "__init__.py" file should be empty.', red_style)
                    return False
    return True


# install the app
def install_app(path: str = workspace) -> bool:
    c_print('Testing app installation.', blue_style)
    p2 = subprocess.Popen(
        [f'cd {path} ; . /opt/conda/bin/activate tethys && python setup.py install'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    res = p2.communicate()
    lines = res[0].decode('utf-8').splitlines()
    for line in lines:
        print(line)
    if 'error' not in res[1].decode('utf-8').lower():
        return True
    return False


# check that needed non-python files were properly added to the resource_files variable of setup.py
def non_python_files_added(app_python_package: str) -> None:
    if app_python_package:
        c_print(
            'Verifying that needed non-python files were properly added to the "resource_files" variable of setup.py',
            blue_style
        )
        non_python_files_repo = []
        non_python_files_installation = []
        repo_python_package = os.path.join(workspace, 'tethysapp', app_python_package)
        installed_python_package = glob(
            f'/opt/conda/envs/tethys/lib/python{python_version}/site-packages/{repo_name.replace("-", "_")}*'
        )[0]

        for root, subdirs, files in os.walk(repo_python_package):
            for file in files:
                if not file.startswith('.') and not file.endswith('.py'):
                    non_python_files_repo.append(file)

        for root, subdirs, files in os.walk(installed_python_package):
            for file in files:
                if not file.endswith('.py'):
                    non_python_files_installation.append(file)

        for file in non_python_files_repo:
            if file not in non_python_files_installation:
                c_print(
                    f'The file "{file}" was not added to the "resource_files" variable in the setup.py.',
                    orange_style
                )


def main() -> str:
    app_installed = False
    setup_py = setup_py_exists()
    install_yml = install_yml_exists()
    dependencies = check_dependencies(install_yml)
    app_python_package = app_python_package_is_only()
    tethys3 = is_tethys_3(app_python_package)

    checks = [setup_py, os.path.isfile(install_yml), dependencies, tethys3]

    if all(check for check in checks):
        app_installed = install_app()
        non_python_files_added(app_python_package)

    if app_installed:
        c_print('The app passed all the checks.\nRESULT: Success', green_style)
    else:
        c_print('The app did not pass all the checks.\nRESULT: Failed', red_style)


if __name__ == "__main__":
    main()
