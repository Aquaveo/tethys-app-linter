# tethys-app-linter
A GitHub Action to check the code integrity of  Tethys applications.

## Example

```yaml
name: tethys-app-linter

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    name: Lint
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Run tethys-app-linter
        uses: Aquaveo/tethys-app-linter@v1
```

This action uses the checkout action to access the repository.

The main input to this action is the gihub repository that triggers it. The action will get this value automatically by using the `${{ github.repository }}` variable.

## Checks

|Check|Description|
|-----|-----------|
|setup_py_exists|Verifies that setup.py exists and is in the right location|
|install_yml_exists|Verifies that install.yml exists and is in the right location|
|install_yml_is_valid|Verifies that install.yml is formatted correctly|
|check_dependencies|Verifies that all app dependencies are listed in the install.yml|
|app_python_package_is_only app_and_release_package_are_not_python_packages init_py_is_empty|Verify that the app package directory is structured correctly|
|is_tethys_3|Verifies that the app is Tethys 3 version compatible|
|install_app|Verifies that the app is installable (no installation errors)|
|non_python_files_added|Verifies that needed non-python files were properly added to the resource_files variable of setup.py
