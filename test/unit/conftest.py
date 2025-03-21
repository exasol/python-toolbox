from inspect import cleandoc

import pytest

from exasol.toolbox.tools import security


@pytest.fixture(scope="session")
def pip_audit_jinja2_issue():
    return security.Issue(
        cve="CVE-2025-27516",
        cwe="None",
        description=cleandoc(
            """An oversight in how the Jinja sandboxed environment interacts with the 
            `|attr` filter allows an attacker that controls the content of a template 
            to execute arbitrary Python code.  To exploit the vulnerability, an 
            attacker needs to control the content of a template. Whether that is the 
            case depends on the type of application using Jinja. This vulnerability 
            impacts users of applications which execute untrusted templates. Jinja's 
            sandbox does catch calls to `str.format` and ensures they don't escape the 
            sandbox. However, it's possible to use the `|attr` filter to get a 
            reference to a string's plain format method, bypassing the sandbox. After 
            the fix, the `|attr` filter no longer bypasses the environment's attribute 
            lookup."""
        ),
        coordinates="jinja2:3.1.5",
        references=(
            "https://github.com/advisories/GHSA-cpwx-vrp4-4pq7",
            "https://nvd.nist.gov/vuln/detail/CVE-2025-27516",
        ),
    )


@pytest.fixture(scope="session")
def pip_audit_cryptography_issue():
    return security.Issue(
        cve="CVE-2024-12797",
        cwe="None",
        description=cleandoc(
            """pyca / cryptography's wheels include a statically linked copy of 
            OpenSSL. The versions of OpenSSL included in  cryptography 42.0.0 - 44.0.0 
            are vulnerable to a security issue. More details about the vulnerability 
            itself can be found in https://openssl-library.org/news/secadv/20250211.txt. 
            If you are building cryptography source(\"sdist\") then you are responsible 
            for upgrading your copy of OpenSSL. Only users installing from wheels built 
            by the cryptography project(i.e., those distributed on PyPI) need to update 
            their cryptography versions."""
        ),
        coordinates="cryptography:43.0.3",
        references=(
            "https://github.com/advisories/GHSA-79v4-65xg-pq4g",
            "https://nvd.nist.gov/vuln/detail/CVE-2024-12797",
        ),
    )


@pytest.fixture(scope="session")
def pip_audit_report(pip_audit_jinja2_issue, pip_audit_cryptography_issue):
    jinja2_name, jinja2_version = pip_audit_jinja2_issue.coordinates.split(":")
    cryptography_name, cryptography_version = (
        pip_audit_cryptography_issue.coordinates.split(":")
    )
    return {
        "dependencies": [
            {
                "name": jinja2_name,
                "version": jinja2_version,
                "vulns": [
                    {
                        "id": "GHSA-cpwx-vrp4-4pq7",
                        "fix_versions": ["3.1.6"],
                        "aliases": [pip_audit_jinja2_issue.cve],
                        "description": pip_audit_jinja2_issue.description,
                    }
                ],
            },
            {
                "name": cryptography_name,
                "version": cryptography_version,
                "vulns": [
                    {
                        "id": "GHSA-79v4-65xg-pq4g",
                        "fix_versions": ["44.0.1"],
                        "aliases": [pip_audit_cryptography_issue.cve],
                        "description": pip_audit_cryptography_issue.description,
                    }
                ],
            },
        ]
    }
