# 0.12.0 - 2024-05-17

## 🐞 Fixed
* Added missing artifact uploads to checks.yml  

## ✨ Added
* **Added Support for Argument Forwarding to Test-Related Nox Tasks**

    **Overview:**
    With this new feature, it is now possible to forward additional arguments to the application (pytest) that executes the tests.

    For example this feature now allows for easy execution of a subset of tests using pytest’s `-k` expression selection or `-m` marker selection (see usage examples below).

    The forwarding will work for the following Nox tasks:
    - unit-tests
    - integration-tests
    - coverage

    **Usage:**

    To prepare a release, simply execute a command in your terminal as shown in the examples below:

    Filter tests based on pytest markers:
    ```shell
    nox -s unit-tests -- -m fast 
    ```

    Filter tests based on pytest expressions:
    ```shell
    nox -s unit-tests -- -k smoke_test 
    ```