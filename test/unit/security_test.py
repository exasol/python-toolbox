import json
import os
import subprocess
from contextlib import contextmanager
from inspect import cleandoc
from unittest import mock

import pytest

from exasol.toolbox.tools import security


@contextmanager
def empty_path():
    """Make sure the PATH environment variable is empty."""
    old_path = os.environ["PATH"]
    os.environ["PATH"] = ""
    yield
    os.environ["PATH"] = old_path


class TestCreateSecurityIssue:
    @pytest.mark.parametrize(
        "expected,issue",
        [
            (
                "🔐 CVE-2023-39410: pkg:maven/fr.turri/aXMLRPC@1.13.0",
                security.Issue(
                    cve="CVE-2023-39410",
                    cwe="None",
                    description="None",
                    coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
                    references=tuple(),
                ),
            )
        ],
    )
    def test_security_issue_title_template(self, expected, issue):
        actual = security.security_issue_title(issue)
        assert actual == expected

    @pytest.mark.parametrize(
        "expected,issue",
        [
            (
                cleandoc(
                    """
                                ## Summary
                                Random Multiline
                                Description
                                ;)

                                CVE: CVE-2023-39410
                                CWE: CWE-XYZ

                                ## References
                                - https://www.example.com
                                - https://www.foobar.com
                                """
                ),
                security.Issue(
                    cve="CVE-2023-39410",
                    cwe="CWE-XYZ",
                    description="Random Multiline\nDescription\n;)",
                    coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
                    references=("https://www.example.com", "https://www.foobar.com"),
                ),
            )
        ],
    )
    def test_security_issue_body_template(self, expected, issue):
        actual = security.security_issue_body(issue)
        assert actual == expected

    def test_gh_cli_is_not_available(self):
        with empty_path():
            with pytest.raises(FileNotFoundError) as exec_info:
                set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = "Command 'gh' not found. Please make sure you have installed the github cli."

        assert actual == expected

    @mock.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd=[
                "gh",
                "issue",
                "create",
                "--label",
                "security",
                "--title",
                "<title>",
                "--body",
                "<body>",
            ],
        ),
    )
    def test_gh_cli_failed(self, _):
        with pytest.raises(subprocess.CalledProcessError) as exec_info:
            set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = str(
            subprocess.CalledProcessError(
                returncode=1,
                cmd=[
                    "gh",
                    "issue",
                    "create",
                    "--label",
                    "security",
                    "--title",
                    "<title>",
                    "--body",
                    "<body>",
                ],
            )
        )
        assert actual == expected

    @mock.patch("subprocess.run")
    def test_query_gh_security_issues(self, run_mock):
        result = mock.MagicMock(subprocess.CompletedProcess)
        result.returncode = 0
        result.stdout = b"https://github.com/exasol/some-project/issues/16"
        result.stderr = b"Creating Issue"
        run_mock.return_value = result

        issues = security.Issue(
            cve="CVE-2023-39410",
            cwe="None",
            description="None",
            coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
            references=tuple(),
        )

        expected = (
            "Creating Issue",
            "https://github.com/exasol/some-project/issues/16",
        )
        actual = security.create_security_issue(issues)
        assert actual == expected


class TestGhSecurityIssues:
    def test_gh_cli_is_not_available(self):
        with empty_path():
            with pytest.raises(FileNotFoundError) as exec_info:
                set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = "Command 'gh' not found. Please make sure you have installed the github cli."

        assert actual == expected

    @mock.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd=[
                "gh",
                "issue",
                "list",
                "--label",
                "security",
                "--search",
                "CVE",
                "--json",
                "id,title",
                "1000",
                "--state",
                "all",
            ],
        ),
    )
    def test_gh_cli_failed(self, _):
        with pytest.raises(subprocess.CalledProcessError) as exec_info:
            set(security.gh_security_issues())

        actual = f"{exec_info.value}"
        expected = str(
            subprocess.CalledProcessError(
                returncode=1,
                cmd=[
                    "gh",
                    "issue",
                    "list",
                    "--label",
                    "security",
                    "--search",
                    "CVE",
                    "--json",
                    "id,title",
                    "1000",
                    "--state",
                    "all",
                ],
            )
        )
        assert actual == expected

    @mock.patch("subprocess.run")
    def test_query_gh_security_issues(self, run_mock):
        result = mock.MagicMock(subprocess.CompletedProcess)
        result.returncode = 0
        result.stdout = (
            b'[{"id":"I_kwDOIRnUks5zutba","title":"\xf0\x9f\x90\x9e CVE-2023-41105: Fix build scripts "},'
            b'{"id":"I_kwDOIRnUks5clFdR","title":"\xf0\x9f\x90\x9e CVE-2023-40217: Version check issues"}]\n'
        )
        run_mock.return_value = result

        expected = {
            ("I_kwDOIRnUks5zutba", "CVE-2023-41105"),
            ("I_kwDOIRnUks5clFdR", "CVE-2023-40217"),
        }
        actual = set(security.gh_security_issues())
        assert actual == expected


@pytest.fixture()
def maven_report():
    yield json.dumps(
        {
            "reports": {
                "org.apache.derby:derbyclient:jar:10.14.2.0:test": {
                    "coordinates": "pkg:maven/org.apache.derby/derbyclient@10.14.2.0",
                    "description": "The Derby client JDBC driver, used to connect to a Derby server over a network connection.",
                    "reference": "https://ossindex.sonatype.org/component/pkg:maven/org.apache.derby/derbyclient@10.14.2.0?utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                },
                "org.apache.commons:commons-configuration2:jar:2.8.0:compile": {
                    "coordinates": "pkg:maven/org.apache.commons/commons-configuration2@2.8.0",
                    "description": "Tools to assist in the reading of configuration/preferences files in\n        various formats",
                    "reference": "https://ossindex.sonatype.org/component/pkg:maven/org.apache.commons/commons-configuration2@2.8.0?utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                },
            },
            "vulnerable": {
                "org.apache.avro:avro:jar:1.7.7:compile": {
                    "coordinates": "pkg:maven/org.apache.avro/avro@1.7.7",
                    "description": "Avro core components",
                    "reference": "https://ossindex.sonatype.org/component/pkg:maven/org.apache.avro/avro@1.7.7?utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                    "vulnerabilities": [
                        {
                            "id": "CVE-2023-39410",
                            "displayName": "CVE-2023-39410",
                            "title": "[CVE-2023-39410] CWE-502: Deserialization of Untrusted Data",
                            "description": "When deserializing untrusted or corrupted data, it is possible for a reader to consume memory beyond the allowed constraints and thus lead to out of memory on the system.\n\nThis issue affects Java applications using Apache Avro Java SDK up to and including 1.11.2.  Users should update to apache-avro version 1.11.3 which addresses this issue.\n\n",
                            "cvssScore": 7.5,
                            "cvssVector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
                            "cwe": "CWE-502",
                            "cve": "CVE-2023-39410",
                            "reference": "https://ossindex.sonatype.org/vulnerability/CVE-2023-39410?component-type=maven&component-name=org.apache.avro%2Favro&utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                            "externalReferences": [
                                "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2023-39410",
                                "https://github.com/apache/avro/pull/2432",
                                "https://issues.apache.org/jira/browse/AVRO-3819",
                                "https://lists.apache.org/thread/q142wj99cwdd0jo5lvdoxzoymlqyjdds",
                            ],
                        }
                    ],
                },
                "fr.turri:aXMLRPC:jar:1.13.0:test": {
                    "coordinates": "pkg:maven/fr.turri/aXMLRPC@1.13.0",
                    "description": "Lightweight Java XML-RPC working also on Android.",
                    "reference": "https://ossindex.sonatype.org/component/pkg:maven/fr.turri/aXMLRPC@1.13.0?utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                    "vulnerabilities": [
                        {
                            "id": "CVE-2020-36641",
                            "displayName": "CVE-2020-36641",
                            "title": "[CVE-2020-36641] CWE-611: Improper Restriction of XML External Entity Reference ('XXE')",
                            "description": "A vulnerability classified as problematic was found in gturri aXMLRPC up to 1.12.0. This vulnerability affects the function ResponseParser of the file src/main/java/de/timroes/axmlrpc/ResponseParser.java. The manipulation leads to xml external entity reference. Upgrading to version 1.12.1 is able to address this issue. The patch is identified as ad6615b3ec41353e614f6ea5fdd5b046442a832b. It is recommended to upgrade the affected component. VDB-217450 is the identifier assigned to this vulnerability.\n\nSonatype's research suggests that this CVE's details differ from those defined at NVD. See https://ossindex.sonatype.org/vulnerability/CVE-2020-36641 for details",
                            "cvssScore": 9.8,
                            "cvssVector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                            "cwe": "CWE-611",
                            "cve": "CVE-2020-36641",
                            "reference": "https://ossindex.sonatype.org/vulnerability/CVE-2020-36641?component-type=maven&component-name=fr.turri%2FaXMLRPC&utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                            "externalReferences": [
                                "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2020-36641",
                                "https://www.tenable.com/cve/CVE-2020-36641",
                            ],
                        }
                    ],
                },
            },
            "excludedVulnerabilities": [
                {
                    "id": "CVE-2023-4586",
                    "displayName": "CVE-2023-4586",
                    "title": "[CVE-2023-4586] CWE-300: Channel Accessible by Non-Endpoint ('Man-in-the-Middle')",
                    "description": "netty-handler - Improper Certificate Validation\n\nThe product does not adequately verify the identity of actors at both ends of a communication channel, or does not adequately ensure the integrity of the channel, in a way that allows the channel to be accessed or influenced by an actor that is not an endpoint.",
                    "cvssScore": 6.5,
                    "cvssVector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:N",
                    "cwe": "CWE-300",
                    "cve": "CVE-2023-4586",
                    "reference": "https://ossindex.sonatype.org/vulnerability/CVE-2023-4586?component-type=maven&component-name=io.netty%2Fnetty-handler&utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                    "externalReferences": [
                        "https://docs.oracle.com/javase/8/docs/api/javax/net/ssl/SSLParameters.html#setEndpointIdentificationAlgorithm-java.lang.String-",
                        "https://github.com/netty/netty/issues/8537",
                        "https://github.com/netty/netty/issues/9930",
                        "https://netty.io/4.1/api/io/netty/handler/ssl/SslContext.html#newHandler-io.netty.buffer.ByteBufAllocator-java.util.concurrent.Executor-",
                    ],
                }
            ],
        }
    )


def test_convert_maven_input(maven_report):  # pylint: disable=redefined-outer-name
    expected = {
        security.Issue(
            cve="CVE-2023-39410",
            cwe="CWE-502",
            description="When deserializing untrusted or corrupted data, it is "
            "possible for a reader to consume memory beyond the allowed "
            "constraints and thus lead to out of memory on the system.\n"
            "\n"
            "This issue affects Java applications using Apache Avro "
            "Java SDK up to and including 1.11.2.  Users should update "
            "to apache-avro version 1.11.3 which addresses this issue.\n"
            "\n",
            coordinates="pkg:maven/org.apache.avro/avro@1.7.7",
            references=(
                "https://ossindex.sonatype.org/vulnerability/CVE-2023-39410?component-type=maven&component-name=org.apache.avro%2Favro&utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2023-39410",
                "https://github.com/apache/avro/pull/2432",
                "https://issues.apache.org/jira/browse/AVRO-3819",
                "https://lists.apache.org/thread/q142wj99cwdd0jo5lvdoxzoymlqyjdds",
            ),
        ),
        security.Issue(
            cve="CVE-2020-36641",
            cwe="CWE-611",
            description="A vulnerability classified as problematic was found in "
            "gturri aXMLRPC up to 1.12.0. This vulnerability affects "
            "the function ResponseParser of the file "
            "src/main/java/de/timroes/axmlrpc/ResponseParser.java. The "
            "manipulation leads to xml external entity reference. "
            "Upgrading to version 1.12.1 is able to address this issue. "
            "The patch is identified as "
            "ad6615b3ec41353e614f6ea5fdd5b046442a832b. It is "
            "recommended to upgrade the affected component. VDB-217450 "
            "is the identifier assigned to this vulnerability.\n"
            "\n"
            "Sonatype's research suggests that this CVE's details "
            "differ from those defined at NVD. See "
            "https://ossindex.sonatype.org/vulnerability/CVE-2020-36641 "
            "for details",
            coordinates="pkg:maven/fr.turri/aXMLRPC@1.13.0",
            references=(
                "https://ossindex.sonatype.org/vulnerability/CVE-2020-36641?component-type=maven&component-name=fr.turri%2FaXMLRPC&utm_source=ossindex-client&utm_medium=integration&utm_content=1.8.1",
                "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2020-36641",
                "https://www.tenable.com/cve/CVE-2020-36641",
            ),
        ),
    }
    actual = set(security.from_maven(maven_report))
    assert actual == expected
