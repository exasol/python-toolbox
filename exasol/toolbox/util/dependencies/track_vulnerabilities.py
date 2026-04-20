from collections import defaultdict
from inspect import cleandoc

from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.dependencies.audit import Vulnerability


class VulnerabilityMatcher:
    def __init__(self, current_vulnerabilities: list[Vulnerability]):
        # Dictionary mapping package names to a unified set of all active
        # vulnerability references (IDs, CVEs, aliases) for that package.
        self._references = defaultdict(set)
        for v in current_vulnerabilities:
            self._references[v.package.name].update(v.references)

    def is_resolved(self, vuln: Vulnerability) -> bool:
        """
        Detects if a vulnerability has been resolved.

        A vulnerability is said to be resolved when it cannot be found in
        the `current_vulnerabilities`.

        Vulnerabilities are matched by the name of the affected package
        and the vulnerability's "references" (set of ID and aliases).

        The vulnerability is rated as "resolved" only if there is not
        intersection between previous and current references.

        This hopefully compensates in case a different ID is assigned to a
        vulnerability.
        """
        refs = set(vuln.references)
        current = self._references.get(vuln.package.name, set())
        return refs.isdisjoint(current)


class DependenciesAudit(BaseModel):
    """
    Compare previous vulnerabilities to current ones and create a report
    about the resolved vulnerabilities.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    previous_vulnerabilities: list[Vulnerability]
    current_vulnerabilities: list[Vulnerability]

    @property
    def resolved_vulnerabilities(self) -> list[Vulnerability]:
        """
        Return the list of resolved vulnerabilities.
        """
        matcher = VulnerabilityMatcher(self.current_vulnerabilities)
        return [
            vuln for vuln in self.previous_vulnerabilities if matcher.is_resolved(vuln)
        ]

    def report_resolved_vulnerabilities(self) -> str:
        if not (resolved := self.resolved_vulnerabilities):
            return ""
        header = cleandoc("""
            This release fixes vulnerabilities by updating dependencies:

            | Dependency | Vulnerability | Affected | Fixed in |
            |------------|---------------|----------|----------|
            """)

        def formatted(vuln: Vulnerability) -> str:
            columns = (
                vuln.package.name,
                vuln.id,
                str(vuln.package.version),
                vuln.fix_versions[0],
            )
            return f'| {" | ".join(columns)} |'

        body = "\n".join(formatted(v) for v in resolved)
        return f"{header}\n{body}"
